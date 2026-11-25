-- Simulated scheduler/ETL job tables (SQLite)
DROP TABLE IF EXISTS job_runs;
DROP TABLE IF EXISTS jobs;
CREATE TABLE jobs (
    job_id      INTEGER PRIMARY KEY,
    job_name    TEXT NOT NULL,
    owner_team  TEXT NOT NULL,
    schedule    TEXT NOT NULL,
    criticality TEXT CHECK (criticality IN ('HIGH','MEDIUM','LOW'))
);
CREATE TABLE job_runs (
    run_id        INTEGER PRIMARY KEY,
    job_id        INTEGER NOT NULL REFERENCES jobs(job_id),
    start_time    TEXT NOT NULL,
    end_time      TEXT,
    status        TEXT CHECK (status IN ('SUCCESS','FAILED','RUNNING')),
    error_message TEXT
);
