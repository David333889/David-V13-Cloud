-- DAVID V14 - Supabase Schema Migration V1
-- Contract: V14_SUPABASE_SCHEMA_MIGRATION_V1
-- Target: public.stock_history
--
-- Purpose:
-- Add V14 Persistence Version / Safety columns.
--
-- Safety:
-- - additive only
-- - idempotent via IF NOT EXISTS
-- - no DROP
-- - no DELETE
-- - no TRUNCATE
-- - no existing column modification
-- - no data backfill in this migration
--
-- Legacy rows remain compatible because new columns are nullable.

alter table public.stock_history
    add column if not exists payload_version text,
    add column if not exists engine_version text,
    add column if not exists baseline_version text,

    add column if not exists risk_state text,
    add column if not exists risk_level text,
    add column if not exists risk_lock boolean,

    add column if not exists action_state text,
    add column if not exists action_signal text,
    add column if not exists action_reason text,
    add column if not exists action_risk_guard text,
    add column if not exists action_confidence text,

    add column if not exists consumer_state text;