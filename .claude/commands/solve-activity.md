Solve the currently running lab activity Docker container end-to-end as a CS108 TA.

Follow these steps in order:

## 1. Check running containers
Run `docker ps` and identify the new activity container (ignore `clabs-daemon`).
From the container name and image, extract:
- Lab number (from image tag, e.g. `lab09`)
- Activity ID (from container name, e.g. `act_2918`)
- Language (from image tag, e.g. `python`)

## 2. Explore the container
Check these paths:
- `/home/labDirectory/` — student submission files (skeleton)
- `/clabTAWorkSpace/studentWorkSpace/` — testcases directory
- `/clabTAWorkSpace/serverEvalScripts/autograder/` — autograder scripts

Read all skeleton files, all testcase inputs/outputs, and the autograder to understand scoring logic and any special checks (e.g. import string detection).

## 3. Write the solution
Implement the solution based on the testcases. Write it to `/tmp/` first, then copy to `/home/labDirectory/` inside the container:
```bash
docker cp /tmp/<file> <container>:/home/labDirectory/<file>
```
Always target `/home/labDirectory/` — that is what the autograder reads.

## 4. Verify all testcases
Run every testcase inside the container and confirm all pass before proceeding.

For shell-script testcases:
```bash
cmd=$(docker exec <container> cat /clabTAWorkSpace/studentWorkSpace/testcases/<tc>.sh)
expected=$(docker exec <container> cat /clabTAWorkSpace/studentWorkSpace/testcases/out_<tc>.txt)
actual=$(docker exec -w /home/labDirectory <container> bash -c "$cmd")
[ "$actual" = "$expected" ] && echo "PASS" || echo "FAIL"
```

For Python-based testcases, run an inline verification script inside the container.

## 5. Save locally
Determine the next available activity subfolder under the appropriate lab folder:
```
CS108-2026/
└── lab<NN>/
    └── act<N>-<activity-name>/
        ├── <solution_file(s)>
        └── solution.md
```

Create the subfolder, copy the solution file(s) into it.

## 6. Write solution.md
Write a TA reference guide at `lab<NN>/act<N>-<name>/solution.md` that includes:

1. **Problem summary** — what the activity asks, modes/functions, input/output format
2. **Key insight** — the non-obvious algorithmic trick or edge case
3. **Core approach** — data structure or algorithm with concise code snippets
4. **Per-function/mode breakdown** — what each part does and common mistakes
5. **Full testcase table** — all inputs and expected outputs
6. **Quick debugging table** — symptom → likely cause, for fast student help

The solution.md should be good enough that a TA can help any student using only that file.
