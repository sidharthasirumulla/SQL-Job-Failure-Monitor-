# Runbook: SQL Job Failure

1. **Acknowledge** the alert and note the time (SLA clock starts).
2. **Identify** the job, criticality and error: run `python monitor.py`.
3. **Classify** the error (Database / Network / Data quality / Access / Infra).
4. **Fix or retry** using the suggested action. Never re-run a HIGH job twice without checking for duplicate loads.
5. **Escalate** to L2/vendor if: 3 consecutive failures, HIGH job down > 30 min, or category is Unknown.
6. **Communicate**: update the ticket and notify the business owner for HIGH jobs.
7. **Document** root cause and add the error to `KNOWLEDGE_BASE` in `monitor.py`.
