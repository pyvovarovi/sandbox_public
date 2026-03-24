# dbt Integrity Checks for Snowflake

Dynamically discovers every table across configurable Snowflake schemas, reads their
declared integrity constraints from `INFORMATION_SCHEMA`, and validates them at query
time — surfacing **NOT NULL**, **UNIQUE**, **PRIMARY KEY**, and **FOREIGN KEY** violations.

> **Why?** Snowflake declares but does **not enforce** most constraints (PK, UNIQUE, FK).
> This project catches violations that silently accumulate in your warehouse.

---

## Project Structure

```
dbt_integrity_checks/
├── dbt_project.yml                          # schema_list + target_database config
├── profiles.yml                             # Snowflake connection (copy to ~/.dbt/)
├── packages.yml                             # dbt_utils dependency
│
├── macros/
│   ├── get_tables_in_schema.sql             # Discover tables per schema
│   ├── get_table_constraints.sql            # Discover constraints per table
│   ├── validate_all_constraints.sql         # CLI orchestrator (run-operation)
│   └── generate_schema_yml.sql              # Auto-generate sources + tests YAML
│
├── models/staging/
│   ├── constraint_violation_report.sql      # Materialised violation table
│   └── schema.yml                           # Model documentation
│
└── tests/generic/
    └── integrity_tests.sql                  # composite_unique & referential_integrity
```

---

## Quick Start

### 1. Configure Connection

```bash
# Set environment variables
export SNOWFLAKE_ACCOUNT='xy12345.us-east-1'
export SNOWFLAKE_USER='my_user'
export SNOWFLAKE_PASSWORD='my_password'
export SNOWFLAKE_ROLE='TRANSFORMER'
export SNOWFLAKE_DATABASE='ANALYTICS'
export SNOWFLAKE_WAREHOUSE='TRANSFORM_WH'

# Copy profile
cp profiles.yml ~/.dbt/profiles.yml
```

### 2. Configure Schemas

Edit `dbt_project.yml`:

```yaml
vars:
  target_database: 'ANALYTICS'
  schema_list:
    - 'PUBLIC'
    - 'RAW'
    - 'STAGING'
```

### 3. Install Dependencies

```bash
dbt deps
```

### 4. Run Validation

You have **three** ways to validate:

#### Option A — Interactive CLI Report (recommended for ad-hoc checks)

```bash
dbt run-operation validate_all_constraints
```

Prints a tree-formatted report to the console:

```
═══════════════════════════════════════════════════════════
  INTEGRITY CONSTRAINT VALIDATION
  Database : ANALYTICS
  Schemas  : PUBLIC, RAW, STAGING
═══════════════════════════════════════════════════════════

┌─ SCHEMA: RAW
│
├── TABLE: RAW.ORDERS
│   ├─ ✓ PRIMARY KEY on [ORDER_ID]
│   ├─ ✓ NOT NULL on [ORDER_ID]
│   ├─ ✗ FOREIGN KEY [CUSTOMER_ID] → RAW.CUSTOMERS [ID] — 12 orphan rows
│   ├─ ✓ NOT NULL on [ORDER_DATE]
│
├── TABLE: RAW.CUSTOMERS
│   ├─ ✓ PRIMARY KEY on [ID]
│   ├─ ✓ UNIQUE on [EMAIL]

  SUMMARY
  ❌ VIOLATIONS FOUND: 1 constraint(s) failed
  • RAW.ORDERS | FOREIGN KEY on [CUSTOMER_ID] — 12 violations
═══════════════════════════════════════════════════════════
```

#### Option B — Materialised Violation Table (recommended for dashboards/alerts)

```bash
dbt run --select constraint_violation_report
```

Creates table `AUDIT.CONSTRAINT_VIOLATION_REPORT` with one row per violated constraint.
Query it in Snowflake, connect to your BI tool, or set up Snowflake alerts.

#### Option C — Auto-Generated dbt Tests (recommended for CI/CD)

```bash
# Generate the YAML
dbt run-operation generate_schema_yml > models/staging/sources.yml

# Run as standard dbt tests
dbt test --select source:*
```

---

## Constraint Types Validated

| Type | What It Checks | How |
|------|---------------|-----|
| **NOT NULL** | No NULL values in the column | `WHERE col IS NULL` |
| **UNIQUE** | No duplicate values (single or composite) | `GROUP BY ... HAVING COUNT(*) > 1` |
| **PRIMARY KEY** | No NULLs **and** no duplicates in PK columns | Both checks combined |
| **FOREIGN KEY** | Every child row has a matching parent | `NOT EXISTS` anti-join |
| **CHECK** | Logged as informational | Snowflake enforces at DML time |

---

## Scheduling

Add to your dbt Cloud job or cron:

```bash
# Nightly integrity scan
dbt run --select constraint_violation_report
```

Or in Airflow / Dagster / Prefect, call the `run-operation` variant and parse output.

---

## Requirements

- **dbt-core** ≥ 1.5
- **dbt-snowflake** ≥ 1.5
- Snowflake role must have `USAGE` on target database/schemas and `SELECT` on
  `INFORMATION_SCHEMA` views.
