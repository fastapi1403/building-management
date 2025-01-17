Drop all tables:
```sql
DROP TABLE IF EXISTS buildings CASCADE;
DROP TABLE IF EXISTS charges CASCADE;
DROP TABLE IF EXISTS cost_documents CASCADE;
DROP TABLE IF EXISTS costs CASCADE;
DROP TABLE IF EXISTS floors CASCADE;
DROP TABLE IF EXISTS fund_transactions CASCADE;
DROP TABLE IF EXISTS funds CASCADE;
DROP TABLE IF EXISTS owners CASCADE;
DROP TABLE IF EXISTS payments CASCADE;
DROP TABLE IF EXISTS tenants CASCADE;
DROP TABLE IF EXISTS units CASCADE;
DROP TABLE IF EXISTS alembic_version;
```

Drop ALL tables and ALL types:
```sql
DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
END $$;

DO $$ DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT typname FROM pg_type WHERE typnamespace = (SELECT oid FROM pg_namespace WHERE nspname = current_schema())) LOOP
        EXECUTE 'DROP TYPE IF EXISTS ' || quote_ident(r.typname) || ' CASCADE';
    END LOOP;
END $$;
```