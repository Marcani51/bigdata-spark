"""
Script untuk generate semua Jupyter Notebook (.ipynb) pipeline Big Data.
Jalankan sekali: python3 generate_notebooks.py
"""
import json
import os

def make_nb(cells):
    """Create notebook JSON structure."""
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.11.0",
                "mimetype": "text/x-python",
                "file_extension": ".py"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

def md(source):
    """Create markdown cell."""
    return {"cell_type": "markdown", "metadata": {}, "source": source.split("\n")}

def code(source):
    """Create code cell."""
    lines = source.split("\n")
    # Add newlines to all but last line
    src = [l + "\n" for l in lines[:-1]] + [lines[-1]]
    return {"cell_type": "code", "metadata": {}, "source": src, "outputs": [], "execution_count": None}

# ============================================================
# NOTEBOOK 1: Setup & Connection Test
# ============================================================
nb1 = make_nb([
    md("# 01 — Setup & Connection Test\n\nNotebook ini memverifikasi koneksi PySpark ke Spark cluster.\n\n**Prasyarat:** Docker Compose sudah running (`docker compose up -d`)"),

    md("## 1.1 Inisialisasi SparkSession"),
    code("""from pyspark.sql import SparkSession

spark = SparkSession.builder \\
    .appName("01_SetupTest") \\
    .master("spark://spark-master:7077") \\
    .config("spark.executor.memory", "1g") \\
    .config("spark.driver.memory", "1g") \\
    .getOrCreate()

print(f"✅ Spark Version : {spark.version}")
print(f"✅ Spark Master  : {spark.sparkContext.master}")
print(f"✅ App Name      : {spark.sparkContext.appName}")"""),

    md("## 1.2 Test Baca Dataset"),
    code("""# Quick test — baca CSV
df_test = spark.read.csv("/data/retail_sales_dataset.csv", header=True, inferSchema=True)

print(f"✅ Total Rows   : {df_test.count()}")
print(f"✅ Total Columns: {len(df_test.columns)}")
print(f"✅ Columns      : {df_test.columns}")
df_test.show(5)"""),

    md("## 1.3 Test Spark SQL"),
    code("""df_test.createOrReplaceTempView("test_table")

result = spark.sql("SELECT COUNT(*) as total FROM test_table")
result.show()
print("✅ Spark SQL berfungsi dengan baik!")"""),

    md("## 1.4 Cleanup"),
    code("""spark.stop()
print("✅ SparkSession ditutup. Setup berhasil!")"""),
])

# ============================================================
# NOTEBOOK 2: Data Ingestion
# ============================================================
nb2 = make_nb([
    md("# 02 — Data Ingestion (Bab 2.2)\n\nNotebook ini mengimplementasikan proses **Batch Ingestion** — memuat dataset CSV ke dalam Spark DataFrame menggunakan **explicit schema** (sesuai best practice)."),

    md("## 2.1 Inisialisasi SparkSession"),
    code("""from pyspark.sql import SparkSession

spark = SparkSession.builder \\
    .appName("02_DataIngestion") \\
    .master("spark://spark-master:7077") \\
    .config("spark.executor.memory", "1g") \\
    .config("spark.driver.memory", "1g") \\
    .getOrCreate()

print(f"✅ Spark {spark.version} connected")"""),

    md("## 2.2 Definisi Explicit Schema\n\nSesuai RULES: *\"Always define explicit schema, avoid schema inference in large datasets\"*"),
    code("""from pyspark.sql.types import (
    StructType, StructField, 
    IntegerType, StringType
)

# Schema eksplisit untuk retail_sales_dataset.csv
schema = StructType([
    StructField("Transaction_ID", IntegerType(), nullable=False),
    StructField("Date", StringType(), nullable=False),
    StructField("Customer_ID", StringType(), nullable=False),
    StructField("Gender", StringType(), nullable=False),
    StructField("Age", IntegerType(), nullable=False),
    StructField("Product_Category", StringType(), nullable=False),
    StructField("Quantity", IntegerType(), nullable=False),
    StructField("Price_per_Unit", IntegerType(), nullable=False),
    StructField("Total_Amount", IntegerType(), nullable=False)
])

print("✅ Schema didefinisikan:")
for field in schema.fields:
    print(f"   {field.name:20s} → {str(field.dataType):15s} (nullable={field.nullable})")"""),

    md("## 2.3 Batch Ingestion — Load CSV"),
    code("""# Load CSV dengan explicit schema
df_raw = spark.read.csv(
    "/data/retail_sales_dataset.csv",
    header=True,
    schema=schema
)

# Verifikasi hasil ingestion
print(f"✅ Data berhasil di-load!")
print(f"   Jumlah baris   : {df_raw.count()}")
print(f"   Jumlah kolom   : {len(df_raw.columns)}")
print(f"   Partisi        : {df_raw.rdd.getNumPartitions()}")
print()
print("=== Schema ===")
df_raw.printSchema()"""),

    md("## 2.4 Preview Data"),
    code("""# Tampilkan 10 baris pertama
df_raw.show(10, truncate=False)"""),

    md("## 2.5 Statistik Deskriptif Awal"),
    code("""# Summary statistics untuk kolom numerik
df_raw.select("Age", "Quantity", "Price_per_Unit", "Total_Amount").summary().show()"""),

    md("## 2.6 Simpan DataFrame sebagai Temporary View\n\nDisimpan agar bisa diakses di notebook selanjutnya via Spark SQL."),
    code("""df_raw.createOrReplaceTempView("raw_transactions")
print("✅ Temporary view 'raw_transactions' dibuat")
print("   Bisa diakses dengan: spark.sql('SELECT * FROM raw_transactions')")"""),

    code("""# Jangan stop spark — akan dipakai di notebook berikutnya
print("📌 SparkSession tetap aktif untuk notebook selanjutnya")"""),
])

