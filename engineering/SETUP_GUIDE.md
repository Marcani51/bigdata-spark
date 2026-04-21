# Setup Guide — Implementasi Solusi Big Data (Localhost + Docker)

Panduan ini menjelaskan langkah-langkah untuk menjalankan seluruh pipeline Big Data dari Bab 2 laporan, menggunakan **Apache Spark (PySpark)** di atas **Docker** pada mesin lokal (MacBook 16 GB RAM).

---

## 1. Arsitektur Implementasi

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                        │
│                                                          │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐ │
│  │ spark-master │◄──│ spark-worker │   │   jupyter     │ │
│  │  :8080       │   │  :8081       │   │  :8888        │ │
│  │  :7077       │   │              │   │  (PySpark)    │ │
│  └──────────────┘   └──────────────┘   └──────────────┘ │
│                                                          │
│         ▲                                    │           │
│         │            Volume Mounts           │           │
│         ▼                                    ▼           │
│  ┌──────────────────────────────────────────────┐       │
│  │  ./data/     → /opt/spark/data               │       │
│  │  ./notebooks/→ /home/jovyan/work             │       │
│  │  ./output/   → /opt/spark/output             │       │
│  └──────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────┘
```

**Data Flow:**
```
retail_sales_dataset.csv (./data/)
    → Jupyter Notebook (PySpark)
    → Spark Master + Worker (Distributed Processing)
    → Parquet Output (./output/)
    → Pandas + Matplotlib (Visualisasi di Notebook)
```

---

## 2. Prasyarat

| Komponen        | Versi Minimum | Cek Instalasi              |
|-----------------|---------------|----------------------------|
| Docker Desktop  | 4.0+          | `docker --version`         |
| Docker Compose  | v2.0+         | `docker compose version`   |
| RAM tersedia    | 6 GB (Docker) | Docker Desktop → Settings  |

### Konfigurasi Docker Desktop (PENTING untuk MacBook 16 GB)

Buka **Docker Desktop → Settings → Resources** dan atur:

| Resource | Rekomendasi | Alasan                                    |
|----------|-------------|-------------------------------------------|
| CPUs     | 4           | Cukup untuk 1 master + 1 worker           |
| Memory   | 6 GB        | Sisa 10 GB untuk macOS + apps lain        |
| Swap     | 2 GB        | Cadangan jika memory penuh                |
| Disk     | 20 GB       | Untuk images + data Parquet               |

> ⚠️ **Jangan set memory Docker lebih dari 8 GB** pada MacBook 16 GB! Ini akan membuat macOS lambat karena kehabisan RAM.

---

## 3. Struktur Direktori Proyek

```
bigdatatugas/
├── dockerspark/
│   ├── docker-compose.yml      ← Docker Compose (sudah diperbarui)
│   ├── data/
│   │   └── retail_sales_dataset.csv  ← Dataset (akan di-copy)
│   ├── notebooks/
│   │   └── pipeline.ipynb      ← Jupyter Notebook utama
│   └── output/                 ← Hasil Parquet output
├── retail_sales_dataset.csv    ← Dataset asli
├── Laporan_BigData_Full.md     ← Laporan
└── SETUP_GUIDE.md              ← File ini
```

---

## 4. Langkah Setup

### Step 1: Siapkan Direktori & Copy Dataset

```bash
# Dari root project
cd bigdatatugas/dockerspark

# Buat folder yang dibutuhkan
mkdir -p data notebooks output

# Copy dataset ke folder Docker
cp ../retail_sales_dataset.csv data/
```

### Step 2: Update Docker Compose

File `docker-compose.yml` sudah diperbarui dengan:
- **Memory limits** (agar MacBook tidak kehabisan RAM)
- **Volume mounts** (agar data & notebook tersimpan di host)
- **Network** (agar kontainer bisa saling komunikasi)
- **Shared Spark jars** (agar Jupyter bisa connect ke cluster)

Lihat file `docker-compose.yml` yang sudah diperbarui di direktori ini.

### Step 3: Jalankan Docker Compose

```bash
cd bigdatatugas/dockerspark

# Pull image terlebih dahulu (hanya perlu sekali)
docker compose pull

# Jalankan semua service
docker compose up -d

