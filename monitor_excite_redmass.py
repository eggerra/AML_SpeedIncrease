"""
monitor_excite_redmass.py
=========================
Monitors EXCITE Timing Drive runs for AML_AE26_ChainDrive__04_spring_update_redMass
and writes excite_td_redmass_log.md every 10 minutes, committed and pushed
to the excite_td branch via a dedicated worktree.

Usage
-----
    python monitor_excite_redmass.py          # runs until all jobs complete
    python monitor_excite_redmass.py --once   # write one snapshot and exit
"""
import os, sys, re, subprocess, time, datetime, json

BASE        = r"D:\Projects_AI\AML_SpeedIncrease"
ETD_DIR     = r"D:\AW82001\5005\excite_td"
MODEL       = "AML_AE26_ChainDrive__04_spring_update_redMass"
CASESET     = f"{MODEL}.EngineSpeed"
LOG_NAME    = "excite_td_redmass_log.md"
STATE_FILE  = os.path.join(BASE, ".excite_redmass_state.json")
WT_PATH     = os.path.join(BASE, ".excite_td_wt")   # shared worktree for excite_td branch
INTERVAL    = 600   # 10 minutes

# Total cam angle: simulation runs 0 → 5400° (15 cam cycles × 360°)
TOTAL_CAM   = 5400.0

# Discover RPM subdirs: <MODEL>.EngineSpeed.<XXXX>rpm
RPM_DIRS = sorted(
    [d for d in os.listdir(ETD_DIR)
     if os.path.isdir(os.path.join(ETD_DIR, d))
     and d.startswith(CASESET + ".")
     and re.search(r"\.\d+rpm$", d)],
    key=lambda x: int(re.search(r"\.(\d+)rpm$", x).group(1)),
)


def read_jobstate(run_dir):
    path = os.path.join(run_dir, "jobstate")
    if not os.path.isfile(path):
        return "unknown"
    try:
        with open(path) as f:
            content = f.read()
        m = re.search(r"state\s+(\S+)", content)
        return m.group(1) if m else "unknown"
    except Exception:
        return "unknown"


def read_last_cam_angle(run_dir):
    path = os.path.join(run_dir, "simulation.out")
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "rb") as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - 8192))
            tail = f.read().decode("utf-8", errors="replace")
        matches = re.findall(r"Cam Angle:\s+[\d.E+\-]+\s*/\s*([\d.]+)", tail)
        if matches:
            return float(matches[-1])
        matches2 = re.findall(r"\(\s*[\d.E+\-]+\s+([\d.]+)\s+[\d.E+\-]", tail)
        return float(matches2[-1]) if matches2 else None
    except Exception:
        return None


def read_cpu_wall(run_dir):
    path = os.path.join(run_dir, "jobstate")
    if not os.path.isfile(path):
        return None, None
    try:
        with open(path) as f:
            content = f.read()
        cpu  = re.search(r"cpuTime\s+([\d.]+)", content)
        wall = re.search(r"wallClockTime\s+([\d.]+)", content)
        return (float(cpu.group(1)) if cpu else None,
                float(wall.group(1)) if wall else None)
    except Exception:
        return None, None


def get_run_info(name):
    run_dir = os.path.join(ETD_DIR, name)
    rpm_m   = re.search(r"\.(\d+)rpm$", name)
    rpm     = int(rpm_m.group(1)) if rpm_m else 0
    state   = read_jobstate(run_dir)
    cam     = read_last_cam_angle(run_dir)
    pct     = (cam / TOTAL_CAM * 100) if cam is not None else None
    cpu, wall = read_cpu_wall(run_dir)
    return dict(name=name, rpm=rpm, state=state,
                cam=cam, pct=pct, cpu=cpu, wall=wall)