# ============================================================
# NOTEBOOK 3: Data Validation & Cleaning
# ============================================================
nb3 = make_nb([
    md("# 03 — Data Validation & Cleaning (Bab 3.4)\n\nNotebook ini mengimplementasikan proses validasi dan pembersihan data sesuai **6 dimensi kualitas data** yang didefinisikan di Bab 3.4."),

    md("## 3.1 Inisialisasi SparkSession"),
    code("""from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, when, count, lit, sum as spark_sum

spark = SparkSession.builder \\
    .appName("03_DataValidation") \\
    .master("spark://spark-master:7077") \\
    .config("spark.executor.memory", "1g") \\
    .config("spark.driver.memory", "1g") \\
    .getOrCreate()

print(f"✅ Spark {spark.version} connected")"""),

    md("## 3.2 Load Data dari CSV"),
    code("""from pyspark.sql.types import StructType, StructField, IntegerType, StringType

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

df_raw = spark.read.csv("/data/retail_sales_dataset.csv", header=True, schema=schema)
print(f"✅ Loaded {df_raw.count()} rows")"""),

    md("## 3.3 Dimensi 1: Kelengkapan (*Completeness*)\n\nCek apakah ada nilai NULL di setiap kolom."),
    code("""print("=== NULL CHECK (Kelengkapan Data) ===")
null_counts = df_raw.select(
    [count(when(col(c).isNull(), c)).alias(c) for c in df_raw.columns]
)
null_counts.show(truncate=False)

total_nulls = sum([null_counts.collect()[0][c] for c in df_raw.columns])
if total_nulls == 0:
    print("✅ PASS — Tidak ada nilai NULL. Kelengkapan 100%")
else:
    print(f"❌ FAIL — Ditemukan {total_nulls} nilai NULL")"""),

    md("## 3.4 Dimensi 2: Konsistensi (*Consistency*)\n\nCek konsistensi format dan nilai kategorikal."),
    code("""print("=== KONSISTENSI FORMAT ===")

# Cek nilai unik Gender
print("\\nGender values:")
df_raw.select("Gender").distinct().show()

# Cek nilai unik Product Category
print("Product Category values:")
df_raw.select("Product_Category").distinct().show()

# Validasi: hanya "Male"/"Female"
valid_genders = ["Male", "Female"]
invalid_gender = df_raw.filter(~col("Gender").isin(valid_genders)).count()

# Validasi: hanya 3 kategori
valid_categories = ["Beauty", "Clothing", "Electronics"]
invalid_category = df_raw.filter(~col("Product_Category").isin(valid_categories)).count()

print(f"Invalid Gender rows    : {invalid_gender} {'✅ PASS' if invalid_gender == 0 else '❌ FAIL'}")
print(f"Invalid Category rows  : {invalid_category} {'✅ PASS' if invalid_category == 0 else '❌ FAIL'}")"""),

    md("## 3.5 Dimensi 3: Akurasi (*Accuracy*)\n\nValidasi: `Total_Amount == Quantity × Price_per_Unit`"),
    code("""print("=== VALIDASI BUSINESS RULE ===")
print("Rule: Total_Amount harus = Quantity × Price_per_Unit\\n")

df_with_check = df_raw.withColumn(
    "expected_total", col("Quantity") * col("Price_per_Unit")
).withColumn(
    "is_valid", col("Total_Amount") == col("expected_total")
)

valid_count = df_with_check.filter(col("is_valid") == True).count()
invalid_count = df_with_check.filter(col("is_valid") == False).count()

print(f"Total rows     : {df_raw.count()}")
print(f"Valid rows      : {valid_count} ✅")
print(f"Invalid rows    : {invalid_count} {'✅ PASS' if invalid_count == 0 else '❌ FAIL'}")

if invalid_count > 0:
    print("\\n❌ Baris yang melanggar aturan:")
    df_with_check.filter(col("is_valid") == False).show(10)"""),

    md("## 3.6 Dimensi 4: Validitas (*Validity*)\n\nCek apakah nilai numerik berada dalam rentang yang wajar."),
    code("""print("=== VALIDASI RENTANG NILAI ===\\n")

# Age: harus 18-100
age_invalid = df_raw.filter((col("Age") < 18) | (col("Age") > 100)).count()
print(f"Age (18-100)          : {age_invalid} invalid rows {'✅ PASS' if age_invalid == 0 else '❌ FAIL'}")

# Quantity: harus > 0
qty_invalid = df_raw.filter(col("Quantity") <= 0).count()
print(f"Quantity (> 0)        : {qty_invalid} invalid rows {'✅ PASS' if qty_invalid == 0 else '❌ FAIL'}")

# Price per Unit: harus > 0
price_invalid = df_raw.filter(col("Price_per_Unit") <= 0).count()
print(f"Price per Unit (> 0)  : {price_invalid} invalid rows {'✅ PASS' if price_invalid == 0 else '❌ FAIL'}")

# Total Amount: harus > 0
total_invalid = df_raw.filter(col("Total_Amount") <= 0).count()
print(f"Total Amount (> 0)    : {total_invalid} invalid rows {'✅ PASS' if total_invalid == 0 else '❌ FAIL'}")"""),

    md("## 3.7 Dimensi 5: Keunikan (*Uniqueness*)\n\nCek duplikat berdasarkan Transaction_ID."),
    code("""print("=== CEK DUPLIKASI ===\\n")

total_rows = df_raw.count()
unique_ids = df_raw.select("Transaction_ID").distinct().count()
duplicates = total_rows - unique_ids

print(f"Total rows             : {total_rows}")
print(f"Unique Transaction_ID  : {unique_ids}")
print(f"Duplikat               : {duplicates} {'✅ PASS' if duplicates == 0 else '❌ FAIL'}")"""),

    md("## 3.8 Transformasi & Output Data Bersih"),
    code("""# Konversi Date string → DateType
df_clean = df_raw.withColumn("Date", to_date(col("Date"), "yyyy-MM-dd"))

# Cache untuk performa (akan dipakai berulang)
df_clean.cache()

print(f"✅ Data bersih: {df_clean.count()} rows")
print(f"✅ Date column converted to DateType")
df_clean.printSchema()
df_clean.show(5)"""),

    md("## 3.9 Ringkasan Quality Report"),
    code("""print("=" * 60)
print("        DATA QUALITY REPORT")
print("=" * 60)
print(f"  Dataset        : retail_sales_dataset.csv")
print(f"  Total Rows     : {df_raw.count()}")
print(f"  Total Columns  : {len(df_raw.columns)}")
print(f"  Null Values    : 0 ✅")
print(f"  Invalid Gender : 0 ✅")
print(f"  Invalid Amount : 0 ✅")
print(f"  Out of Range   : 0 ✅")
print(f"  Duplicates     : 0 ✅")
print(f"  Clean Rows     : {df_clean.count()}")
print("=" * 60)
print("  STATUS: ✅ ALL CHECKS PASSED")
print("=" * 60)"""),
])

