-- Single durable PostgreSQL state boundary for stack fresh-making.
-- Repository canon and generated artifacts remain outside SQL authority.

CREATE TABLE IF NOT EXISTS schema_migrations (
    version text PRIMARY KEY,
    applied_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS derivations (
    target text PRIMARY KEY CHECK (target ~ '^[A-Za-z0-9][A-Za-z0-9._:-]*$'),
    kind text NOT NULL,
    freshness_key text NOT NULL CHECK (freshness_key ~ '^[0-9a-f]{64}$'),
    spec_json jsonb NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS derivation_dependencies (
    target text NOT NULL REFERENCES derivations(target) ON DELETE CASCADE,
    depends_on_target text NOT NULL,
    PRIMARY KEY (target, depends_on_target),
    CHECK (target <> depends_on_target)
);

CREATE TABLE IF NOT EXISTS jobs (
    id text PRIMARY KEY,
    dedupe_key text NOT NULL UNIQUE CHECK (dedupe_key ~ '^[0-9a-f]{64}$'),
    kind text NOT NULL,
    target text NOT NULL CHECK (target ~ '^[A-Za-z0-9][A-Za-z0-9._:-]*$'),
    freshness_key text NOT NULL CHECK (freshness_key ~ '^[0-9a-f]{64}$'),
    preferred_executor text NOT NULL CHECK (preferred_executor IN ('local','github-actions')),
    state text NOT NULL CHECK (
        state IN ('queued','leased','running','verifying','succeeded','failed','hmmm','cancelled')
    ),
    attempts integer NOT NULL DEFAULT 0 CHECK (attempts >= 0),
    payload_json jsonb NOT NULL,
    created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    lease_owner text,
    lease_until timestamptz,
    active_attempt_id text,
    receipt_id text,
    error text,
    hmmm text,
    CHECK (
        (state IN ('leased','running','verifying') AND lease_owner IS NOT NULL AND lease_until IS NOT NULL AND active_attempt_id IS NOT NULL)
        OR
        (state NOT IN ('leased','running','verifying') AND lease_owner IS NULL AND lease_until IS NULL AND active_attempt_id IS NULL)
    )
);

CREATE INDEX IF NOT EXISTS jobs_queue ON jobs(created_at,id) WHERE state='queued';
CREATE INDEX IF NOT EXISTS jobs_target ON jobs(target,created_at DESC);
CREATE UNIQUE INDEX IF NOT EXISTS jobs_one_active_per_target
ON jobs(target) WHERE state IN ('queued','leased','running','verifying');
CREATE INDEX IF NOT EXISTS jobs_lease_expiry ON jobs(lease_until) WHERE state IN ('leased','running','verifying');

CREATE TABLE IF NOT EXISTS attempts (
    id text PRIMARY KEY,
    job_id text NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    ordinal integer NOT NULL CHECK (ordinal > 0),
    executor text NOT NULL CHECK (executor IN ('local','github-actions')),
    worker_id text NOT NULL,
    state text NOT NULL CHECK (state IN ('leased','running','verifying','succeeded','failed','hmmm','cancelled')),
    created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started_at timestamptz,
    finished_at timestamptz,
    error text,
    hmmm text,
    UNIQUE(job_id, ordinal)
);

CREATE UNIQUE INDEX IF NOT EXISTS attempts_one_active_per_job
ON attempts(job_id) WHERE state IN ('leased','running','verifying');

CREATE TABLE IF NOT EXISTS receipts (
    id text PRIMARY KEY,
    job_id text NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    target text NOT NULL,
    freshness_key text NOT NULL CHECK (freshness_key ~ '^[0-9a-f]{64}$'),
    attempt_id text NOT NULL REFERENCES attempts(id),
    output_path text NOT NULL,
    output_sha256 text NOT NULL CHECK (output_sha256 ~ '^[0-9a-f]{64}$'),
    receipt_json jsonb NOT NULL,
    verified_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS receipts_target_key ON receipts(target,freshness_key,verified_at DESC);

CREATE TABLE IF NOT EXISTS target_acceptance (
    target text PRIMARY KEY,
    freshness_key text NOT NULL CHECK (freshness_key ~ '^[0-9a-f]{64}$'),
    receipt_id text NOT NULL REFERENCES receipts(id),
    accepted_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS hmmm (
    id text PRIMARY KEY,
    target text,
    job_id text REFERENCES jobs(id) ON DELETE CASCADE,
    constraint text NOT NULL,
    observed_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at timestamptz,
    resolution text
);

CREATE INDEX IF NOT EXISTS hmmm_open ON hmmm(observed_at DESC) WHERE resolved_at IS NULL;

INSERT INTO schema_migrations(version) VALUES ('001_postgres_fresh_making')
ON CONFLICT(version) DO NOTHING;