# Cek status
docker compose ps
```

### Step 4: Akses Services

| Service        | URL                          | Fungsi                          |
|----------------|------------------------------|---------------------------------|
| Spark Master   | http://localhost:8080         | Dashboard Spark cluster         |
| Spark Worker   | http://localhost:8081         | Dashboard worker node           |
| Jupyter Lab    | http://localhost:8888         | Notebook untuk coding PySpark   |

> 📌 **Jupyter token**: Cek token dengan `docker compose logs jupyter | grep token`

### Step 5: Verifikasi Koneksi Spark

Buka Jupyter (http://localhost:8888), buat notebook baru, lalu jalankan:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("RetailAnalysis") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "1g") \
    .config("spark.driver.memory", "1g") \
    .getOrCreate()

# Test: cek Spark version
print(f"Spark Version: {spark.version}")
print(f"Spark Master: {spark.sparkContext.master}")

# Test: baca dataset
df = spark.read.csv("/opt/spark/data/retail_sales_dataset.csv", header=True, inferSchema=True)
df.show(5)
print(f"Total rows: {df.count()}")
```

Jika output menunjukkan 1.000 baris → setup berhasil! ✅

---

## 5. Pipeline Implementasi (Sesuai Bab 2)

Setelah setup berhasil, jalankan pipeline berikut di Jupyter Notebook.
File notebook `pipeline.ipynb` sudah disiapkan di folder `notebooks/`.

### 5.1 Data Ingestion (Bab 2.2)

```python
from pyspark.sql import SparkSession
from pyspark.sql.types import *

# Inisialisasi Spark Session
spark = SparkSession.builder \
    .appName("RetailBigDataPipeline") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "1g") \
    .config("spark.driver.memory", "1g") \
    .getOrCreate()

# Definisi Schema Eksplisit (sesuai RULES — no inferSchema)
schema = StructType([
    StructField("Transaction_ID", IntegerType(), False),
    StructField("Date", StringType(), False),
    StructField("Customer_ID", StringType(), False),
    StructField("Gender", StringType(), False),
    StructField("Age", IntegerType(), False),
    StructField("Product_Category", StringType(), False),
    StructField("Quantity", IntegerType(), False),
    StructField("Price_per_Unit", IntegerType(), False),
    StructField("Total_Amount", IntegerType(), False)
])

# Batch Ingestion — Load CSV
df_raw = spark.read.csv(
    "/opt/spark/data/retail_sales_dataset.csv",
    header=True,
    schema=schema
)

print(f"✅ Data loaded: {df_raw.count()} rows, {len(df_raw.columns)} columns")
df_raw.printSchema()
df_raw.show(5)
```

### 5.2 Data Validation & Cleaning

```python
from pyspark.sql.functions import col, to_date, when, count

# 1. Konversi Date string → DateType
df = df_raw.withColumn("Date", to_date(col("Date"), "yyyy-MM-dd"))

# 2. Null check
print("=== Null Check ===")
df.select([count(when(col(c).isNull(), c)).alias(c) for c in df.columns]).show()

# 3. Validasi rentang nilai
print("=== Range Validation ===")
df.select(
    col("Age").alias("Age_val"),
    col("Quantity").alias("Qty_val"),
    col("Price_per_Unit").alias("Price_val")
).summary("min", "max").show()

# 4. Validasi business rule: Total_Amount == Quantity × Price_per_Unit
df_invalid = df.filter(col("Total_Amount") != col("Quantity") * col("Price_per_Unit"))
print(f"❌ Invalid rows (Total ≠ Qty × Price): {df_invalid.count()}")
print(f"✅ Valid rows: {df.count() - df_invalid.count()}")

# 5. Cache cleaned data (akan dipakai berulang)
df_clean = df.filter(col("Total_Amount") == col("Quantity") * col("Price_per_Unit"))
df_clean.cache()
print(f"\n✅ Clean data cached: {df_clean.count()} rows")
```

### 5.3 Data Storage — Simpan ke Parquet (Bab 2.3)

```python
# Simpan ke Parquet (partisi berdasarkan Product_Category)
df_clean.write \
    .mode("overwrite") \
    .partitionBy("Product_Category") \
    .parquet("/opt/spark/output/retail_parquet")

print("✅ Data saved to Parquet (partitioned by Product_Category)")

# Verifikasi: baca kembali dari Parquet
df_parquet = spark.read.parquet("/opt/spark/output/retail_parquet")
print(f"✅ Parquet read back: {df_parquet.count()} rows")
```