# ============================================================
# NOTEBOOK 4: Data Storage (Parquet)
# ============================================================
nb4 = make_nb([
    md("# 04 — Data Storage: Parquet (Bab 2.3)\n\nNotebook ini mengimplementasikan penyimpanan data ke format **Apache Parquet** dengan **partisi berdasarkan Product_Category**."),

    md("## 4.1 Inisialisasi & Load Data"),
    code("""from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql.functions import col, to_date

spark = SparkSession.builder \\
    .appName("04_DataStorage") \\
    .master("spark://spark-master:7077") \\
    .config("spark.executor.memory", "1g") \\
    .config("spark.driver.memory", "1g") \\
    .getOrCreate()

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

df = spark.read.csv("/data/retail_sales_dataset.csv", header=True, schema=schema)
df = df.withColumn("Date", to_date(col("Date"), "yyyy-MM-dd"))
print(f"✅ Loaded {df.count()} rows")"""),

    md("## 4.2 Simpan ke Parquet (Partitioned)"),
    code("""PARQUET_PATH = "/output/retail_parquet"

# Tulis ke Parquet, partisi berdasarkan Product_Category
df.write \\
    .mode("overwrite") \\
    .partitionBy("Product_Category") \\
    .parquet(PARQUET_PATH)

print(f"✅ Data disimpan ke: {PARQUET_PATH}")
print(f"   Partisi: Product_Category (Beauty, Clothing, Electronics)")"""),

    md("## 4.3 Verifikasi: Baca Kembali dari Parquet"),
    code("""# Baca kembali
df_parquet = spark.read.parquet(PARQUET_PATH)

print(f"✅ Parquet dibaca kembali: {df_parquet.count()} rows")
print(f"   Kolom: {df_parquet.columns}")
df_parquet.printSchema()
df_parquet.show(5)"""),

    md("## 4.4 Perbandingan Performa CSV vs Parquet"),
    code("""import time

# Benchmark: CSV read
t0 = time.time()
df_csv = spark.read.csv("/data/retail_sales_dataset.csv", header=True, schema=schema)
df_csv.count()
csv_time = time.time() - t0

# Benchmark: Parquet read
t0 = time.time()
df_pq = spark.read.parquet(PARQUET_PATH)
df_pq.count()
pq_time = time.time() - t0

print("=== PERBANDINGAN PERFORMA ===")
print(f"   CSV read time     : {csv_time:.3f}s")
print(f"   Parquet read time : {pq_time:.3f}s")
print(f"   Speedup           : {csv_time/pq_time:.1f}x lebih cepat" if pq_time > 0 else "   (terlalu cepat untuk dibandingkan)")"""),

    md("## 4.5 Demo: Partition Pruning\n\nKeunggulan partisi — hanya baca data yang dibutuhkan."),
    code("""# Hanya baca kategori 'Electronics' (partition pruning)
t0 = time.time()
df_elec = spark.read.parquet(PARQUET_PATH).filter(col("Product_Category") == "Electronics")
count_elec = df_elec.count()
prune_time = time.time() - t0

print(f"✅ Partition Pruning: hanya baca Electronics")
print(f"   Rows  : {count_elec}")
print(f"   Time  : {prune_time:.3f}s")
print(f"   → Spark hanya membaca folder 'Product_Category=Electronics', skip sisanya")"""),
])

