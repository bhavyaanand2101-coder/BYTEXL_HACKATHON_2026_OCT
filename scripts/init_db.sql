-- Initialize assistant_ro role with SELECT only grants for advisor assistant endpoint
DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'assistant_ro') THEN
      CREATE ROLE assistant_ro WITH LOGIN PASSWORD 'assistant_ro_secret';
   END IF;
END
$$;

GRANT CONNECT ON DATABASE campuspulse_db TO assistant_ro;
GRANT USAGE ON SCHEMA public TO assistant_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO assistant_ro;
