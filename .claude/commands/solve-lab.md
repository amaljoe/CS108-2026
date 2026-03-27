Solve all activities under a given lab number end-to-end, fully autonomously.

The user will invoke this as: `/solve-lab <N>` where N is the lab number (e.g. 8, 9).

---

## Setup: Load credentials from .env

Read `.env` from the project root. Extract:
- `BODHI_TOKEN` — auth token for all API calls
- `BODHI_DAEMON_URL` — local daemon (default: http://localhost:14014)
- `BODHI_BACKEND_URL` — Bodhi backend (default: https://robin.bodhi.cse.iitb.ac.in/api)
- `COURSE_ID` — e.g. 136
- `USER_ID` — e.g. 2918

---

## Step 1: Resolve Lab Number → Lab ID

Call the daemon labs API to find the lab whose title matches "Lab <N>":

```bash
curl -s http://localhost:14014/labs/${COURSE_ID} \
  -H "Authorization: Bearer ${BODHI_TOKEN}"
```

Match lab by title containing "Lab <N>" or "Lab<N>" (case-insensitive). Extract its `id`.

---

## Step 2: Get All Activities for the Lab

```bash
curl -s http://localhost:14014/activities/${LAB_ID} \
  -H "Authorization: Bearer ${BODHI_TOKEN}"
```

Extract list of `{id, name}` pairs, sorted by id. These are the activities to solve in order.

---

## Step 3: For Each Activity — Launch Container

Launch the container via the daemon:

```bash
curl -s -X POST http://localhost:14014/workspace/create_folders \
  -H "Authorization: Bearer ${BODHI_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"activityId\": ${ACTIVITY_ID}}"
```

Then poll until the container appears in `docker ps`:
```bash
# Container name pattern: clab_act_<USER_ID>_<ACTIVITY_ID>
docker ps --filter "name=clab_act_${USER_ID}_${ACTIVITY_ID}" --format "{{.Names}}"
```

Wait up to 60 seconds (poll every 3s). The container pulls the image on first launch — may take longer if image not cached locally.

---

## Step 4: Solve the Activity

Once the container is running, follow the same workflow as `/solve-activity`:

1. Explore `/home/labDirectory/` and `/clabTAWorkSpace/studentWorkSpace/`
2. Read autograder at `/clabTAWorkSpace/serverEvalScripts/autograder/` or `evaluate.sh`
3. Read all testcase inputs/outputs
4. Understand the problem and write the solution
5. Copy solution to `/home/labDirectory/` via `docker cp`

```bash
CONTAINER="clab_act_${USER_ID}_${ACTIVITY_ID}"
docker cp /tmp/<solution_file> ${CONTAINER}:/home/labDirectory/<solution_file>
```

---

## Step 5: Verify All Testcases

Run every testcase inside the container and confirm all pass before proceeding.

---

## Step 6: Save Locally + Write solution.md

Determine activity index (1, 2, 3...) from its position in the sorted activity list.
Infer activity name from the activity `name` field (slugify it).

Create folder:
```
lab<NN>/act<index>-<slugified-name>/
    <solution_file(s)>
    solution.md
```

Write `solution.md` per the standard format (see CLAUDE.md).

---

## Step 7: Stop the Container

After solving, stop the container to free resources:

```bash
docker stop clab_act_${USER_ID}_${ACTIVITY_ID}
```

---

## Step 8: Commit After All Activities Done

After all activities in the lab are solved, create a single commit:

```bash
git add lab<NN>/
git commit -m "Add Lab <NN> solutions: <comma-separated activity names>"
git push
```

---

## Error Handling

- If container fails to start after 60s, skip that activity and note it
- If a testcase fails after writing the solution, debug and re-attempt before moving on
- If the autograder uses a 3s timeout, ensure solutions are efficient enough

---

## Key API Reference (from CLAUDE.md)

| Action | Method | Endpoint |
|--------|--------|----------|
| List labs | GET | `{daemon}/labs/{course_id}` |
| List activities | GET | `{daemon}/activities/{lab_id}` |
| Get activity details | GET | `{daemon}/activities/activity_details/{activity_id}` |
| Launch container | POST | `{daemon}/workspace/create_folders` body: `{"activityId": N}` |
| Stop container | GET | `{daemon}/workspace/exit_workspace?studentId={uid}&activityId={aid}` |
| Evaluate | POST | `{daemon}/evaluate/...` |

Container name: `clab_act_<USER_ID>_<ACTIVITY_ID>`
