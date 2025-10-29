# Salesforce integration overview

**User:** Igor Pyvovarov (pyvovarov.igor@gmail.com)  
**Created:** 8/12/2025 10:19:12  
**Updated:** 10/28/2025 19:50:03  
**Exported:** 10/28/2025 16:50:28  
**Link:** [https://chatgpt.com/c/689b4d39-f500-832c-8765-b9a7acdf6aaf](https://chatgpt.com/c/689b4d39-f500-832c-8765-b9a7acdf6aaf)  

## Prompt:
Sailforse integration information, database, schema, access

## Response:
Thought for 19s

Got it — here’s a compact, practitioner-friendly overview of Salesforce (I’ll assume “Sailforse” = Salesforce) integration focused on database, schema, and access.

Integration patterns (how to get data in/out)
=============================================

*   **API-ETL to your DB (most common):** Use Bulk/REST APIs via tools like Fivetran, Airbyte, Stitch, Hevo, Matillion, dbt Cloud + custom code, etc. Pros: reliable, incremental, managed schema drift. Cons: license cost/limits.
*   **DIY pipelines:** Python/Java + Bulk API v2 (ingest/query), orchestrated by Airflow/Prefect. Pros: control/cost. Cons: you own retries, backoff, schema drift.
*   **Change Data Capture (CDC):** Subscribe to **Change Data Capture** or **Platform Events** via Pub/Sub (gRPC) or Streaming API to capture near-real-time changes; land to Kafka, then into your warehouse.
*   **Salesforce Connect (virtual tables):** Live link external DBs into Salesforce (read-through). Good for read-heavy, not for full replication.
*   **Heroku Connect / MuleSoft:** Bi-directional sync to Postgres or enterprise integration orchestration.
*   **Data Cloud (CDP):** For identity resolution + activation use cases (separate product, not just ELT).

Access methods (APIs you’ll actually use)
=========================================

*   **OAuth 2.0** with a **Connected App** (JWT Bearer or Web Server flow). Scope typically: `api refresh_token`.
*   **Bulk API v2** (CSV/JSON; async; best for >10k records): upsert with external IDs, chunked loads.
*   **REST API** (JSON; good for point lookups, small writes) and **Composite** (bundle multiple calls).
*   **SOAP API** (legacy but still everywhere; some metadata ops).
*   **SOQL** (query language) + **SOSL** (search).
*   **Pub/Sub API** (gRPC) or **Streaming API** (CometD) for CDC, Platform Events.
*   **Metadata API / Tooling API** for schema discovery (objects, fields, picklists, layouts).

Security & governance you must plan for
=======================================

*   **Profiles & Permission Sets** control field/object access; **Field-Level Security** affects API visibility.
*   **IP relaxations** for the Connected App, **OAuth policies**, **Named Credentials** for outbound calls.
*   **Row-level sharing** may filter API results (respect “with sharing” scenarios).
*   **Shield Platform Encryption** may encrypt fields (affects search/filters).

Salesforce schema model (what you’ll see)
=========================================

*   **Standard objects:** `Account`, `Contact`, `Lead`, `Opportunity`, `Case`, `User`, `Task`, `Event`, `Product2`, etc.
*   **Custom objects:** suffixed `__c` (e.g., `Invoice__c`). Custom fields end with `__c`.
*   **IDs:** 18-character, case-insensitive. Use them as stable PKs.
*   **Timestamps:** `SystemModstamp` (for incrementals), `CreatedDate`, `LastModifiedDate`.
*   **Soft delete:** `IsDeleted = true` means in Recycle Bin; still visible via some APIs.
*   **Picklists & multi-select picklists:** text values; multi-select are semicolon-delimited (`;`).
*   **Lookups & master-detail:** foreign keys like `AccountId`; many-to-many via **junction objects**.
*   **Polymorphic lookups:** `WhoId` (Lead/Contact), `WhatId` (many types) in `Task/Event`.
*   **Activities:** `Task`, `Event`, and `ActivityHistory` nuances.
*   **Attachments/Files:** Newer **ContentVersion/ContentDocument** replaces legacy `Attachment`.

Typical warehouse landing design
================================

**Schema layout (example for Snowflake/Postgres/BigQuery):**

*   One **schema per source**: e.g., `SALESFORCE`.
*   One **table per object**: e.g., `SALESFORCE.ACCOUNT`, `SALESFORCE.CONTACT`, `SALESFORCE.OPPORTUNITY`, `SALESFORCE.OPPORTUNITYLINEITEM`, `SALESFORCE.USER`, `SALESFORCE.TASK`, `SALESFORCE.CASE`, `SALESFORCE.CONTENTVERSION`, custom `*_C`.
*   Include:
    *   `ID` (PK), `ISDELETED`, `CREATEDDATE`, `LASTMODIFIEDDATE`, **`SYSTEMMODSTAMP`**,
    *   All business fields (nullable; picklists as text),
    *   FKs: `ACCOUNTID`, `OWNERID`, etc.

**Incremental loads:**

*   Pull changed rows where `SystemModstamp > :last_max`.
*   Upsert by `Id`. If `IsDeleted=true`, **soft-delete** in warehouse (flag or move to `_DELETED` table).
*   Snapshot slowly changing elements (optional SCD2) where business logic needs history.

**Constraints & types:**

*   Store `Id` as **VARCHAR(18)**.
*   Datetimes as UTC. Numeric currency fields as DECIMAL. Multi-select picklists kept as STRING plus a **helper split table** if you need relational joins.
*   Create **surrogate keys** only for marts; keep raw as close to source as possible.

Example: minimal SOQL and upsert flow
=====================================

**Query incrementally (SOQL):**

```soql
SELECT Id, Name, AccountNumber, Industry, OwnerId, SystemModstamp, IsDeleted
FROM Account
WHERE SystemModstamp > 2025-08-10T00:00:00Z
ORDER BY SystemModstamp
```

**Warehouse DDL (Postgres-ish):**

```sql
CREATE TABLE salesforce.account_raw (
  id              varchar(18) PRIMARY KEY,
  name            text,
  accountnumber   text,
  industry        text,
  ownerid         varchar(18),
  systemmodstamp  timestamp with time zone NOT NULL,
  createddate     timestamp with time zone,
  lastmodifieddate timestamp with time zone,
  isdeleted       boolean default false
);
CREATE INDEX ON salesforce.account_raw (systemmodstamp);
```

**Bulk upsert strategy:**

1.  Extract to CSV/Parquet.
2.  Stage to object storage (S3/GCS/Azure).
3.  Use warehouse `COPY` into a **staging table**.
4.  `MERGE` into target by `Id`, set `isdeleted`, update changed fields.
5.  Record high-watermark = max(`systemmodstamp`) processed.

Handling schema drift (new fields / changed picklists)
======================================================

*   Poll **Metadata API** daily to detect new fields.
*   In managed ELT tools, enable **auto-add columns**.
*   Keep a **field dictionary** table (object, field, label, type, picklist values, is\_required).

API limits & performance tips
=============================

*   Respect **daily API limits** (varies by edition/users); use **Bulk API v2** for large pulls.
*   Page with `ORDER BY SystemModstamp` and `LIMIT`/`OFFSET` or server-side chunking tokens.
*   For writes, prefer **External IDs** to avoid lookups and enable idempotent upserts.
*   Use **Composite** to reduce chattiness for small transactional bundles.

Access setup checklist (admin + dev)
====================================

1.  Create a **Connected App**; enable OAuth flows; define callback.
2.  Configure **Policies** (IP relaxation as needed).
3.  Create **Integration User** with minimal **Profile** and **Permission Sets** for objects/fields.
4.  Generate and store **JWT cert** (for JWT flow) in your secret manager.
5.  Test with **Workbench** or **Postman**; verify FLS/record visibility.
6.  Stand up extraction in dev sandbox first; promote to production.

* * *

If you tell me your target database (Snowflake, Postgres, BigQuery, Databricks/Spark, etc.) and whether you prefer a managed connector or Python/Airflow, I can drop in a ready-to-run incremental pipeline template (including DDL, MERGE, and example Bulk API v2 code).

## Prompt:
Snowflake

## Response:
Thought for 21s

Awesome — here’s a Snowflake-focused starter kit for integrating **Salesforce → Snowflake** with clean schemas, secure access, and solid incrementals.

1) Architecture options (Snowflake-centric)
===========================================