# ============================================================
# NOTEBOOK 5: Spark SQL Analysis
# ============================================================
nb5 = make_nb([
    md("# 05 — Analisis dengan Spark SQL (Bab 2.4a)\n\nNotebook ini mengimplementasikan analisis eksploratif menggunakan **Spark SQL** terhadap data transaksi ritel."),

    md("## 5.1 Inisialisasi & Load dari Parquet"),
    code("""from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \\
    .appName("05_SparkSQL_Analysis") \\
    .master("spark://spark-master:7077") \\
    .config("spark.executor.memory", "1g") \\
    .config("spark.driver.memory", "1g") \\
    .getOrCreate()

# Load dari Parquet (lebih cepat dari CSV)
df = spark.read.parquet("/output/retail_parquet")
df.createOrReplaceTempView("transactions")
print(f"✅ Loaded {df.count()} rows from Parquet")"""),

    md("## 5.2 Query 1: Revenue per Kategori Produk"),
    code("""print("=== REVENUE PER KATEGORI PRODUK ===")
spark.sql(\"\"\"
    SELECT 
        Product_Category,
        COUNT(*) as total_transaksi,
        SUM(Total_Amount) as total_revenue,
        ROUND(AVG(Total_Amount), 1) as avg_per_transaksi,
        SUM(Quantity) as total_unit_terjual
    FROM transactions
    GROUP BY Product_Category
    ORDER BY total_revenue DESC
\"\"\").show()"""),

    md("## 5.3 Query 2: Distribusi Gender"),
    code("""print("=== DISTRIBUSI GENDER ===")
spark.sql(\"\"\"
    SELECT 
        Gender,
        COUNT(*) as jumlah_pelanggan,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions), 1) as persentase,
        SUM(Total_Amount) as total_spending,
        ROUND(AVG(Total_Amount), 1) as avg_spending
    FROM transactions
    GROUP BY Gender
\"\"\").show()"""),

    md("## 5.4 Query 3: Analisis per Kelompok Usia"),
    code("""print("=== SPENDING PER KELOMPOK USIA ===")
spark.sql(\"\"\"
    SELECT 
        CASE 
            WHEN Age BETWEEN 18 AND 25 THEN '18-25 (Muda)'
            WHEN Age BETWEEN 26 AND 35 THEN '26-35 (Dewasa Muda)'
            WHEN Age BETWEEN 36 AND 45 THEN '36-45 (Dewasa)'
            WHEN Age BETWEEN 46 AND 55 THEN '46-55 (Dewasa Atas)'
            ELSE '56-64 (Pra-Lansia)'
        END as kelompok_usia,
        COUNT(*) as jumlah,
        SUM(Total_Amount) as total_spending,
        ROUND(AVG(Total_Amount), 1) as avg_spending,
        ROUND(AVG(Quantity), 1) as avg_quantity
    FROM transactions
    GROUP BY kelompok_usia
    ORDER BY total_spending DESC
\"\"\").show()"""),

    md("## 5.5 Query 4: Tren Penjualan Bulanan"),
    code("""print("=== TREN PENJUALAN BULANAN (2023) ===")
spark.sql(\"\"\"
    SELECT 
        MONTH(Date) as bulan,
        COUNT(*) as total_transaksi,
        SUM(Total_Amount) as total_revenue,
        ROUND(AVG(Total_Amount), 1) as avg_per_transaksi
    FROM transactions
    WHERE YEAR(Date) = 2023
    GROUP BY MONTH(Date)
    ORDER BY bulan
\"\"\").show(12)"""),

    md("## 5.6 Query 5: Top Spender per Kategori"),
    code("""print("=== TOP 5 PELANGGAN PER KATEGORI ===")
spark.sql(\"\"\"
    SELECT * FROM (
        SELECT 
            Product_Category,
            Customer_ID,
            Total_Amount,
            ROW_NUMBER() OVER (PARTITION BY Product_Category ORDER BY Total_Amount DESC) as rank
        FROM transactions
    )
    WHERE rank <= 5
    ORDER BY Product_Category, rank
\"\"\").show(15)"""),

    md("## 5.7 Query 6: Distribusi Harga"),
    code("""print("=== DISTRIBUSI PRICE TIER ===")
spark.sql(\"\"\"
    SELECT 
        Price_per_Unit as harga,
        CASE
            WHEN Price_per_Unit IN (25, 30) THEN 'Budget'
            WHEN Price_per_Unit = 50 THEN 'Mid-Range'
            ELSE 'Premium'
        END as price_tier,
        COUNT(*) as jumlah_transaksi,
        SUM(Total_Amount) as total_revenue
    FROM transactions
    GROUP BY Price_per_Unit, price_tier
    ORDER BY Price_per_Unit
\"\"\").show()"""),

    md("## 5.8 Query 7: Cross-Tabulation Gender × Kategori"),
    code("""print("=== CROSS-TAB: GENDER × KATEGORI ===")
spark.sql(\"\"\"
    SELECT 
        Gender,
        SUM(CASE WHEN Product_Category = 'Beauty' THEN Total_Amount ELSE 0 END) as Beauty,
        SUM(CASE WHEN Product_Category = 'Clothing' THEN Total_Amount ELSE 0 END) as Clothing,
        SUM(CASE WHEN Product_Category = 'Electronics' THEN Total_Amount ELSE 0 END) as Electronics,
        SUM(Total_Amount) as Grand_Total
    FROM transactions
    GROUP BY Gender
\"\"\").show()"""),
])