### 5.4 Analisis dengan Spark SQL (Bab 2.4a)

```python
# Register sebagai SQL Table
df_clean.createOrReplaceTempView("transactions")

# Query 1: Revenue per kategori produk
print("=== Revenue per Kategori ===")
spark.sql("""
    SELECT 
        Product_Category,
        COUNT(*) as total_transaksi,
        ROUND(AVG(Total_Amount), 1) as avg_amount,
        SUM(Total_Amount) as total_revenue
    FROM transactions
    GROUP BY Product_Category
    ORDER BY total_revenue DESC
""").show()

# Query 2: Distribusi gender
print("=== Distribusi Gender ===")
spark.sql("""
    SELECT 
        Gender,
        COUNT(*) as jumlah,
        ROUND(AVG(Total_Amount), 1) as avg_spending
    FROM transactions
    GROUP BY Gender
""").show()

# Query 3: Top spending age groups
print("=== Spending per Age Group ===")
spark.sql("""
    SELECT 
        CASE 
            WHEN Age BETWEEN 18 AND 25 THEN '18-25 (Muda)'
            WHEN Age BETWEEN 26 AND 35 THEN '26-35 (Dewasa Muda)'
            WHEN Age BETWEEN 36 AND 45 THEN '36-45 (Dewasa)'
            WHEN Age BETWEEN 46 AND 55 THEN '46-55 (Dewasa Atas)'
            ELSE '56-64 (Pra-Lansia)'
        END as age_group,
        COUNT(*) as jumlah,
        SUM(Total_Amount) as total_spending,
        ROUND(AVG(Total_Amount), 1) as avg_spending
    FROM transactions
    GROUP BY age_group
    ORDER BY total_spending DESC
""").show()

# Query 4: Tren bulanan
print("=== Tren Penjualan Bulanan ===")
spark.sql("""
    SELECT 
        MONTH(Date) as bulan,
        COUNT(*) as total_transaksi,
        SUM(Total_Amount) as total_revenue
    FROM transactions
    GROUP BY MONTH(Date)
    ORDER BY bulan
""").show(12)
```

### 5.5 Segmentasi Pelanggan — K-Means (Bab 2.4b)

```python
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.clustering import KMeans
from pyspark.ml import Pipeline

# Buat fitur per pelanggan
df_customer = spark.sql("""
    SELECT 
        Customer_ID,
        COUNT(*) as frequency,
        AVG(Total_Amount) as avg_monetary,
        AVG(Quantity) as avg_quantity
    FROM transactions
    GROUP BY Customer_ID
""")

# Assemble fitur menjadi vector
assembler = VectorAssembler(
    inputCols=["frequency", "avg_monetary", "avg_quantity"],
    outputCol="features_raw"
)

# Scale fitur
scaler = StandardScaler(
    inputCol="features_raw",
    outputCol="features",
    withStd=True, withMean=True
)

# K-Means (3 segmen: Low, Medium, High Value)
kmeans = KMeans(k=3, seed=42, featuresCol="features", predictionCol="segment")

# Pipeline
pipeline = Pipeline(stages=[assembler, scaler, kmeans])
model = pipeline.fit(df_customer)
df_segmented = model.transform(df_customer)

# Hasil segmentasi
print("=== Hasil Segmentasi Pelanggan (K-Means, k=3) ===")
df_segmented.groupBy("segment").agg(
    {"Customer_ID": "count", "avg_monetary": "avg", "frequency": "avg"}
).orderBy("segment").show()

# Simpan hasil segmentasi
df_segmented.select("Customer_ID", "frequency", "avg_monetary", "avg_quantity", "segment") \
    .write.mode("overwrite") \
    .parquet("/opt/spark/output/customer_segments")

print("✅ Segmentasi disimpan ke /opt/spark/output/customer_segments")
```

### 5.6 Visualisasi dengan Pandas + Matplotlib (Bab 2.4c)

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Konversi ke Pandas (dataset kecil, aman pakai .toPandas())
pdf_revenue = spark.sql("""
    SELECT Product_Category, SUM(Total_Amount) as revenue
    FROM transactions GROUP BY Product_Category
""").toPandas()

