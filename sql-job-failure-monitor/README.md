# SQL Job Failure Monitor (Beginner)

An application-support style tool that **monitors scheduled SQL jobs, debugs failures, and produces a daily report**.
Built to mirror real L1/L2 support work: monitoring, root-cause classification, escalation rules and runbooks.

## Skills shown
SQL (joins, aggregates, window functions, CTEs) | Python (sqlite3) | Incident triage | Documentation

## Run it
```bash
python generate_data.py      # creates job_monitor.db with 7 days of fake job history
python monitor.py            # prints and saves reports/daily_report.md
sqlite3 job_monitor.db < sql/diagnostic_queries.sql   # optional manual diagnostics
```
Requires only Python 3.8+ (no installs).

## What's inside
| File | Purpose |
|---|---|
| `sql/schema.sql` | Jobs and job_runs tables |
| `generate_data.py` | Creates realistic failures and slow runs |
| `sql/diagnostic_queries.sql` | 4 queries support engineers use daily |
| `monitor.py` | Daily report with root-cause category + fix suggestion + escalation |
| `docs/runbook.md` | Step-by-step response procedure |

## Ideas to extend
Email the report via SMTP, add a Power BI dashboard on `job_runs`, add more error patterns.
