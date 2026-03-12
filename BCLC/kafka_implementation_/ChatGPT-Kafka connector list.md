# Kafka connector list

**User:** Igor Pyvovarov (pyvovarov.igor@gmail.com)  
**Created:** 10/22/2025 18:42:20  
**Updated:** 10/28/2025 19:48:06  
**Exported:** 10/28/2025 16:49:00  
**Link:** [https://chatgpt.com/c/68f95dc8-11f4-8330-b3a7-7d0f8c463917](https://chatgpt.com/c/68f95dc8-11f4-8330-b3a7-7d0f8c463917)  

## Prompt:
List Kafka connectors

## Response:
Here’s a categorized list of **popular Apache Kafka connectors** — both **official (Confluent, Debezium)** and **community** ones — that are widely used in data engineering and integration pipelines.

* * *

### 🧩 **1\. Database Source Connectors**

Used to stream data **from databases into Kafka**.

| Connector | Type | Description |
| --- | --- | --- |
| **Debezium MySQL Connector** | Source | CDC (Change Data Capture) for MySQL |
| **Debezium PostgreSQL Connector** | Source | CDC for PostgreSQL |
| **Debezium SQL Server Connector** | Source | CDC for SQL Server |
| **Debezium Oracle Connector** | Source | CDC for Oracle DB |
| **Debezium MongoDB Connector** | Source | CDC for MongoDB |
| **JDBC Source Connector** | Source | Generic JDBC connector for polling any relational DB |
| **Snowflake Kafka Connector** | Sink | Streams Kafka topics into Snowflake tables |
| **MongoDB Kafka Connector** | Source/Sink | MongoDB official connector for Kafka |
| **Cassandra Source Connector** | Source | Streams changes from Cassandra (via CDC tables) |
| **Elasticsearch Source Connector** | Source | Streams data changes from Elasticsearch |

* * *

### 💾 **2\. Database Sink Connectors**

Used to stream **Kafka data into target databases**.

| Connector | Type | Description |
| --- | --- | --- |
| **JDBC Sink Connector** | Sink | Writes Kafka topics to any JDBC-compatible DB |
| **PostgreSQL Sink Connector** | Sink | Writes directly into PostgreSQL |
| **MySQL Sink Connector** | Sink | Writes directly into MySQL |
| **Snowflake Sink Connector** | Sink | Streams Kafka data to Snowflake |
| **Redshift Sink Connector** | Sink | Loads Kafka messages into Amazon Redshift |
| **Cassandra Sink Connector** | Sink | Writes Kafka topics to Cassandra tables |
| **MongoDB Sink Connector** | Sink | Streams Kafka topics to MongoDB collections |
| **Elasticsearch Sink Connector** | Sink | Indexes Kafka messages in Elasticsearch |

* * *

### ☁️ **3\. Cloud / Data Warehouse Connectors**

| Connector | Direction | Description |
| --- | --- | --- |
| **BigQuery Sink Connector** | Sink | Streams Kafka topics into Google BigQuery |
| **Amazon S3 Sink Connector** | Sink | Writes Kafka topics to S3 buckets (JSON/Avro/Parquet) |
| **Azure Blob Storage Sink Connector** | Sink | Writes Kafka topics to Azure Blob Storage |
| **Google Cloud Storage (GCS) Sink** | Sink | Writes Kafka topics to GCS |
| **Snowflake Sink Connector** | Sink | Streams Kafka messages to Snowflake |
| **Databricks Delta Lake Sink** | Sink | Writes to Delta tables |
| **Confluent Cloud Connectors** | Source/Sink | Managed connectors for SaaS and cloud services |

* * *

### 🔄 **4\. Messaging / Streaming Systems**

| Connector | Direction | Description |
| --- | --- | --- |
| **ActiveMQ Connector** | Source/Sink | Bridge Kafka with ActiveMQ queues |
| **RabbitMQ Connector** | Source/Sink | Bridge Kafka with RabbitMQ |
| **MQTT Connector** | Source/Sink | Stream IoT data to/from MQTT brokers |
| **Pulsar Connector** | Source/Sink | Kafka–Pulsar interoperability |

* * *

### 🗂 **5\. File and Storage Connectors**

| Connector | Type | Description |
| --- | --- | --- |
| **FileStream Source** | Source | Reads from local file (for testing) |
| **FileStream Sink** | Sink | Writes Kafka messages to local file |
| **SFTP Sink Connector** | Sink | Writes messages to remote SFTP server |
| **HDFS Sink Connector** | Sink | Writes Kafka messages to HDFS |
| **FTP Source/Sink** | Source/Sink | Transfers data via FTP/SFTP servers |

* * *

### 🧠 **6\. Analytics & Search**

| Connector | Type | Description |
| --- | --- | --- |
| **Elasticsearch Sink Connector** | Sink | Indexes data for search |
| **OpenSearch Sink Connector** | Sink | Similar to Elasticsearch sink |
| **Solr Sink Connector** | Sink | Writes Kafka topics to Apache Solr |

* * *

### ⚙️ **7\. Monitoring / Utility Connectors**

| Connector | Type | Description |
| --- | --- | --- |
| **Datadog Metrics Connector** | Sink | Exports metrics to Datadog |
| **Prometheus JMX Exporter** | Source | Publishes Kafka metrics |
| **Syslog Source Connector** | Source | Streams syslog messages into Kafka |
| **HTTP Sink Connector** | Sink | Sends Kafka records to HTTP endpoints (REST APIs) |

* * *

### 🧩 **8\. Notable Connector Frameworks**

*   **Confluent Hub** – official curated repository: https://www.confluent.io/hub/
*   **Debezium** – open-source CDC framework: https://debezium.io
*   **Kafka Connect (Apache)** – framework to run and manage connectors.
*   **Lenses.io** and **Aiven.io** – host enhanced connector ecosystems.

* * *

Would you like me to create a **comparison table (CSV or Markdown)** showing **source/sink direction, license, and configuration examples** for each?  
That’s often useful when planning Kafka integration in ETL or CDC pipelines.

## Prompt:
Yes, md

## Response:
Here’s a **comprehensive Markdown table** of the most popular **Apache Kafka Connect connectors**, categorized and ready for documentation use.  
You can copy it directly into your README, Confluence, or GitHub repo.

* * *

🧩 Kafka Connectors Overview
----------------------------

| Category | Connector | Type | Direction | Description | License / Source |
| --- | --- | --- | --- | --- | --- |
| **Databases (CDC / RDBMS)** | Debezium MySQL | CDC | Source | Streams MySQL binlog changes to Kafka | Apache 2.0 / debezium.io |
|  | Debezium PostgreSQL | CDC | Source | PostgreSQL logical decoding to Kafka | Apache 2.0 |
|  | Debezium SQL Server | CDC | Source | Reads SQL Server CDC tables | Apache 2.0 |
|  | Debezium Oracle | CDC | Source | Captures Oracle redo log changes | Apache 2.0 |
|  | Debezium MongoDB | CDC | Source | Streams MongoDB oplog changes | Apache 2.0 |
|  | JDBC Source | Polling | Source | Generic JDBC polling for any RDBMS | Confluent Hub |
|  | JDBC Sink | Writer | Sink | Writes Kafka topics to JDBC databases | Confluent Hub |
|  | Cassandra Source | CDC | Source | Streams Cassandra CDC logs | Community |
|  | Cassandra Sink | Writer | Sink | Writes topics to Cassandra | Confluent Hub |
|  | MongoDB Connector | CDC | Source/Sink | Streams between Kafka and MongoDB | MongoDB Inc. |
|  | Snowflake Connector | Loader | Sink | Streams Kafka topics into Snowflake | Snowflake Inc. |
|  | Redshift Sink | Loader | Sink | Loads Kafka topics into AWS Redshift | Confluent Hub |
|  | BigQuery Sink | Loader | Sink | Streams Kafka topics into GCP BigQuery | Confluent Hub |

* * *

| Category | Connector | Type | Direction | Description | License / Source |
| --- | --- | --- | --- | --- | --- |
| **Storage / Filesystems** | S3 Sink | Writer | Sink | Stores Kafka records in S3 (JSON, Avro, Parquet) | Confluent Hub |
|  | Azure Blob Sink | Writer | Sink | Stores Kafka messages in Azure Blob | Confluent Hub |
|  | Google Cloud Storage Sink | Writer | Sink | Streams to GCS | Confluent Hub |
|  | HDFS Sink | Writer | Sink | Writes Kafka records to HDFS | Confluent Hub |
|  | SFTP Sink | Writer | Sink | Streams Kafka topics to SFTP servers | Community |
|  | FileStream Source | Simple | Source | Reads local file line-by-line (for test) | Apache Kafka |
|  | FileStream Sink | Simple | Sink | Writes Kafka topics to local file | Apache Kafka |

* * *

| Category | Connector | Type | Direction | Description | License / Source |
| --- | --- | --- | --- | --- | --- |
| **Messaging / Streaming** | RabbitMQ | Bridge | Source/Sink | Bridges RabbitMQ and Kafka | Community |
|  | ActiveMQ | Bridge | Source/Sink | Connects Kafka with ActiveMQ | Confluent Hub |
|  | MQTT | IoT | Source/Sink | Streams IoT messages via MQTT | Community |
|  | Pulsar | Bridge | Source/Sink | Kafka–Pulsar interoperability | Apache 2.0 |
|  | JMS Connector | Bridge | Source/Sink | Works with any JMS-compatible queue | Confluent Hub |

* * *

| Category | Connector | Type | Direction | Description | License / Source |
| --- | --- | --- | --- | --- | --- |
| **Analytics / Search** | Elasticsearch | Indexer | Sink | Indexes Kafka messages in Elasticsearch | Confluent Hub |
|  | OpenSearch | Indexer | Sink | Writes Kafka data to OpenSearch | AWS |
|  | Solr | Indexer | Sink | Writes to Apache Solr | Community |
|  | Databricks Delta | Loader | Sink | Writes to Delta Lake tables | Confluent Hub |

* * *

| Category | Connector | Type | Direction | Description | License / Source |
| --- | --- | --- | --- | --- | --- |
| **Monitoring / Logs** | Syslog Source | Ingest | Source | Streams syslog messages into Kafka | Community |
|  | HTTP Sink | Writer | Sink | Sends Kafka events to HTTP REST APIs | Confluent Hub |
|  | Datadog Metrics | Exporter | Sink | Sends Kafka metrics to Datadog | Confluent Hub |
|  | Prometheus JMX Exporter | Metrics | Source | Publishes Kafka Connect metrics | Apache 2.0 |

* * *

| Category | Connector | Type | Direction | Description | License / Source |
| --- | --- | --- | --- | --- | --- |
| **Cloud SaaS / Apps** | Salesforce Connector | API | Source/Sink | Streams Salesforce events | Confluent Hub |
|  | ServiceNow Connector | API | Source/Sink | Reads/writes ServiceNow data | Confluent Hub |
|  | Google Pub/Sub | API | Source/Sink | Streams between Kafka and GCP Pub/Sub | Confluent Hub |
|  | Azure Event Hubs | API | Source/Sink | Connects Kafka to Azure Event Hubs | Microsoft |
|  | SAP HANA Connector | API | Source/Sink | Integrates with SAP HANA | Confluent Hub |

* * *

⚙️ Example Configuration (Kafka Connect JSON)
---------------------------------------------

```json
{
  "name": "jdbc-source-connector",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "connection.url": "jdbc:postgresql://localhost:5432/mydb",
    "connection.user": "dbuser",
    "connection.password": "dbpass",
    "table.whitelist": "customers",
    "mode": "incrementing",
    "incrementing.column.name": "id",
    "topic.prefix": "db-",
    "poll.interval.ms": 10000
  }
}
```

* * *

🔗 References
-------------

*   **Confluent Hub (official connectors):** https://www.confluent.io/hub/
*   **Debezium (CDC connectors):** https://debezium.io/documentation/
*   **Kafka Connect (Apache docs):** https://kafka.apache.org/documentation/#connect
*   **Community Connectors:** [https://github.com/topics/kafka-connect](https://github.com/topics/kafka-connect)

* * *

Would you like me to generate this as a **Markdown file (`kafka_connectors.md`)** for download or GitHub import (with emojis and links preserved)?

## Prompt:
Kafka multcloud connect aws to Salesforce

## Response:
Excellent — you're referring to **integrating AWS data with Salesforce via Apache Kafka Connect**, often through a **multi-cloud architecture** (AWS ↔ Kafka ↔ Salesforce).  
Let’s break this down in a **clear, architecture-level guide**, including recommended connectors, data flow, and configuration examples.

* * *

☁️ **1\. Architecture Overview: AWS → Kafka → Salesforce**
----------------------------------------------------------

```
+----------------+         +-------------------+         +---------------------+
|  AWS Services  |  --->   |  Kafka Connect    |  --->   |  Salesforce (CRM)   |
| (S3, RDS, SNS) |         |  (on AWS or GCP)  |         |  Cloud or Sandbox   |
+----------------+         +-------------------+         +---------------------+
        ↑                         ↑                             ↑
        |                         |                             |
    Debezium / S3 Source    Kafka Topics                 Salesforce Sink Connector
```

**Core idea:**  
Kafka acts as a **multi-cloud message bridge**, streaming data **from AWS (S3, RDS, DynamoDB, etc.) into Salesforce objects** in near-real-time using **Kafka Connect + Confluent Salesforce Sink** (or **HTTP API sink**).

* * *

🔗 **2\. Required Kafka Connectors**
------------------------------------

| Connector | Direction | Description | Source |
| --- | --- | --- | --- |
| **S3 Source Connector** | Source | Reads new files (JSON, Avro, CSV, Parquet) from AWS S3 buckets | Confluent Hub |
| **JDBC Source (RDS)** | Source | Streams rows from AWS RDS (PostgreSQL, MySQL, Aurora) | Confluent Hub |
| **Kinesis Source Connector** | Source | Ingests events from AWS Kinesis streams | Confluent Hub |
| **Salesforce Sink Connector** | Sink | Writes Kafka topic records into Salesforce objects via REST/Bulk APIs | Confluent Hub |
| _(optional)_ **Salesforce Source Connector** | Source | Captures Salesforce CDC events (Streaming API v2) | Confluent Hub |

* * *

⚙️ **3\. Typical Data Flows**
-----------------------------

### 🔸 **Use Case A — AWS RDS → Kafka → Salesforce**

*   Use **Debezium or JDBC Source** to read data from RDS.
*   Transform schema (via **Kafka Connect SMTs** or **ksqlDB**).
*   Deliver records into **Salesforce Contacts, Leads, Cases**, etc., via the **Salesforce Sink Connector**.

### 🔸 **Use Case B — S3 Files → Kafka → Salesforce**

*   Use **S3 Source Connector** to monitor bucket and stream file content.
*   Map JSON/CSV fields to Salesforce object fields.
*   Send transformed payloads to **Salesforce Sink**.

### 🔸 **Use Case C — Bi-Directional**

*   Add **Salesforce Source Connector** to stream updates from Salesforce back to Kafka for AWS analytics or auditing.

* * *

🧰 **4\. Example Configurations**
---------------------------------

### 🟢 **S3 Source Connector**

```json
{
  "name": "s3-source",
  "config": {
    "connector.class": "io.confluent.connect.s3.source.S3SourceConnector",
    "tasks.max": "1",
    "s3.bucket.name": "aws-data-bucket",
    "aws.access.key.id": "YOUR_AWS_KEY",
    "aws.secret.access.key": "YOUR_AWS_SECRET",
    "format.class": "io.confluent.connect.s3.format.json.JsonFormat",
    "topic.prefix": "s3-",
    "transforms": "unwrap",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState"
  }
}
```

* * *

### 🔵 **Salesforce Sink Connector**

```json
{
  "name": "salesforce-sink",
  "config": {
    "connector.class": "io.confluent.connect.salesforce.SalesforceSinkConnector",
    "topics": "s3-customers",
    "tasks.max": "1",
    "salesforce.object": "Contact",
    "salesforce.instance": "https://login.salesforce.com",
    "salesforce.username": "youruser@example.com",
    "salesforce.password": "yourPasswordWithToken",
    "salesforce.consumer.key": "YOUR_CONSUMER_KEY",
    "salesforce.consumer.secret": "YOUR_CONSUMER_SECRET",
    "salesforce.use.bulk.api": "true",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false"
  }
}
```

* * *

🔐 **5\. Security & Authentication**
------------------------------------

| Layer | Mechanism |
| --- | --- |
| **AWS → Kafka** | IAM Role / Access Key for S3, JDBC credentials for RDS |
| **Kafka → Salesforce** | OAuth2 / Connected App consumer key + secret |
| **Kafka Cluster** | SASL\_SSL, mTLS, or Confluent Cloud API keys |
| **Data Encryption** | End-to-end TLS (AWS SDK → Kafka Connect → Salesforce REST) |

* * *

🚀 **6\. Deployment Options**
-----------------------------

| Deployment | Description |
| --- | --- |
| **Confluent Cloud Connect** | Managed Kafka Connect + Salesforce Sink (no infra) |
| **Self-Managed Connect Cluster (AWS EKS/EC2)** | Control versions and custom SMTs |
| **Fully Multi-Cloud** | Kafka on AWS, Salesforce on SF Cloud, with optional backup Kafka MirrorMaker between regions |

* * *

📈 **7\. Multi-Cloud Sync Enhancements**
----------------------------------------

*   **Schema Registry** – Ensure consistent field mappings for Salesforce objects.
*   **ksqlDB / Streams API** – Filter or enrich AWS data before loading.
*   **Dead-Letter Queue (DLQ)** – Catch rejected records from Salesforce API.
*   **Monitoring** – Use Confluent Control Center or Datadog connector for metrics.

* * *

🧩 **8\. References**
---------------------

*   Confluent Salesforce Sink: https://www.confluent.io/hub/confluentinc/kafka-connect-salesforce
*   AWS S3 Source Connector: https://www.confluent.io/hub/confluentinc/kafka-connect-s3-source
*   Debezium CDC: https://debezium.io/documentation/
*   Multi-Cloud MirrorMaker: https://docs.confluent.io/platform/current/mirrormaker2/overview.html

* * *

Would you like me to generate this as a **ready-to-use `kafka_aws_salesforce.md` architecture file** (with diagrams and connector JSON templates included)?  
It can serve as your deployment or documentation blueprint.



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)