# CS108 TA Workspace

## Overview

This workspace is for managing and solving student lab activities running in Docker containers on the Bodhi/cLabs platform (IITB CS108-26). The workflow is: launch container → explore → solve → verify → save locally with TA reference notes → commit.

---

## Credentials & Config

All credentials are in `.env` (gitignored). Load them before any API call:

```bash
source .env
# or read line by line in Python: python-dotenv / manual parse
```

| Variable | Value |
|----------|-------|
| `BODHI_TOKEN` | Bearer token for daemon + backend API |
| `BODHI_DAEMON_URL` | `http://localhost:14014` |
| `BODHI_BACKEND_URL` | `https://robin.bodhi.cse.iitb.ac.in/api` |
| `COURSE_ID` | `136` (CS108-26) |
| `USER_ID` | `2918` (24m0797@iitb.ac.in) |

---

## Platform Architecture

```
cLabs UI (Electron)
    └── clabs-daemon (Docker, port 14014)
            ├── proxies API calls to Bodhi backend (robin.bodhi.cse.iitb.ac.in)
            ├── manages Docker containers for each activity
            └── serves the React frontend
```

Auth: daemon uses `Authorization: Bearer <token>` header. Backend uses `Authorization: Token <token>`.

---

## Container Naming Pattern

```
clab_act_<USER_ID>_<ACTIVITY_ID>
          2918      255           ← platform activity ID, NOT a sequence number
```

Example: `clab_act_2918_255` = user 2918 doing activity 255 (Word Translator, Lab 9).

---

## Key API Endpoints

All daemon calls use `Authorization: Bearer $BODHI_TOKEN`.
All backend calls use `Authorization: Token $BODHI_TOKEN`.

| Action | Method | URL |
|--------|--------|-----|
| Who am I | GET | `{daemon}/auth/whoami` |
| List courses | GET | `{daemon}/courses/` |
| List labs in course | GET | `{daemon}/labs/{course_id}` |
| List activities in lab | GET | `{daemon}/activities/{lab_id}` |
| Get activity details | GET | `{daemon}/activities/activity_details/{activity_id}` |
| **Launch container** | POST | `{daemon}/workspace/create_folders` + body `{"activityId": N}` |
| Container status | GET | `{daemon}/workspace/container_status?studentId={uid}&activityId={aid}` |
| Launch progress | GET | `{daemon}/workspace/{activity_id}/progress` |
| Stop container | GET | `{daemon}/workspace/exit_workspace?studentId={uid}&activityId={aid}` |
| Activity details (backend) | GET | `{backend}/clab/activity/{activity_id}/` |

---

## Lab → Activity ID Map (CS108-26, Course 136)

| Lab ID | Lab Title | Activity IDs | Docker Image |
|--------|-----------|-------------|-------------|
| 800 | Lab 9: Python I | 255, 256, 257, 258, 259 | `lab09-python` |
| 804 | Lab 8: Sed/Awk | 241, 242, 243, 244, 245 | `lab-06` |
| 797 | Lab 7: Bash | 232, 233, 234, 235 | `lab-06` |
| 812 | Lab 6: Git | 216, 217, 218 | `lab-06` |
| 799 | Lab 5: Make/GDB | 149, 150, 151, 152, 153 | `sl108-selenium-latest` |
| 809 | Lab 4: JavaScript | 137, 138, 140 | `sl108-selenium-latest` |
| 808 | Lab 3: HTML/CSS | 126, 128, 129, 130 | `sl104-3` |
| 801 | Lab 2: Linux Adv | 120, 121, 122, 123 | `sl104-1` |
| 802 | Lab 0: Getting Started | 1, 2, 3, 4, 5 | — |

Image registry prefix: `sarus.bodhi.cse.iitb.ac.in/bodhi_robin/424/`

---

## Launching a Container

```bash
curl -s -X POST http://localhost:14014/workspace/create_folders \
  -H "Authorization: Bearer $BODHI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"activityId": 255}'
```

Then poll for the container to appear:
```bash
docker ps --filter "name=clab_act_${USER_ID}_${ACTIVITY_ID}" --format "{{.Names}}"
```

The first launch pulls the Docker image — may take 30–90s depending on image size.

---

## Key Paths Inside Every Container

| Path | Purpose |
|------|---------|
| `/home/labDirectory/` | **Submission directory** — autograder reads from here |
| `/clabTAWorkSpace/studentWorkSpace/` | Student workspace mirror + testcases |
| `/clabTAWorkSpace/studentWorkSpace/testcases/` or `/test/` | Testcase inputs and expected outputs |
| `/clabTAWorkSpace/serverEvalScripts/evaluate.sh` | Eval entry point |
| `/clabTAWorkSpace/serverEvalScripts/autograder/` | Autograder scripts |
| `/home/.evaluationScripts/` | Instructor-side eval scripts (read-only reference) |
| `/home/.evaluationScripts/evaluate.json` | Live evaluation results |

**Always write solutions to `/home/labDirectory/`** — not the workspace mirror.

---

## Standard Solve Workflow

1. **Launch** container via API (or user does it via UI)
2. **Explore** — read skeleton files, testcases, autograder
3. **Solve** — write solution to `/tmp/`, then `docker cp` to `/home/labDirectory/`
4. **Verify** — run all testcases inside container, confirm all pass
5. **Save locally** — create `lab<NN>/act<N>-<name>/` with solution + `solution.md`
6. **Commit & push** — `git add lab<NN>/` → commit → push

---

## Local Folder Structure

```
CS108-2026/
├── .env                    ← credentials (gitignored)
├── .gitignore
├── CLAUDE.md
├── .claude/
│   └── commands/
│       ├── solve-activity.md   ← /solve-activity: solve the currently running container
│       └── solve-lab.md        ← /solve-lab N: launch + solve all activities in lab N
└── lab<NN>/
    ├── act1-<name>/
    │   ├── <solution_file(s)>
    │   └── solution.md
    └── act2-<name>/
        ├── <solution_file(s)>
        └── solution.md
```

---

## solution.md Template

Every `solution.md` must include:

1. **Problem summary** — what the activity asks, modes/functions, input/output format
2. **Key insight** — the non-obvious algorithmic trick or edge case
3. **Core approach** — data structure or algorithm with concise code snippets
4. **Per-function/mode breakdown** — what each part does and common mistakes
5. **Full testcase table** — all inputs and expected outputs
6. **Quick debugging table** — symptom → likely cause

Goal: a TA can help any student using only `solution.md`, without re-reading the code.

---

## Lab 9 Activity Reference (Solved)

| Activity ID | Name | Key Insight |
|-------------|------|-------------|
| 255 | Word Translator | BFS for indirect translations via intermediate language |
| 256 | Basic Maths (Complex/Polar) | Implement modulus, arg, abscissa, ordinate, distance; must import classes correctly |
| 257 | Olympics | Aggregate medals across files; sort by gold desc, ties alphabetically |
| 258 | Casino Dice | DP: count ordered dice-roll sequences summing to N, mod 10^9+7 |
| 259 | Tower of Hanoi | Standard recursion; print move count on line 1, then `src dst` per line |
