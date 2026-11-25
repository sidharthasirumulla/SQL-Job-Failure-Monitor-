# Daily Job Health Report - 2026-11-25 07:30

**Failures in last 24h:** 4

## Failures (highest criticality first)

| Job | Priority | Time | Category | Suggested action |
|---|---|---|---|---|
| Nightly_Sales_ETL | HIGH | 2026-11-25 01:00:00 | Concurrency | Re-run after blocking session ends; check overlapping schedules. |
| Nightly_Sales_ETL | HIGH | 2026-11-24 19:00:00 | Data quality | Dedupe source rows or add MERGE/UPSERT logic. |
| Customer_Sync | HIGH | 2026-11-24 19:00:00 | Access | Raise access request to DBA for the service account. |
| Nightly_Sales_ETL | HIGH | 2026-11-24 13:00:00 | Concurrency | Re-run after blocking session ends; check overlapping schedules. |

## Escalate (3 consecutive failures)

- Nightly_Sales_ETL

## 7-day failure summary

| Job | Runs | Failures |
|---|---|---|
| Nightly_Sales_ETL | 28 | 11 |
| Invoice_Report | 28 | 8 |
| Email_Digest | 28 | 2 |
| Inventory_Refresh | 28 | 1 |
| Customer_Sync | 28 | 1 |
| Archive_Old_Logs | 28 | 0 |