# RULES.md — Big Data Engineering & Analytics (Apache Spark + Python)

## 1. Core Principles

- Always design for **scalability**, **fault tolerance**, and **distributed processing**.
- Prefer **lazy evaluation frameworks** (Spark) over eager computation.
- Optimize for **data locality** and **minimize shuffling**.
- Solutions must be **production-oriented**, not just academic.

---

## 2. Technology Stack Standards

### Mandatory

- Apache Spark (PySpark)
- Python 3.10+
- Distributed Storage: HDFS / S3-compatible
- Data Format: Parquet (default), ORC (optional)

### Optional (depending on use case)

- Kafka (streaming)
- Airflow (orchestration)
- Delta Lake / Iceberg (data lakehouse)
- Redis (caching)

---

## 3. Data Handling Rules

### Format

- Use **Parquet** as default format
- Avoid CSV in production pipelines

### Schema

- Always define explicit schema
- Avoid schema inference in large datasets

### Partitioning

- Partition by:
  - Date (YYYY/MM/DD)
  - High-cardinality keys only if necessary

### Example

```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("user_id", StringType()),
    StructField("amount", IntegerType())
])
```

---

## 4. Performance Optimization Rules

### MUST

- Use `.select()` instead of `select *`
- Use `.filter()` early (predicate pushdown)
- Cache only when reused multiple times

### AVOID

- `.collect()` on large datasets
- `.toPandas()` unless dataset is small

### Joins

- Use broadcast join when one dataset is small

```python
from pyspark.sql.functions import broadcast

df.join(broadcast(small_df), "id")
```

---

## 5. Spark Architecture Usage

- Use **DataFrame API** over RDD
- Use **Spark SQL** for complex queries
- Use **Structured Streaming** for real-time data

---

## 6. Pipeline Design Rules

Pipeline must follow:

1. Ingestion
2. Validation
3. Transformation
4. Aggregation
5. Storage
6. Serving layer

---

## 7. Error Handling

- Always log errors
- Use retry mechanisms for ingestion
- Validate schema and null values

---

## 8. Code Structure

```
/project
  /jobs
  /utils
  /configs
  /pipelines
  main.py
```

---

## 9. Testing

- Unit test transformations
- Use small sample datasets
- Validate schema consistency

---

## 10. Output Standards

- Always provide:
  - Architecture diagram (textual)
  - Data flow explanation
  - Code implementation (PySpark)
  - Optimization explanation