pdf_monthly = spark.sql("""
    SELECT MONTH(Date) as bulan, SUM(Total_Amount) as revenue
    FROM transactions GROUP BY MONTH(Date) ORDER BY bulan
""").toPandas()

pdf_segments = df_segmented.select("segment", "avg_monetary", "frequency").toPandas()

# --- Plot 1: Revenue per Kategori ---
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

axes[0].bar(pdf_revenue["Product_Category"], pdf_revenue["revenue"], 
            color=["#FF6B6B", "#4ECDC4", "#45B7D1"])
axes[0].set_title("Total Revenue per Kategori Produk", fontsize=13, fontweight="bold")
axes[0].set_ylabel("Revenue")
axes[0].ticklabel_format(style='plain', axis='y')

# --- Plot 2: Tren Bulanan ---
axes[1].plot(pdf_monthly["bulan"], pdf_monthly["revenue"], 
             marker='o', color="#6C5CE7", linewidth=2)
axes[1].set_title("Tren Penjualan Bulanan (2023)", fontsize=13, fontweight="bold")
axes[1].set_xlabel("Bulan")
axes[1].set_ylabel("Revenue")
axes[1].set_xticks(range(1, 13))

# --- Plot 3: Segmentasi Pelanggan ---
colors = ["#FF6B6B", "#4ECDC4", "#45B7D1"]
for seg in sorted(pdf_segments["segment"].unique()):
    mask = pdf_segments["segment"] == seg
    axes[2].scatter(pdf_segments[mask]["frequency"], 
                    pdf_segments[mask]["avg_monetary"],
                    label=f"Segment {seg}", alpha=0.6, color=colors[seg])
axes[2].set_title("Segmentasi Pelanggan (K-Means)", fontsize=13, fontweight="bold")
axes[2].set_xlabel("Frequency")
axes[2].set_ylabel("Avg Monetary")
axes[2].legend()

plt.tight_layout()
plt.savefig("/home/jovyan/work/visualisasi_hasil.png", dpi=150, bbox_inches="tight")
plt.show()
print("✅ Visualisasi disimpan ke notebooks/visualisasi_hasil.png")
```

---

## 6. Perintah Operasional

### Start / Stop Cluster

```bash
# Start semua service
docker compose up -d

# Stop (data tetap tersimpan di volume)
docker compose down

# Stop + hapus semua data
docker compose down -v
```

### Monitoring

```bash
# Lihat log semua service
docker compose logs -f

# Lihat log Spark Master saja
docker compose logs -f spark-master

# Cek resource usage
docker stats
```

### Troubleshooting

| Masalah                          | Solusi                                           |
|----------------------------------|--------------------------------------------------|
| Jupyter tidak bisa akses         | `docker compose logs jupyter \| grep token`      |
| Spark worker disconnect          | Cek memory limit, naikkan jika perlu              |
| "Java heap space" error          | Kurangi `spark.executor.memory` ke `512m`         |
| Container restart terus          | `docker compose logs <service>` untuk cek error   |
| Port sudah dipakai               | Ubah port mapping di `docker-compose.yml`         |

---

## 7. Tips Hemat Memory MacBook

1. **Jangan jalankan app berat** (Chrome banyak tab, VS Code extensions) bersamaan dengan Spark cluster
2. **Stop cluster saat tidak dipakai**: `docker compose down`
3. **Monitor RAM**: Gunakan Activity Monitor untuk cek sisa memory
4. **Gunakan 1 worker saja** (sudah dikonfigurasi di docker-compose)
5. **Cache hanya DataFrame yang benar-benar dipakai berulang**
6. **Gunakan `.select()` untuk ambil kolom yang dibutuhkan saja**, jangan `select *`


StructType([
    StructField("transaction_id", IntegerType(), nullable=False),
    StructField("date", DateType(), nullable=False),
    StructField("customer_id", StringType(), nullable=False),
    StructField("gender", StringType(), nullable=False),
    StructField("age", IntegerType(), nullable=False),
    StructField("product_category", StringType(), nullable=False),
    StructField("quantity", IntegerType(), nullable=False),
    StructField("price_per_unit", IntegerType(), nullable=False),
    StructField("total_amount", IntegerType(), nullable=False)
])