def fmt_duration(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    if h > 0:
        return f"{h}h {m:02d}m"
    return f"{m}m"


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def write_status(runs):
    now     = datetime.datetime.now()
    now_ts  = time.time()
    n_total = len(runs)
    n_done  = sum(1 for r in runs if r["state"] in {"finished", "completed"})
    n_run   = sum(1 for r in runs if r["state"] == "running")
    n_wait  = sum(1 for r in runs if r["state"] == "unknown")

    pcts    = [r["pct"] for r in runs if r["pct"] is not None]
    avg_pct = sum(pcts) / len(pcts) if pcts else 0.0

    state     = load_state()
    prev_pct  = state.get("avg_pct", 0.0)
    prev_ts   = state.get("timestamp", now_ts)
    delta_pct = avg_pct - prev_pct
    delta_s   = now_ts - prev_ts

    if delta_pct > 0 and delta_s > 0:
        rate_pct_per_s = delta_pct / delta_s
        remaining_s    = (100.0 - avg_pct) / rate_pct_per_s
        eta_dt         = now + datetime.timedelta(seconds=remaining_s)
        eta_str        = f"{fmt_duration(remaining_s)} (ETA {eta_dt.strftime('%H:%M')})"
    elif avg_pct > 0 and (now_ts - state.get("first_ts", now_ts)) > 0:
        total_s = now_ts - state.get("first_ts", now_ts)
        rate    = avg_pct / total_s if total_s > 0 else 0
        remaining_s = (100.0 - avg_pct) / rate if rate > 0 else 0
        eta_dt  = now + datetime.timedelta(seconds=remaining_s)
        eta_str = f"{fmt_duration(remaining_s)} (ETA {eta_dt.strftime('%H:%M')})"
    else:
        eta_str = "— (awaiting data)"

    save_state({
        "avg_pct":   avg_pct,
        "timestamp": now_ts,
        "first_ts":  state.get("first_ts", now_ts),
    })

    elapsed_s = now_ts - state.get("first_ts", now_ts)

    lines = [
        f"# EXCITE Timing Drive — {MODEL}",
        f"",
        f"**Model:** `{MODEL}.etd`  ",
        f"**Caseset:** `{CASESET}`  ",
        f"**RPM cases:** {', '.join(str(r['rpm']) for r in runs)}  ",
        f"**Total duration:** 5400° cam angle  ",
        f"**Last updated:** {now.strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Monitor elapsed:** {fmt_duration(max(0, elapsed_s))}  ",
        f"**Est. remaining:** {eta_str}  ",
        f"**Status:** {n_done}/{n_total} finished, {n_run} running, {n_wait} queued",
        f"",
        f"## Run Progress",
        f"",
        f"| RPM | State | Cam angle | Progress | CPU time (s) | Wall time (s) |",
        f"|-----|-------|-----------|----------|--------------|---------------|",
    ]

    all_done = True
    for r in runs:
        icon = {"running": "▶", "finished": "✓", "completed": "✓",
                "error": "✗", "submitted": "⏳", "unknown": "⏳"}.get(r["state"], "?")
        cam_str  = f"{r['cam']:.1f}°" if r["cam"] is not None else "—"
        pct_str  = f"{r['pct']:.1f}%" if r["pct"] is not None else "—"
        cpu_str  = f"{r['cpu']:.0f}" if r["cpu"] else "—"
        wall_str = f"{r['wall']:.0f}" if r["wall"] else "—"
        lines.append(
            f"| {r['rpm']} | {icon} {r['state']} | {cam_str} | {pct_str} | {cpu_str} | {wall_str} |"
        )
        if r["state"] not in {"finished", "completed", "error"}:
            all_done = False

    if pcts:
        bar_fill = int(avg_pct / 5)
        bar      = "█" * bar_fill + "░" * (20 - bar_fill)
        lines += [
            f"",
            f"## Overall Progress",
            f"",
            f"`[{bar}]` {avg_pct:.1f}% average across {len(pcts)} active case(s)  ",
            f"**Est. remaining:** {eta_str}",
        ]

    lines += ["", "---", f"_Auto-generated by monitor_excite_redmass.py — updates every 10 min_"]
    content = "\n".join(lines) + "\n"

    # Write to both main repo (reference copy) and worktree (for git commit).
    # Preserve any manually-appended sections that follow the auto-generated sentinel.
    SENTINEL = "\n---\n_Auto-generated by monitor_excite_redmass.py"
    for target_dir in [BASE, WT_PATH]:
        try:
            fpath = os.path.join(target_dir, LOG_NAME)
            tail = ""
            if os.path.isfile(fpath):
                existing = open(fpath, encoding="utf-8").read()
                idx = existing.find(SENTINEL)
                if idx >= 0:
                    after = existing[idx + len(SENTINEL):]
                    # skip to end of sentinel line, keep anything after
                    nl = after.find("\n")
                    tail = after[nl:] if nl >= 0 else ""
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content + tail)
        except Exception:
            pass

    return all_done, runs, avg_pct


