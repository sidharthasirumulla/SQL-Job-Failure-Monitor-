"""Generate a realistic fake job-run history into SQLite (no external libs)."""
import random, sqlite3
from datetime import datetime, timedelta

random.seed(42)
JOBS = [
    ("Nightly_Sales_ETL", "Data", "02:00 daily", "HIGH"),
    ("Customer_Sync", "CRM", "every 1h", "HIGH"),
    ("Invoice_Report", "Finance", "06:00 daily", "MEDIUM"),
    ("Inventory_Refresh", "Supply", "every 4h", "MEDIUM"),
    ("Archive_Old_Logs", "Infra", "Sun 01:00", "LOW"),
    ("Email_Digest", "Marketing", "08:00 daily", "LOW"),
]
ERRORS = [
    "ORA-01555: snapshot too old",
    "Deadlock detected on table SALES_FACT",
    "Connection timeout to source DB",
    "Duplicate key violation on CUSTOMER_ID",
    "Disk space low on /data/stage",
    "Permission denied: stage_user cannot SELECT INVENTORY",
    "Null value in NOT NULL column ORDER_DATE",
]

def main(db="job_monitor.db"):
    con = sqlite3.connect(db)
    con.executescript(open("sql/schema.sql").read())
    con.executemany("INSERT INTO jobs(job_name,owner_team,schedule,criticality) VALUES (?,?,?,?)", JOBS)
    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    rows = []
    for job_id, (_, _, _, crit) in enumerate(JOBS, start=1):
        base = random.randint(3, 25)
        flaky = 0.22 if job_id in (1, 3) else 0.05
        for h in range(7 * 24, 0, -6):
            start = now - timedelta(hours=h)
            dur = max(1, int(random.gauss(base, base * 0.2)))
            failed = random.random() < flaky
            # force a recent streak on job 1 so the escalation rule fires
            if job_id == 1 and h <= 18:
                failed = True
            if failed:
                rows.append((job_id, start.isoformat(" "), (start + timedelta(minutes=2)).isoformat(" "),
                             "FAILED", random.choice(ERRORS)))
            else:
                if random.random() < 0.03:
                    dur *= 4  # occasional slow run
                rows.append((job_id, start.isoformat(" "), (start + timedelta(minutes=dur)).isoformat(" "),
                             "SUCCESS", None))
    con.executemany("INSERT INTO job_runs(job_id,start_time,end_time,status,error_message) VALUES (?,?,?,?,?)", rows)
    con.commit(); con.close()
    print(f"Created {db} with {len(JOBS)} jobs and {len(rows)} runs")

if __name__ == "__main__":
    main()