*   **Managed ELT (fastest):** Fivetran / Airbyte / Matillion push Salesforce objects into Snowflake tables and auto-handle schema drift. You mostly model with dbt/Snowflake SQL.
*   **DIY ELT (most control):** Python pulls (Bulk API v2) → land files to S3/Azure/GCS → **Snowpipe**/**Snowpipe Streaming** → raw tables → `MERGE` to curated. (Templates below.)
*   **Near-real-time CDC:** Salesforce **Change Data Capture** → Kafka (or Pub/Sub API) → Snowpipe Streaming client → Snowflake. (Use this if you truly need sub-minute latency.)

2) Canonical Snowflake layout
=============================

*   **Databases:** `RAW_SFDC` (immutable raw), `CURATED_SFDC` (cleaned), `ANALYTICS` (marts).
*   **Schemas:** per domain, e.g., `CORE`, `SALES`, `SERVICE`.
*   **Tables:** one per object (`ACCOUNT`, `CONTACT`, `OPPORTUNITY`, `OPPORTUNITYLINEITEM`, `USER`, `TASK`, `CASE`, `CONTENTVERSION`, plus `*_C` for customs).
*   **Columns to always keep:**  
    `ID` (PK, VARCHAR(18)), `ISDELETED` (BOOLEAN), `SYSTEMMODSTAMP`, `CREATEDDATE`, `LASTMODIFIEDDATE`, business fields, and FKs like `ACCOUNTID`, `OWNERID`.  
    Multi-select picklists stay as `STRING`; optionally explode later.

3) Secure access & roles (RBAC)
===============================

```sql
-- One-time: roles & warehouses
CREATE ROLE IF NOT EXISTS SFDC_PIPE_ROLE;
CREATE ROLE IF NOT EXISTS SFDC_READ_ROLE;

GRANT ROLE SFDC_READ_ROLE TO ROLE SYSADMIN; -- or to your top-level role/users

CREATE WAREHOUSE IF NOT EXISTS WH_SFDC_PIPE
  WAREHOUSE_SIZE = XSMALL
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;

-- Databases
CREATE DATABASE IF NOT EXISTS RAW_SFDC;
CREATE DATABASE IF NOT EXISTS CURATED_SFDC;

GRANT USAGE ON DATABASE RAW_SFDC TO ROLE SFDC_READ_ROLE;
GRANT USAGE ON ALL SCHEMAS IN DATABASE RAW_SFDC TO ROLE SFDC_READ_ROLE;
GRANT SELECT ON FUTURE TABLES IN DATABASE RAW_SFDC TO ROLE SFDC_READ_ROLE;
```

4) Landing (S3 example) → Snowpipe
==================================

```sql
USE ROLE SECURITYADMIN;

-- Storage integration (IAM role on S3 with Snowflake external ID)
CREATE STORAGE INTEGRATION IF NOT EXISTS S3_SFDC_INT
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = S3
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::<account-id>:role/snowflake-s3-integration'
  COMMENT='For Salesforce raw drops';

-- File format (CSV or JSON depending on your extractor)
CREATE OR REPLACE FILE FORMAT RAW_SFDC.PUBLIC.CSVFF
  TYPE = CSV
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  NULL_IF = ('', 'NULL');

-- External stage pointing at your S3 prefix
CREATE OR REPLACE STAGE RAW_SFDC.PUBLIC.S3_SFDC_STAGE
  STORAGE_INTEGRATION = S3_SFDC_INT
  URL = 's3://<bucket>/salesforce/'
  FILE_FORMAT = RAW_SFDC.PUBLIC.CSVFF;

-- Raw table example (Account)
CREATE OR REPLACE TABLE RAW_SFDC.CORE.ACCOUNT_RAW (
  ID STRING, NAME STRING, ACCOUNTNUMBER STRING, INDUSTRY STRING,
  OWNERID STRING, ISDELETED BOOLEAN, SYSTEMMODSTAMP TIMESTAMP_TZ,
  CREATEDDATE TIMESTAMP_TZ, LASTMODIFIEDDATE TIMESTAMP_TZ,
  _INGESTED_AT TIMESTAMP_TZ DEFAULT CURRENT_TIMESTAMP()
);

-- Snowpipe (auto-ingest with S3 event notifications recommended)
CREATE OR REPLACE PIPE RAW_SFDC.CORE.ACCOUNT_PIPE
  AS COPY INTO RAW_SFDC.CORE.ACCOUNT_RAW
     FROM @RAW_SFDC.PUBLIC.S3_SFDC_STAGE/account/
     ON_ERROR = 'CONTINUE';
```

> If you need sub-minute latency without S3, consider **Snowpipe Streaming** (client SDK pushes rows directly to table; no stage required).

5) Curated merge (incrementals, soft delete)
============================================

```sql
-- Curated table mirrors source but clean types & naming
CREATE OR REPLACE TABLE CURATED_SFDC.CORE.ACCOUNT (
  ID STRING PRIMARY KEY,
  NAME STRING,
  ACCOUNTNUMBER STRING,
  INDUSTRY STRING,
  OWNERID STRING,
  ISDELETED BOOLEAN,
  SYSTEMMODSTAMP TIMESTAMP_TZ,
  CREATEDDATE TIMESTAMP_TZ,
  LASTMODIFIEDDATE TIMESTAMP_TZ,
  RECORD_LAST_SEEN TIMESTAMP_TZ
);

-- Merge by Id; upsert changes and reflect deletes
MERGE INTO CURATED_SFDC.CORE.ACCOUNT T
USING (
  SELECT *
  FROM RAW_SFDC.CORE.ACCOUNT_RAW
  QUALIFY ROW_NUMBER() OVER (PARTITION BY ID ORDER BY SYSTEMMODSTAMP DESC, _INGESTED_AT DESC) = 1
) S
ON T.ID = S.ID
WHEN MATCHED AND NVL2HASH(T) != NVL2HASH(S) THEN UPDATE SET
  NAME = S.NAME,
  ACCOUNTNUMBER = S.ACCOUNTNUMBER,
  INDUSTRY = S.INDUSTRY,
  OWNERID = S.OWNERID,
  ISDELETED = S.ISDELETED,
  SYSTEMMODSTAMP = S.SYSTEMMODSTAMP,
  CREATEDDATE = S.CREATEDDATE,
  LASTMODIFIEDDATE = S.LASTMODIFIEDDATE,
  RECORD_LAST_SEEN = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN INSERT (
  ID, NAME, ACCOUNTNUMBER, INDUSTRY, OWNERID, ISDELETED,
  SYSTEMMODSTAMP, CREATEDDATE, LASTMODIFIEDDATE, RECORD_LAST_SEEN
) VALUES (
  S.ID, S.NAME, S.ACCOUNTNUMBER, S.INDUSTRY, S.OWNERID, S.ISDELETED,
  S.SYSTEMMODSTAMP, S.CREATEDDATE, S.LASTMODIFIEDDATE, CURRENT_TIMESTAMP()
);

-- Helper hash to detect changes (define once in a util schema)
CREATE OR REPLACE FUNCTION UTIL.NVL2HASH(OBJ VARIANT)
RETURNS STRING
AS
$$
  -- Minimal example: hash the important columns; replace with OBJECT_CONSTRUCT + HASH
  MD5(TO_VARCHAR(OBJ))
$$;
```

_(If you prefer, replace the function with a direct `HASH(*)` approach on selected columns.)_

**Scheduling:** use a **TASK** chain (pipe is continuous; merge runs every N minutes):

```sql
CREATE OR REPLACE TASK CURATED_SFDC.CORE.ACCOUNT_MERGE_TASK
  WAREHOUSE = WH_SFDC_PIPE
  SCHEDULE = 'USING CRON 0,10,20,30,40,50 * * * * America/Toronto'
AS
  CALL CURATED_SFDC.CORE.SP_MERGE_ACCOUNT();  -- or inline MERGE

ALTER TASK CURATED_SFDC.CORE.ACCOUNT_MERGE_TASK RESUME;
```

6) Python extractor (Bulk API v2 → S3)
======================================

Skeleton you can drop into Airflow/Prefect:

```python
import csv, io, json, os, time
import boto3, requests
from datetime import datetime, timezone

SF_LOGIN = os.environ["SF_LOGIN"]         # yourdomain.my.salesforce.com
SF_CLIENT_ID = os.environ["SF_CLIENT_ID"]
SF_USERNAME = os.environ["SF_USERNAME"]
SF_JWT_BEARER = os.environ["SF_JWT_BEARER"]  # signed JWT for OAuth JWT flow
S3_BUCKET = os.environ["S3_BUCKET"]

def salesforce_access_token():
    # Exchange JWT for access token
    r = requests.post(
        f"https://{SF_LOGIN}/services/oauth2/token",
        data={"grant_type":"urn:ietf:params:oauth:grant-type:jwt-bearer",
              "assertion": SF_JWT_BEARER}
    )
    r.raise_for_status()
    return r.json()["access_token"]

def bulk_query(object_name, soql):
    token = salesforce_access_token()
    h = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}
    # Create job
    job = requests.post(
        f"https://{SF_LOGIN}/services/data/v61.0/jobs/query",
        headers=h, json={"operation":"query","query":soql,"contentType":"CSV"}
    ).json()
    job_id = job["id"]
    # Poll until complete
    while True:
        j = requests.get(f"https://{SF_LOGIN}/services/data/v61.0/jobs/query/{job_id}", headers=h).json()
        if j["state"] in ("JobComplete","Failed","Aborted"): break
        time.sleep(3)
    # Download results (single chunk shown for brevity)
    r = requests.get(f"https://{SF_LOGIN}/services/data/v61.0/jobs/query/{job_id}/results", headers=h, stream=True)
    r.raise_for_status()
    return r.iter_lines()

def drop_to_s3(key_prefix, csv_iter):
    s3 = boto3.client("s3")
    key = f"{key_prefix}/load_dt={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H-%M-%S')}/part-00000.csv"
    body = io.BytesIO(b"")
    for line in csv_iter:
        body.write(line + b"\n")
    body.seek(0)
    s3.upload_fileobj(body, S3_BUCKET, key)
    return key

if __name__ == "__main__":
    # Incremental high-watermark (persist yours in a durable store)
    last_ts = os.environ.get("LAST_WM", "2025-08-10T00:00:00Z")
    soql = f"""
      SELECT Id, Name, AccountNumber, Industry, OwnerId,
             IsDeleted, SystemModstamp, CreatedDate, LastModifiedDate
      FROM Account
      WHERE SystemModstamp > {last_ts}
      ORDER BY SystemModstamp
    """
    lines = bulk_query("Account", soql)
    key = drop_to_s3("salesforce/account", lines)
    print("Uploaded:", key)
```

7) Governance: PII masking & row access
=======================================

```sql
-- Dynamic masking for emails (example)
CREATE OR REPLACE MASKING POLICY UTIL.MASK_EMAIL AS (VAL STRING) RETURNS STRING ->
  CASE WHEN CURRENT_ROLE() IN ('SFDC_READ_ROLE','SYSADMIN')
       THEN VAL
       ELSE REGEXP_REPLACE(VAL, '(^.).*(@.*$)', '\\1***\\2')
  END;

-- Apply to columns:
ALTER TABLE CURATED_SFDC.CORE.CONTACT MODIFY COLUMN EMAIL SET MASKING POLICY UTIL.MASK_EMAIL;

-- Row-level filters (e.g., by Region)
CREATE OR REPLACE ROW ACCESS POLICY UTIL.RAP_REGION AS (REGION STRING) RETURNS BOOLEAN ->
  REGION = CURRENT_REGION();  -- replace with your team/role mapping

ALTER TABLE ANALYTICS.SALES.OPPORTUNITY SET ROW ACCESS POLICY UTIL.RAP_REGION ON (REGION);
```

8) Monitoring & ops
===================

*   **API side:** track Bulk v2 job successes, retries, API limit headroom.
*   **Snowflake side:** `INFORMATION_SCHEMA.COPY_HISTORY`, `PIPE_USAGE_HISTORY`, `TASK_HISTORY`; alerts on failures.
*   **Drift detection:** nightly pull of **Salesforce Metadata** → compare to Snowflake columns; auto-add nullable columns in RAW.

* * *

If you want, tell me which **objects** you need first (e.g., `Account`, `Contact`, `Opportunity`, `Case`, `Task`) and your **cloud** (AWS/Azure/GCP). I’ll tailor the exact DDL, the `COPY`/`MERGE` scripts, and the Python extractor for your stack.



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)