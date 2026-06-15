"""
monitor_jobs.py  —  dual-job status monitor
Checks local Abaqus job + HPC cluster job, writes simulation_log.md, pushes to git.
Run once per invocation (cron handles the 10-min interval).
"""
import os, re, subprocess, datetime, paramiko

BASE        = r"D:\Projects_AI\AML_SpeedIncrease"
LOG_FILE    = os.path.join(BASE, "simulation_log.md")
LOCAL_STA   = os.path.join(BASE, "ValveSpring_oval_contact_abaqus.sta")
LOCAL_MSG   = os.path.join(BASE, "ValveSpring_oval_contact_abaqus.msg")
REMOTE_DIR  = "/lustre/calc1/eggerra/eggerra_AW82001_5004_AML_SpeedIncrease"
REMOTE_STA  = f"{REMOTE_DIR}/ValveSpring_oval_contact_abaqus.sta"
REMOTE_LOG  = f"{REMOTE_DIR}/ValveSpring_oval_contact_abaqus.log"
HPC_HOST    = "fe6"
HPC_USER    = "eggerra"
HPC_PASS    = "Rebengasse1@graz"
HPC_JOB_ID  = "279357.atgrzsl4803"


def parse_sta(text):
    """Return (step, inc, total_time, step_time) from last data line of .sta file."""
    lines = [l for l in text.splitlines() if re.match(r'\s+\d+\s+\d+', l)]
    if not lines:
        return None
    parts = lines[-1].split()
    try:
        step = int(parts[0]); inc = int(parts[1])
        # .sta columns: STEP INC ATT SEV_DISC EQUIL TOTAL_ITERS TOTAL_TIME STEP_TIME INC_TIME
        total_time = float(parts[6]); step_time = float(parts[7])
        return step, inc, total_time, step_time
    except Exception:
        return None


def read_local_sta():
    try:
        with open(LOCAL_STA) as f:
            return f.read()
    except Exception:
        return ""


def local_job_running():
    result = subprocess.run(
        ["tasklist"], capture_output=True, text=True, shell=True
    )
    return "standard.exe" in result.stdout.lower()


def get_hpc_status(client):
    """Returns (qstat_line, sta_text, log_tail)."""
    try:
        # qstat — use -u to avoid tcsh redirection issues
        job_short = HPC_JOB_ID.split('.')[0]
        _, stdout, _ = client.exec_command(f"qstat -u eggerra")
        qstat_all = stdout.read().decode()
        qstat = next((l for l in qstat_all.splitlines() if job_short in l), 'NOT_FOUND')

        # .sta file
        _, stdout, _ = client.exec_command(f"cat {REMOTE_STA} 2>/dev/null || echo ''")
        sta = stdout.read().decode()

        # job log tail (only exists once running)
        _, stdout, _ = client.exec_command(
            f"tail -5 {REMOTE_DIR}/ValveSpring_oval_contact_abaqus.log 2>/dev/null || echo ''"
        )
        log_tail = stdout.read().decode().strip()

        return qstat, sta, log_tail
    except Exception as e:
        return f"SSH error: {e}", "", ""


def format_sta_summary(sta_text, label):
    info = parse_sta(sta_text)
    if not info:
        return f"  - {label}: no increment data yet"
    step, inc, total_time, step_time = info
    step_name = "preload" if step == 1 else "valve lift"
    step_end  = 10.0 if step == 1 else 10.0
    pct = min(100.0, step_time / step_end * 100)
    return (
        f"  - {label}: Step {step} ({step_name}), "
        f"Inc {inc}, step time {step_time:.2f}/{step_end:.1f} mm ({pct:.0f}%)"
    )


def main():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # --- LOCAL JOB ---
    local_sta_text = read_local_sta()
    local_running  = local_job_running()
    local_summary  = format_sta_summary(local_sta_text, "Local (Win, 14 CPU)")
    local_status   = "RUNNING" if local_running else "FINISHED/STOPPED"

    # --- HPC JOB ---
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HPC_HOST, username=HPC_USER, password=HPC_PASS, timeout=15)
        qstat, hpc_sta_text, log_tail = get_hpc_status(client)
        client.close()
        hpc_ok = True
    except Exception as e:
        qstat = f"SSH error: {e}"
        hpc_sta_text = ""
        log_tail = ""
        hpc_ok = False

    # Parse HPC queue status
    if "NOT_FOUND" in qstat or not qstat:
        hpc_queue = "UNKNOWN / NOT IN QUEUE"
    elif re.search(r'\bQ\b', qstat):
        hpc_queue = "QUEUED"
    elif re.search(r'\bR\b', qstat):
        hpc_queue = "RUNNING"
    elif re.search(r'\bF\b|\bC\b|\bE\b', qstat):
        hpc_queue = "FINISHED"
    else:
        hpc_queue = qstat.split('\n')[-1][:60] if qstat else "UNKNOWN"

    hpc_summary = format_sta_summary(hpc_sta_text, f"HPC fe6 (32 CPU, Abq2025HF4) — {hpc_queue}")

    # --- BUILD LOG ENTRY ---
    entry = f"""
---
### {now}

**Local job** (`ValveSpring_oval_contact_abaqus`) — {local_status}
{local_summary}

**HPC job** (`{HPC_JOB_ID}`) — {hpc_queue}
{hpc_summary}
"""
    if log_tail and hpc_queue == "RUNNING":
        entry += f"\n  HPC log tail:\n```\n{log_tail}\n```\n"

    # --- WRITE LOG ---
    header_needed = not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        if header_needed:
            f.write("# Simulation Monitor — ValveSpring Abaqus (L0=47.440 mm)\n\n")
            f.write("Both local (14 CPU) and HPC cluster (16 CPU, fe6) jobs running in parallel.\n")
            f.write("Geometry: oval wire 2.92×3.66 mm, L0=47.440 mm, 18428 nodes, 9157 C3D10 elements.\n")
            f.write("Step 1: compress 15.8 mm to installed length. Step 2: 10 mm valve lift.\n\n")
        f.write(entry)
    print(f"[{now}] Log updated.")

    # --- GIT PUSH ---
    os.chdir(BASE)
    subprocess.run(["git", "add", "simulation_log.md"], check=True)
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        capture_output=True
    )
    if result.returncode != 0:
        subprocess.run(
            ["git", "commit", "-m", f"sim: status update {now}"],
            check=True
        )
        subprocess.run(["git", "push"], check=True)
        print(f"[{now}] Pushed to git.")
    else:
        print(f"[{now}] No changes to commit.")


if __name__ == "__main__":
    main()
