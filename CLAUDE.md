# CS108 TA Workflow

## Overview

This workspace is for managing and solving student lab activities running in Docker containers on the Bodhi platform (IITB). The workflow is: inspect container → infer lab/activity → solve → verify → save locally with TA reference notes.

---

## Step 1: Check Running Containers

```bash
docker ps
```

Key fields to note from the output:
- **Container name**: `clab_act_<activity_id>_<instance>` — activity ID is the number after `act_`
- **Image**: `sarus.bodhi.cse.iitb.ac.in/bodhi_robin/<course_id>/<lab>-<language>` — gives lab number and language
- **Ports**: which ports are exposed

Example:
```
clab_act_2918_255   bodhi_robin/424/lab09-python   → Lab 09, Activity 2918, Python
```

---

## Step 2: Explore the Container

Always check these three locations:

```bash
docker exec <container> ls /home/labDirectory/          # student submission files
docker exec <container> ls /clabTAWorkSpace/studentWorkSpace/   # includes testcases/
docker exec <container> ls /clabTAWorkSpace/serverEvalScripts/autograder/
```

Read the autograder to understand:
- What files it expects (`/home/labDirectory/` is the submission path)
- How it scores (per-testcase, epsilon comparisons, import checks, etc.)
- Any special pre-checks (e.g. import string detection)

Read all testcase inputs and expected outputs:
```bash
docker exec <container> ls /clabTAWorkSpace/studentWorkSpace/testcases/
# or
docker exec <container> ls /clabTAWorkSpace/studentWorkSpace/test/
```

---

## Step 3: Infer Activity Name and Details

From the image name and container name:
- **Lab number**: from image tag (e.g. `lab09`)
- **Activity ID**: from container name (e.g. `act_2918`)
- **Language**: from image tag (e.g. `python`)
- **Activity name**: inferred from the student files and testcases (not always explicitly stated)
- **Course**: from image path (e.g. `424`)

---

## Step 4: Write the Solution

- Read all student skeleton files in `/home/labDirectory/`
- Read all testcase input/output files to understand exact expected format
- Read the autograder (`autograder.py` or `evaluate.sh`) for scoring logic and edge cases
- Write the solution locally at `/tmp/<filename>`
- Copy into the container's submission directory:

```bash
docker cp /tmp/<file> <container>:/home/labDirectory/<file>
```

**Important:** Always write to `/home/labDirectory/` — this is what the autograder reads. The `/clabTAWorkSpace/studentWorkSpace/` directory is a mirror but is NOT what gets evaluated.

---

## Step 5: Verify All Testcases

Run testcases manually inside the container before considering done. Either:

**For shell-script based testcases** (compare stdout):
```bash
for tc in q1_1 q1_2 ...; do
  cmd=$(docker exec <container> cat /clabTAWorkSpace/studentWorkSpace/testcases/${tc}.sh)
  expected=$(docker exec <container> cat /clabTAWorkSpace/studentWorkSpace/testcases/out_${tc}.txt)
  actual=$(docker exec -w /home/labDirectory <container> bash -c "$cmd")
  [ "$actual" = "$expected" ] && echo "PASS $tc" || echo "FAIL $tc"
done
```

**For Python-based testcases** (inline verification):
```bash
docker exec -w /home/labDirectory <container> python3 -c "
# import solution, run each testcase, compare against expected
"
```

All testcases must pass before moving on.

---

## Step 6: Save Locally

### Folder structure

```
CS108-2026/
└── lab<NN>/
    ├── act1-<activity-name>/
    │   ├── <solution_file(s)>
    │   └── solution.md
    └── act2-<activity-name>/
        ├── <solution_file(s)>
        └── solution.md
```

Create the subfolder and copy the solution:
```bash
mkdir -p lab<NN>/act<N>-<name>
cp /tmp/<file> lab<NN>/act<N>-<name>/
```

### Write solution.md

Each `solution.md` is a TA reference guide. It must include:

1. **Problem summary** — what the activity asks, modes/functions, input/output format
2. **Key insight** — the non-obvious part of the solution (algorithmic trick, edge case, etc.)
3. **Core approach** — data structure or algorithm used, with concise code snippets
4. **Per-function/mode breakdown** — what each part does and common mistakes for each
5. **Full testcase table** — all inputs and expected outputs in one place
6. **Quick debugging table** — symptom → likely cause, for fast student help

The goal: a TA should be able to help any student using only the `solution.md`, without re-reading the code.

---

## Naming Conventions

| Thing | Convention |
|-------|-----------|
| Local lab folder | `lab09/`, `lab10/`, etc. |
| Local activity subfolder | `act1-word-translator/`, `act2-complex-polar/` |
| Activity name | Inferred from files; use kebab-case |
| solution.md | Always named exactly `solution.md` |

---

## Quick Reference: Key Paths Inside Container

| Path | Purpose |
|------|---------|
| `/home/labDirectory/` | **Submission directory** — autograder reads from here |
| `/clabTAWorkSpace/studentWorkSpace/` | Student workspace mirror + testcases |
| `/clabTAWorkSpace/studentWorkSpace/testcases/` or `/test/` | Testcase inputs and expected outputs |
| `/clabTAWorkSpace/serverEvalScripts/evaluate.sh` | Eval entry point |
| `/clabTAWorkSpace/serverEvalScripts/autograder/` | Autograder scripts |
| `/home/.evaluationScripts/evaluate.json` | Live evaluation results (updated after grader runs) |