def write_final_docs(runs):
    """Write completion summary appended to excite_td_simulation_log.md."""
    now = datetime.datetime.now()
    log_path = os.path.join(BASE, "excite_td_simulation_log.md")

    completion_block = [
        f"",
        f"---",
        f"",
        f"## {MODEL} — Final Results",
        f"",
        f"**Completed:** {now.strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"",
        f"| RPM | State | Final cam angle | Progress | CPU time (s) | Wall time (s) |",
        f"|-----|-------|-----------------|----------|--------------|---------------|",
    ]
    for r in runs:
        icon     = "✓" if r["state"] in {"finished", "completed"} else "✗"
        cam_str  = f"{r['cam']:.1f}°" if r["cam"] is not None else "—"
        pct_str  = f"{r['pct']:.1f}%" if r["pct"] is not None else "—"
        cpu_str  = f"{r['cpu']:.0f}" if r["cpu"] else "—"
        wall_str = f"{r['wall']:.0f}" if r["wall"] else "—"
        completion_block.append(
            f"| {r['rpm']} | {icon} {r['state']} | {cam_str} | {pct_str} | {cpu_str} | {wall_str} |"
        )

    completion_block += [
        f"",
        f"**Notes:** Reduced-mass variant of `_04_spring_update` — all {len(runs)} RPM cases completed successfully.",
    ]

    # Append to master log in worktree and base
    for target_dir in [BASE, WT_PATH]:
        try:
            with open(os.path.join(target_dir, os.path.basename(log_path)), "a", encoding="utf-8") as f:
                f.write("\n".join(completion_block) + "\n")
        except Exception:
            pass

    # Also mark redmass log as complete in worktree and base
    for target_dir in [BASE, WT_PATH]:
        try:
            with open(os.path.join(target_dir, LOG_NAME), "a", encoding="utf-8") as f:
                f.write(f"\n**SIMULATION COMPLETE** — {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
        except Exception:
            pass

    print(f"  [{now.strftime('%H:%M:%S')}] Final docs written to {log_path} and {redmass_log}")


def ensure_worktree():
    if not os.path.isdir(WT_PATH):
        subprocess.run(
            ["git", "-C", BASE, "worktree", "add", WT_PATH, "excite_td"],
            check=True, capture_output=True,
        )


def git_push(message, extra_files=None):
    wt = WT_PATH
    files = [LOG_NAME]
    if extra_files:
        files.extend(extra_files)
    for f in files:
        subprocess.run(["git", "-C", wt, "add", f],
                       check=False, capture_output=True)
    subprocess.run(["git", "-C", wt, "commit", "-m", message],
                   check=False, capture_output=True)
    subprocess.run(["git", "-C", wt, "push", "origin", "excite_td"],
                   check=False, capture_output=True)


DONE_STATES = {"finished", "completed"}

def snapshot():
    runs            = [get_run_info(n) for n in RPM_DIRS]
    all_done, runs, avg_pct = write_status(runs)
    n_run   = sum(1 for r in runs if r["state"] == "running")
    n_done  = sum(1 for r in runs if r["state"] in DONE_STATES)
    n_total = len(runs)
    now     = datetime.datetime.now()

    if all_done:
        msg = f"excite_redmass: all {n_total} runs completed — {MODEL}"
        write_final_docs(runs)
        git_push(msg, extra_files=["excite_td_simulation_log.md"])
        print(f"  [{now.strftime('%H:%M:%S')}] {msg} — pushed to excite_td")
    else:
        msg = (f"excite_redmass: {n_run}/{n_total} running, {n_done}/{n_total} done, "
               f"avg {avg_pct:.1f}% — {MODEL}")
        git_push(msg)
        print(f"  [{now.strftime('%H:%M:%S')}] {msg} — pushed to excite_td")

    return all_done


if __name__ == "__main__":
    once = "--once" in sys.argv
    print(f"EXCITE TD redMass monitor starting")
    print(f"  Model : {MODEL}")
    print(f"  ETD   : {ETD_DIR}")
    print(f"  Cases : {len(RPM_DIRS)} RPM dirs")
    for d in RPM_DIRS:
        print(f"          {d}")
    print(f"  Log   : {LOG_NAME}")
    print(f"  Branch: excite_td (via worktree {WT_PATH})")

    ensure_worktree()
    done = snapshot()
    if once or done:
        sys.exit(0)

    while True:
        time.sleep(INTERVAL)
        done = snapshot()
        if done:
            print("All runs finished — monitor exiting.")
            break
