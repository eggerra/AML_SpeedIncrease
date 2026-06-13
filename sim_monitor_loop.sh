#!/usr/bin/env bash
# sim_monitor_loop.sh
# Updates simulation_log.md and pushes to git every 10 minutes.
# Stops when the Abaqus lock file disappears (job finished or aborted).

BASE="D:/Projects_AI/AML_SpeedIncrease"
JOB="ValveSpring_oval_contact_abaqus"
LCK="$BASE/$JOB.lck"
LOG="$BASE/simulation_log.md"
DONE_FLAG="$BASE/.sim_monitor_done"

cd "$BASE"

echo "[sim_monitor] Started at $(date '+%Y-%m-%d %H:%M:%S')"

# Wait up to 10 minutes for Abaqus to create the lock file
echo "[sim_monitor] Waiting for job lock file to appear..."
for i in $(seq 1 60); do
    [ -f "$LCK" ] && break
    sleep 10
done
if [ ! -f "$LCK" ]; then
    echo "[sim_monitor] WARNING: lock file never appeared — job may not have started."
fi

while true; do
    # Update log
    python "$BASE/monitor_sim.py"

    # Stage and commit log
    git add simulation_log.md
    git diff --cached --quiet || git commit -m "sim: status update $(date '+%Y-%m-%d %H:%M:%S')"
    git push origin abaqus 2>&1 | tail -3

    # Check if job is still running
    if [ ! -f "$LCK" ]; then
        echo "[sim_monitor] Lock file gone — job finished. Running final update."
        # Final log update
        python "$BASE/monitor_sim.py"
        git add simulation_log.md
        git commit -m "sim: final status — job complete $(date '+%Y-%m-%d %H:%M:%S')"
        git push origin abaqus
        touch "$DONE_FLAG"
        echo "[sim_monitor] Done."
        break
    fi

    echo "[sim_monitor] Job still running — sleeping 10 min..."
    sleep 600
done
