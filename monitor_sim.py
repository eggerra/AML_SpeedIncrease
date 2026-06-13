"""
monitor_sim.py
==============
Reads ValveSpring_oval_contact_abaqus .sta / .msg and writes simulation_log.md.
Called by the background monitor loop every 10 minutes.
"""
import os, re, subprocess
from datetime import datetime

BASE    = r"D:\Projects_AI\AML_SpeedIncrease"
JOB     = "ValveSpring_oval_contact_abaqus"
STA     = os.path.join(BASE, JOB + ".sta")
MSG     = os.path.join(BASE, JOB + ".msg")
LCK     = os.path.join(BASE, JOB + ".lck")
LOG     = os.path.join(BASE, "simulation_log.md")

def read_tail(path, n=60):
    if not os.path.isfile(path):
        return "(file not found)"
    with open(path, "r", errors="replace") as f:
        lines = f.readlines()
    return "".join(lines[-n:])

def job_running():
    return os.path.isfile(LCK)

def parse_sta(sta_text):
    """Return list of (step, inc, att, converged, total_time, inc_size) from .sta lines."""
    rows = []
    for line in sta_text.splitlines():
        m = re.match(
            r"\s*(\d+)\s+(\d+)\s+(\d+)(U?)\s+(\d+)\s+(\d+)\s+(\d+)\s+"
            r"([\d.E+\-]+)\s+([\d.E+\-]+)\s+([\d.E+\-]+)", line)
        if m:
            rows.append({
                "step": int(m.group(1)), "inc": int(m.group(2)),
                "att": int(m.group(3)), "converged": m.group(4) != "U",
                "total_time": float(m.group(8)), "inc_size": float(m.group(10)),
            })
    return rows

def extract_errors_warnings(msg_text):
    lines = msg_text.splitlines()
    hits = []
    for i, line in enumerate(lines):
        if "***ERROR" in line or "***WARNING" in line:
            block = lines[i:i+3]
            hits.append(" ".join(l.strip() for l in block if l.strip()))
    return hits[-20:]  # last 20

def count_summary(msg_text):
    m_err  = re.search(r"(\d+)\s+ERROR MESSAGES", msg_text)
    m_warn = re.search(r"(\d+)\s+WARNING MESSAGES DURING ANALYSIS", msg_text)
    m_wall = re.search(r"WALLCLOCK TIME \(SEC\)\s*=\s*([\d.E+]+)", msg_text)
    m_cpu  = re.search(r"TOTAL CPU TIME \(SEC\)\s*=\s*([\d.E+]+)", msg_text)
    return {
        "errors":   int(m_err.group(1))  if m_err  else None,
        "warnings": int(m_warn.group(1)) if m_warn else None,
        "wallclock": float(m_wall.group(1)) if m_wall else None,
        "cpu":       float(m_cpu.group(1))  if m_cpu  else None,
    }

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sta_text = read_tail(STA, n=80)
    msg_text = read_tail(MSG, n=120)
    running  = job_running()

    rows = parse_sta(sta_text)
    last = rows[-1] if rows else None
    errors_warnings = extract_errors_warnings(msg_text)
    summary = count_summary(msg_text)

    # Determine overall status
    if running:
        status = "RUNNING"
    elif summary["errors"]:
        status = "FAILED"
    elif "HAS NOT BEEN COMPLETED" in msg_text or "HAS NOT BEEN COMPLETED" in sta_text:
        status = "ABORTED"
    elif "SUCCESSFULLY COMPLETED" in msg_text or "HAS BEEN COMPLETED" in msg_text:
        status = "COMPLETED"
    else:
        status = "UNKNOWN"

    lines = []
    lines.append(f"# Simulation Run Log — {JOB}")
    lines.append(f"\n**Last updated:** {now}  \n**Job status:** {status}\n")

    lines.append("## Current Progress (.sta)")
    if last:
        conv = "converged" if last["converged"] else "NOT CONVERGED"
        lines.append(f"- Step {last['step']}, Increment {last['inc']}, "
                     f"Attempt {last['att']} — **{conv}**")
        lines.append(f"- Total time: {last['total_time']:.4f}  |  "
                     f"Increment size: {last['inc_size']:.5f}")
        completed = [r for r in rows if r["converged"]]
        lines.append(f"- Converged increments so far: {len(completed)}")
    else:
        lines.append("- No increment data yet.")

    if summary["wallclock"]:
        wc = summary["wallclock"]
        lines.append(f"- Wall clock: {wc:.0f}s ({wc/60:.1f} min)")
    if summary["cpu"]:
        lines.append(f"- CPU time: {summary['cpu']:.0f}s")

    lines.append("\n## Errors & Warnings")
    if errors_warnings:
        for ew in errors_warnings:
            lines.append(f"- {ew}")
    else:
        lines.append("- None recorded yet.")

    if summary["errors"] is not None:
        lines.append(f"\n**Total errors: {summary['errors']}  |  "
                     f"Warnings: {summary['warnings']}**")

    lines.append("\n## Run Configuration (fixes applied this run)")
    lines.append("| Parameter | Previous | Current |")
    lines.append("|-----------|----------|---------|")
    lines.append("| Min increment | 0.02 mm | 0.001 mm |")
    lines.append("| Initial increment | 0.5 mm | 0.1 mm |")
    lines.append("| Contact STABILIZE | 0.0002 | 0.001 |")
    lines.append("| Contact type | LINEAR (50 N/mm³) | EXPONENTIAL (c0=0.1mm, p0=0) |")
    lines.append("| Threads | 4 | 4 |")
    lines.append("\n**Root cause of previous failure:** "
                 "Contact penetration oscillation at coil-binding transition in Step 2 "
                 "(node 77533, SPRING_SURF self-contact). "
                 "LINEAR penalty caused abrupt contact stiffness changes driving "
                 "displacement corrections beyond increment tolerance (16 iterations, no convergence). "
                 "Fix: EXPONENTIAL pressure-overclosure (c0=0.1mm) provides smooth continuous "
                 "contact stiffness, avoiding the chattering that caused the minimum increment violation.")

    lines.append("\n## Raw .sta tail")
    lines.append("```")
    lines.append(sta_text.strip())
    lines.append("```")

    lines.append("\n## Recent .msg output")
    lines.append("```")
    lines.append(msg_text.strip())
    lines.append("```")

    with open(LOG, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[{now}] Log updated — status: {status}")
    if last:
        print(f"  Step {last['step']} Inc {last['inc']} Att {last['att']}  "
              f"time={last['total_time']:.3f}  inc={last['inc_size']:.5f}")

if __name__ == "__main__":
    main()
