"""Daily SQL job health report: finds failures, classifies root cause, suggests fixes, flags escalations."""
import sqlite3, sys
from datetime import datetime

# Keyword -> (category, first-line fix). Extend this table as you learn new errors.
KNOWLEDGE_BASE = {
    "snapshot too old": ("Database", "Increase UNDO retention or run job off-peak; re-run."),
    "deadlock": ("Concurrency", "Re-run after blocking session ends; check overlapping schedules."),
    "timeout": ("Network", "Check source DB / VPN connectivity, then re-run."),
    "duplicate key": ("Data quality", "Dedupe source rows or add MERGE/UPSERT logic."),
    "disk space": ("Infrastructure", "Clear staging area, request more disk from infra team."),
    "permission denied": ("Access", "Raise access request to DBA for the service account."),
    "null value": ("Data quality", "Fix upstream feed or add COALESCE default."),
}

def classify(msg):
    low = (msg or "").lower()
    for key, (cat, fix) in KNOWLEDGE_BASE.items():
        if key in low:
            return cat, fix
    return "Unknown", "Escalate to L2 with full log."

def main(db="job_monitor.db", out="reports/daily_report.md"):
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    fails = con.execute("""
        SELECT j.job_name, j.criticality, r.start_time, r.error_message
        FROM job_runs r JOIN jobs j USING(job_id)
        WHERE r.status='FAILED' AND r.start_time >= datetime('now','localtime','-1 day')
        ORDER BY CASE j.criticality WHEN 'HIGH' THEN 1 WHEN 'MEDIUM' THEN 2 ELSE 3 END, r.start_time DESC
    """).fetchall()
    streaks = con.execute("""
        WITH ranked AS (SELECT job_id,status,ROW_NUMBER() OVER (PARTITION BY job_id ORDER BY start_time DESC) rn FROM job_runs)
        SELECT j.job_name FROM ranked JOIN jobs j USING(job_id)
        WHERE rn<=3 AND status='FAILED' GROUP BY j.job_name HAVING COUNT(*)=3
    """).fetchall()
    rate = con.execute("""
        SELECT j.job_name, COUNT(*) runs, SUM(r.status='FAILED') failures
        FROM job_runs r JOIN jobs j USING(job_id) GROUP BY j.job_name ORDER BY failures DESC
    """).fetchall()

    lines = [f"# Daily Job Health Report - {datetime.now():%Y-%m-%d %H:%M}", "",
             f"**Failures in last 24h:** {len(fails)}", ""]
    lines += ["## Failures (highest criticality first)", "",
              "| Job | Priority | Time | Category | Suggested action |", "|---|---|---|---|---|"]
    for f in fails:
        cat, fix = classify(f["error_message"])
        lines.append(f"| {f['job_name']} | {f['criticality']} | {f['start_time']} | {cat} | {fix} |")
    lines += ["", "## Escalate (3 consecutive failures)", ""]
    lines += [f"- {s['job_name']}" for s in streaks] or ["- None"]
    lines += ["", "## 7-day failure summary", "", "| Job | Runs | Failures |", "|---|---|---|"]
    lines += [f"| {r['job_name']} | {r['runs']} | {r['failures']} |" for r in rate]
    text = "\n".join(lines)
    open(out, "w").write(text)
    print(text)

if __name__ == "__main__":
    main(*sys.argv[1:])
