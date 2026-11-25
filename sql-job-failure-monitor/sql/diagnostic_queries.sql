-- 1. Failures in the last 24h with job details
SELECT j.job_name, j.criticality, r.start_time, r.error_message
FROM job_runs r JOIN jobs j USING (job_id)
WHERE r.status = 'FAILED' AND r.start_time >= datetime('now','localtime','-1 day')
ORDER BY j.criticality, r.start_time DESC;

-- 2. Failure rate per job (find flaky jobs)
SELECT j.job_name,
       COUNT(*) AS runs,
       SUM(r.status='FAILED') AS failures,
       ROUND(100.0*SUM(r.status='FAILED')/COUNT(*),1) AS fail_pct
FROM job_runs r JOIN jobs j USING (job_id)
GROUP BY j.job_name HAVING failures > 0 ORDER BY fail_pct DESC;

-- 3. Jobs that failed 3 times in a row (needs escalation) - window function
WITH ranked AS (
  SELECT job_id, status,
         ROW_NUMBER() OVER (PARTITION BY job_id ORDER BY start_time DESC) AS rn
  FROM job_runs)
SELECT j.job_name, COUNT(*) AS consecutive_failures
FROM ranked JOIN jobs j USING (job_id)
WHERE rn <= 3 AND status='FAILED'
GROUP BY j.job_name HAVING COUNT(*) = 3;

-- 4. Long-running jobs (> 2x their own average duration)
WITH d AS (
  SELECT run_id, job_id,
         (julianday(end_time)-julianday(start_time))*1440 AS mins
  FROM job_runs WHERE end_time IS NOT NULL)
SELECT j.job_name, ROUND(d.mins,1) AS mins, ROUND(a.avg_mins,1) AS avg_mins
FROM d JOIN (SELECT job_id, AVG(mins) avg_mins FROM d GROUP BY job_id) a USING (job_id)
JOIN jobs j USING (job_id)
WHERE d.mins > 2*a.avg_mins ORDER BY d.mins DESC;