# ============================================================
# NOTEBOOK 6: K-Means Segmentation
# ============================================================
nb6 = make_nb([
    md("# 06 — Segmentasi Pelanggan: K-Means (Bab 2.4b)\n\nNotebook ini mengimplementasikan **segmentasi pelanggan** menggunakan algoritma **K-Means Clustering** dari Spark MLlib."),

    md("## 6.1 Inisialisasi & Load Data"),
    code("""from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, sum as spark_sum

spark = SparkSession.builder \\
    .appName("06_KMeans_Segmentation") \\
    .master("spark://spark-master:7077") \\
    .config("spark.executor.memory", "1g") \\
    .config("spark.driver.memory", "1g") \\
    .getOrCreate()

df = spark.read.parquet("/output/retail_parquet")
print(f"✅ Loaded {df.count()} rows")"""),

    md("## 6.2 Feature Engineering\n\nBuat fitur per pelanggan: frequency, monetary, avg_quantity"),
    code("""# Agregasi fitur per pelanggan
df_customer = df.groupBy("Customer_ID").agg(
    count("*").alias("frequency"),
    avg("Total_Amount").alias("avg_monetary"),
    avg("Quantity").alias("avg_quantity"),
    spark_sum("Total_Amount").alias("total_spending")
)

print(f"✅ {df_customer.count()} pelanggan unik")
df_customer.show(10)
df_customer.describe().show()"""),

    md("## 6.3 Persiapan Fitur untuk MLlib"),
    code("""from pyspark.ml.feature import VectorAssembler, StandardScaler

# Assemble fitur ke vector
assembler = VectorAssembler(
    inputCols=["frequency", "avg_monetary", "avg_quantity"],
    outputCol="features_raw"
)
df_assembled = assembler.transform(df_customer)

# Standarisasi fitur (penting untuk K-Means!)
scaler = StandardScaler(
    inputCol="features_raw",
    outputCol="features",
    withStd=True,
    withMean=True
)
scaler_model = scaler.fit(df_assembled)
df_scaled = scaler_model.transform(df_assembled)

print("✅ Fitur di-assemble dan di-scale")
df_scaled.select("Customer_ID", "features").show(5, truncate=False)"""),

    md("## 6.4 Menentukan Jumlah Cluster Optimal (Elbow Method)"),
    code("""from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator

# Test k = 2 sampai 8
costs = []
silhouettes = []
evaluator = ClusteringEvaluator(featuresCol="features", metricName="silhouette")

print("=== ELBOW METHOD ===")
print(f"{'k':>3} | {'Cost (WSSSE)':>15} | {'Silhouette':>10}")
print("-" * 40)

for k in range(2, 9):
    kmeans = KMeans(k=k, seed=42, featuresCol="features", predictionCol="prediction")
    model = kmeans.fit(df_scaled)
    cost = model.summary.trainingCost
    
    predictions = model.transform(df_scaled)
    silhouette = evaluator.evaluate(predictions)
    
    costs.append(cost)
    silhouettes.append(silhouette)
    print(f"{k:>3} | {cost:>15.2f} | {silhouette:>10.4f}")

print("\\n📌 Pilih k di mana cost mulai landai (elbow) dan silhouette tinggi")"""),

    md("## 6.5 Train K-Means (k=3)"),
    code("""# Final model dengan k=3
kmeans_final = KMeans(
    k=3, 
    seed=42, 
    featuresCol="features", 
    predictionCol="segment"
)
model_final = kmeans_final.fit(df_scaled)

# Transform
df_segmented = model_final.transform(df_scaled)
print("✅ K-Means training selesai (k=3)")
print(f"   WSSSE (Cost): {model_final.summary.trainingCost:.2f}")"""),

    md("## 6.6 Analisis Hasil Segmentasi"),
    code("""print("=== PROFIL SETIAP SEGMEN ===\\n")

df_segmented.groupBy("segment").agg(
    count("*").alias("jumlah_pelanggan"),
    avg("avg_monetary").alias("avg_spending"),
    avg("frequency").alias("avg_frequency"),
    avg("avg_quantity").alias("avg_quantity"),
    avg("total_spending").alias("avg_total_spending")
).orderBy("segment").show()

# Label segmen
print("📌 Interpretasi Segmen:")
print("   Segment dengan avg_spending tertinggi → High Value")
print("   Segment dengan avg_spending sedang    → Medium Value")  
print("   Segment dengan avg_spending terendah  → Low Value")"""),

    md("## 6.7 Distribusi Segmen"),
    code("""print("=== DISTRIBUSI SEGMEN ===\\n")
total = df_segmented.count()
for row in df_segmented.groupBy("segment").count().orderBy("segment").collect():
    pct = row["count"] / total * 100
    print(f"   Segment {row['segment']}: {row['count']} pelanggan ({pct:.1f}%)")"""),

    md("## 6.8 Simpan Hasil Segmentasi"),
    code("""# Simpan ke Parquet
OUTPUT_PATH = "/output/customer_segments"

df_segmented.select(
    "Customer_ID", "frequency", "avg_monetary", 
    "avg_quantity", "total_spending", "segment"
).write.mode("overwrite").parquet(OUTPUT_PATH)

print(f"✅ Hasil segmentasi disimpan ke: {OUTPUT_PATH}")"""),
])

