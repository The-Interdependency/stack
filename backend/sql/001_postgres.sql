-- Durable stack orchestration state. PostgreSQL 14+.
-- Repositories own canon and artifacts; this database owns orchestration state only.

CREATE TABLE IF NOT EXISTS schema_migrations (
    version text PRIMARY KEY,
    applied_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS jobs (
    id text PRIMARY KEY,
    dedupe_key text NOT NULL UNIQUE CHECK (dedupe_key ~ '^[0-9a-f]{64}$'),
    kind text NOT NULL,
    target text NOT NULL CHECK (target ~ '^[A-Za-z0-9][A-Za-z0-9._-]*$'),
    source_sha text NOT NULL CHECK (source_sha ~ '^[0-9a-f]{40}$'),
    generator_identity text NOT NULL CHECK (generator_identity ~ '^[0-9a-f]{64}$'),
    executor text NOT NULL CHECK (executor IN ('local', 'github-actions')),
    state text NOT NULL CHECK (
        state IN ('queued','running','succeeded','failed','hmmm','cancelled')
    ),
    attempts integer NOT NULL DEFAULT 0 CHECK (attempts >= 0),
    payload_json jsonb NOT NULL,
    created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    artifact_path text,
    artifact_sha256 text CHECK (
        artifact_sha256 IS NULL OR artifact_sha256 ~ '^[0-9a-f]{64}$'
    ),
    error text,
    hmmm text,
    lease_owner text,
    lease_until timestamptz,
    CHECK (
        (lease_owner IS NULL AND lease_until IS NULL)
        OR (state = 'running' AND lease_owner IS NOT NULL AND lease_until IS NOT NULL)
    )
);

CREATE INDEX IF NOT EXISTS jobs_queue
ON jobs (created_at, id)
WHERE state = 'queued';

CREATE INDEX IF NOT EXISTS jobs_lease_expiry
ON jobs (lease_until)
WHERE state = 'running' AND lease_until IS NOT NULL;

CREATE TABLE IF NOT EXISTS attempts (
    id text PRIMARY KEY,
    job_id text NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    executor text NOT NULL CHECK (executor IN ('local', 'github-actions')),
    worker_id text NOT NULL,
    state text NOT NULL CHECK (
        state IN ('running','succeeded','failed','hmmm','cancelled')
    ),
    started_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    finished_at timestamptz,
    error text
);

CREATE UNIQUE INDEX IF NOT EXISTS attempts_one_running_per_job
ON attempts (job_id)
WHERE state = 'running';

CREATE INDEX IF NOT EXISTS attempts_by_job
ON attempts (job_id, started_at DESC);

CREATE TABLE IF NOT EXISTS receipts (
    job_id text PRIMARY KEY REFERENCES jobs(id) ON DELETE CASCADE,
    source_sha text NOT NULL CHECK (source_sha ~ '^[0-9a-f]{40}$'),
    generator_identity text NOT NULL CHECK (generator_identity ~ '^[0-9a-f]{64}$'),
    artifact_path text NOT NULL,
    artifact_sha256 text NOT NULL CHECK (artifact_sha256 ~ '^[0-9a-f]{64}$'),
    verified_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS job_dependencies (
    job_id text NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    depends_on_job_id text NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    required_state text NOT NULL DEFAULT 'succeeded' CHECK (required_state = 'succeeded'),
    PRIMARY KEY (job_id, depends_on_job_id),
    CHECK (job_id <> depends_on_job_id)
);

CREATE TABLE IF NOT EXISTS hmmm (
    id text PRIMARY KEY,
    job_id text NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    constraint text NOT NULL,
    observed_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at timestamptz,
    resolution text
);

CREATE INDEX IF NOT EXISTS hmmm_open
ON hmmm (observed_at DESC)
WHERE resolved_at IS NULL;

INSERT INTO schema_migrations(version)
VALUES ('001_postgres')
ON CONFLICT (version) DO NOTHING;