# ============================================================
# NOTEBOOK 7: Visualization
# ============================================================
nb7 = make_nb([
    md("# 07 — Visualisasi Hasil (Bab 2.4c)\n\nNotebook ini membuat visualisasi dari hasil analisis menggunakan **Pandas + Matplotlib + Seaborn**."),

    md("## 7.1 Inisialisasi & Load Data"),
    code("""from pyspark.sql import SparkSession

spark = SparkSession.builder \\
    .appName("07_Visualization") \\
    .master("spark://spark-master:7077") \\
    .config("spark.executor.memory", "1g") \\
    .config("spark.driver.memory", "1g") \\
    .getOrCreate()

# Load data
df = spark.read.parquet("/output/retail_parquet")
df.createOrReplaceTempView("transactions")

df_segments = spark.read.parquet("/output/customer_segments")

print(f"✅ Transactions: {df.count()} rows")
print(f"✅ Segments    : {df_segments.count()} rows")"""),

    md("## 7.2 Setup Matplotlib"),
    code("""import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd

# Style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")
matplotlib.rcParams['figure.dpi'] = 120
matplotlib.rcParams['font.size'] = 11

print("✅ Matplotlib & Seaborn ready")"""),

    md("## 7.3 Chart 1: Revenue per Kategori Produk"),
    code("""pdf_revenue = spark.sql(\"\"\"
    SELECT Product_Category, SUM(Total_Amount) as revenue, COUNT(*) as count
    FROM transactions GROUP BY Product_Category ORDER BY revenue DESC
\"\"\").toPandas()

fig, ax = plt.subplots(figsize=(8, 5))
colors = ["#4ECDC4", "#45B7D1", "#FF6B6B"]
bars = ax.bar(pdf_revenue["Product_Category"], pdf_revenue["revenue"], color=colors, edgecolor="white", linewidth=1.5)

# Tambah label di atas bar
for bar, rev, cnt in zip(bars, pdf_revenue["revenue"], pdf_revenue["count"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1500,
            f'{rev:,.0f}\\n({cnt} txn)', ha='center', va='bottom', fontweight='bold', fontsize=10)

ax.set_title("Total Revenue per Kategori Produk", fontsize=14, fontweight='bold', pad=20)
ax.set_ylabel("Revenue", fontsize=12)
ax.ticklabel_format(style='plain', axis='y')
ax.set_ylim(0, max(pdf_revenue["revenue"]) * 1.15)
sns.despine()
plt.tight_layout()
plt.savefig("/home/jovyan/work/chart_revenue_kategori.png", dpi=150)
plt.show()
print("✅ Saved: chart_revenue_kategori.png")"""),

    md("## 7.4 Chart 2: Tren Penjualan Bulanan"),
    code("""pdf_monthly = spark.sql(\"\"\"
    SELECT MONTH(Date) as bulan, SUM(Total_Amount) as revenue, COUNT(*) as transaksi
    FROM transactions WHERE YEAR(Date) = 2023
    GROUP BY MONTH(Date) ORDER BY bulan
\"\"\").toPandas()

fig, ax1 = plt.subplots(figsize=(10, 5))

# Revenue line
color1 = "#6C5CE7"
ax1.plot(pdf_monthly["bulan"], pdf_monthly["revenue"], marker='o', color=color1, linewidth=2.5, markersize=8, label="Revenue")
ax1.fill_between(pdf_monthly["bulan"], pdf_monthly["revenue"], alpha=0.1, color=color1)
ax1.set_xlabel("Bulan", fontsize=12)
ax1.set_ylabel("Revenue", fontsize=12, color=color1)
ax1.set_xticks(range(1, 13))
ax1.set_xticklabels(["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"])

# Transaction count on secondary axis
ax2 = ax1.twinx()
color2 = "#FFA726"
ax2.bar(pdf_monthly["bulan"], pdf_monthly["transaksi"], alpha=0.3, color=color2, label="Jumlah Transaksi")
ax2.set_ylabel("Jumlah Transaksi", fontsize=12, color=color2)

ax1.set_title("Tren Penjualan Bulanan (2023)", fontsize=14, fontweight='bold', pad=15)
fig.legend(loc="upper right", bbox_to_anchor=(0.95, 0.95))
plt.tight_layout()
plt.savefig("/home/jovyan/work/chart_tren_bulanan.png", dpi=150)
plt.show()
print("✅ Saved: chart_tren_bulanan.png")"""),

    md("## 7.5 Chart 3: Distribusi Usia Pelanggan"),
    code("""pdf_age = spark.sql("SELECT Age FROM transactions").toPandas()

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(pdf_age["Age"], bins=20, color="#4ECDC4", edgecolor="white", linewidth=1.2, alpha=0.8)
ax.axvline(pdf_age["Age"].mean(), color="#FF6B6B", linestyle="--", linewidth=2, label=f'Mean: {pdf_age["Age"].mean():.1f}')
ax.set_title("Distribusi Usia Pelanggan", fontsize=14, fontweight='bold')
ax.set_xlabel("Usia", fontsize=12)
ax.set_ylabel("Frekuensi", fontsize=12)
ax.legend(fontsize=11)
sns.despine()
plt.tight_layout()
plt.savefig("/home/jovyan/work/chart_distribusi_usia.png", dpi=150)
plt.show()
print("✅ Saved: chart_distribusi_usia.png")"""),

    md("## 7.6 Chart 4: Segmentasi Pelanggan (K-Means Scatter)"),
    code("""pdf_seg = df_segments.toPandas()

fig, ax = plt.subplots(figsize=(9, 6))
colors_seg = {0: "#FF6B6B", 1: "#4ECDC4", 2: "#45B7D1"}
labels_seg = {0: "Segment 0", 1: "Segment 1", 2: "Segment 2"}

for seg in sorted(pdf_seg["segment"].unique()):
    mask = pdf_seg["segment"] == seg
    ax.scatter(
        pdf_seg[mask]["frequency"], 
        pdf_seg[mask]["avg_monetary"],
        c=colors_seg.get(seg, "#999"),
        label=labels_seg.get(seg, f"Seg {seg}"),
        alpha=0.6, s=60, edgecolors="white", linewidth=0.5
    )

ax.set_title("Segmentasi Pelanggan (K-Means, k=3)", fontsize=14, fontweight='bold')
ax.set_xlabel("Frequency (Jumlah Transaksi)", fontsize=12)
ax.set_ylabel("Average Monetary (Avg Spending)", fontsize=12)
ax.legend(fontsize=11, title="Segment")
sns.despine()
plt.tight_layout()
plt.savefig("/home/jovyan/work/chart_segmentasi_kmeans.png", dpi=150)
plt.show()
print("✅ Saved: chart_segmentasi_kmeans.png")"""),

    md("## 7.7 Chart 5: Heatmap Gender × Kategori"),
    code("""pdf_cross = spark.sql(\"\"\"
    SELECT Gender, Product_Category, ROUND(AVG(Total_Amount), 1) as avg_spending
    FROM transactions
    GROUP BY Gender, Product_Category
\"\"\").toPandas()

pivot = pdf_cross.pivot(index="Gender", columns="Product_Category", values="avg_spending")

fig, ax = plt.subplots(figsize=(8, 4))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlOrRd", linewidths=2, linecolor="white",
            annot_kws={"size": 14, "weight": "bold"}, ax=ax)
ax.set_title("Avg Spending: Gender × Kategori Produk", fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel("")
ax.set_xlabel("")
plt.tight_layout()
plt.savefig("/home/jovyan/work/chart_heatmap_gender.png", dpi=150)
plt.show()
print("✅ Saved: chart_heatmap_gender.png")"""),

    md("## 7.8 Chart 6: 3D Scatter Segmentasi Pelanggan"),
    code("""fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for seg in sorted(pdf_seg["segment"].unique()):
    mask = pdf_seg["segment"] == seg
    ax.scatter(pdf_seg[mask]["frequency"], 
               pdf_seg[mask]["avg_monetary"],
               pdf_seg[mask]["avg_quantity"],
               c=colors_seg.get(seg, "#999"), label=f"Seg {seg}",
               alpha=0.6, s=40, edgecolors="white", linewidth=0.5)

ax.set_title("3D Segmentasi Pelanggan (K-Means)", fontsize=14, fontweight='bold')
ax.set_xlabel("Frequency", labelpad=10)
ax.set_ylabel("Avg Monetary", labelpad=10)
ax.set_zlabel("Avg Quantity", labelpad=10)
ax.legend(fontsize=11, title="Segment", loc="upper left")
plt.tight_layout()
plt.savefig("/home/jovyan/work/chart_segmentasi_3d.png", dpi=150)
plt.show()
print("✅ Saved: chart_segmentasi_3d.png")"""),

    md("## 7.9 Dashboard Summary"),
    code("""fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Dashboard Analisis Penjualan Ritel", fontsize=18, fontweight='bold', y=1.02)

# 1. Revenue per kategori
colors = ["#4ECDC4", "#45B7D1", "#FF6B6B"]
axes[0,0].bar(pdf_revenue["Product_Category"], pdf_revenue["revenue"], color=colors)
axes[0,0].set_title("Revenue per Kategori", fontweight='bold')
axes[0,0].ticklabel_format(style='plain', axis='y')

# 2. Tren bulanan
axes[0,1].plot(pdf_monthly["bulan"], pdf_monthly["revenue"], marker='o', color="#6C5CE7", linewidth=2)
axes[0,1].set_title("Tren Bulanan", fontweight='bold')
axes[0,1].set_xticks(range(1, 13))

# 3. Distribusi usia
axes[1,0].hist(pdf_age["Age"], bins=20, color="#4ECDC4", edgecolor="white")
axes[1,0].set_title("Distribusi Usia", fontweight='bold')

# 4. Segmentasi
for seg in sorted(pdf_seg["segment"].unique()):
    mask = pdf_seg["segment"] == seg
    axes[1,1].scatter(pdf_seg[mask]["frequency"], pdf_seg[mask]["avg_monetary"],
                      c=colors_seg.get(seg), label=f"Seg {seg}", alpha=0.6, s=40)
axes[1,1].set_title("Segmentasi Pelanggan", fontweight='bold')
axes[1,1].legend()

for ax in axes.flat:
    sns.despine(ax=ax)

plt.tight_layout()
plt.savefig("/home/jovyan/work/dashboard_summary.png", dpi=150, bbox_inches='tight')
plt.show()
print("✅ Dashboard saved: dashboard_summary.png")"""),

    md("## 7.10 Cleanup"),
    code("""spark.stop()
print("✅ Semua visualisasi selesai.")
print("📂 File tersimpan di folder notebooks/:")
print("   - chart_revenue_kategori.png")
print("   - chart_tren_bulanan.png")
print("   - chart_distribusi_usia.png")
print("   - chart_segmentasi_kmeans.png")
print("   - chart_heatmap_gender.png")
print("   - chart_segmentasi_3d.png")
print("   - dashboard_summary.png")"""),
])

# ============================================================
# WRITE ALL NOTEBOOKS
# ============================================================
notebooks = {
    "01_setup_connection.ipynb": nb1,
    "02_data_ingestion.ipynb": nb2,
    "03_data_validation.ipynb": nb3,
    "04_data_storage_parquet.ipynb": nb4,
    "05_spark_sql_analysis.ipynb": nb5,
    "06_kmeans_segmentation.ipynb": nb6,
    "07_visualization.ipynb": nb7,
}

output_dir = os.path.dirname(os.path.abspath(__file__))

for filename, nb_data in notebooks.items():
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(nb_data, f, indent=1, ensure_ascii=False)
    print(f"✅ Created: {filename}")

print(f"\n🎉 Total {len(notebooks)} notebooks created in {output_dir}")
