# Arsitektur Solusi Big Data (Bab 2)

Berikut adalah diagram arsitektur solusi Big Data yang dirancang menggunakan PySpark, mulai dari tahap pengumpulan data hingga visualisasi. Anda dapat mempratinjau diagram ini menggunakan Markdown previewer yang mendukung Mermaid (seperti GitHub atau plugin VSCode).

```mermaid
flowchart LR
    %% Pengaturan Gaya
    classDef source fill:#f3f4f6,stroke:#4b5563,stroke-width:2px,color:#1f2937,font-weight:bold
    classDef ingest fill:#fef3c7,stroke:#d97706,stroke-width:2px,color:#92400e
    classDef storage fill:#e0f2fe,stroke:#0284c7,stroke-width:2px,color:#075985
    classDef process fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#1e40af
    classDef viz fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#166534

    %% 1. Sumber Data
    subgraph Fase1 ["1. Pengumpulan Data"]
        A[("retail_sales_dataset.csv\n(Kaggle Public Dataset)")]:::source
    end

    %% 2. Data Ingestion
    subgraph Fase2 ["2. Data Ingestion (Batch)"]
        direction TB
        B("PySpark Load\n[spark.read.csv]"):::ingest
        C("Validasi & Transformasi\n- InferSchema\n- Null Check\n- Date Casting"):::ingest
        B --> C
    end

    %% 3. Data Storage
    subgraph Fase3 ["3. Penyimpanan (Data Storage)"]
        direction TB
        D[("Spark DataFrame\n(In-Memory)")]:::storage
        E[("Apache Parquet\n(Persistent & Partitioned)")]:::storage
    end

    %% 4. Processing Framework
    subgraph Fase4 ["4. Pemrosesan (Processing Framework)"]
        direction TB
        F("Spark SQL\n(Analisis Eksploratif & SQL)"):::process
        G("Spark MLlib\n(K-Means & FP-Growth)"):::process
    end

    %% 5. Visualisasi
    subgraph Fase5 ["5. Visualisasi & Laporan"]
        H("Pandas DataFrame\n[.toPandas()]"):::viz
        I("Matplotlib & Seaborn\n[Grafik, Hist, Chart]"):::viz
    end

    %% Relasi antar fase
    A ==> B
    C ==> D
    D <==>|Cache / Write| E
    D ==> F
    D ==> G
    F ==> H
    G ==> H
    H --> I
```

### Penjelasan Setiap Fase (Berdasarkan Bab 2):

1. **Pengumpulan Data:** Menggunakan sumber data statis dari berkas `retail_sales_dataset.csv` berisi transaksi ritel harian.
2. **Data Ingestion:** Pemrosesan secara _batch_ di mana data diserap oleh PySpark menggunakan `spark.read.csv`. Setelahnya, dilakukan pembersihan data seperti pengecekan nilai null dan pengubahan format teks ke _DateType_.
3. **Penyimpanan:** Data dalam memori disimpan sebagai **Spark DataFrame** untuk pemrosesan super cepat. Untuk penyimpanan permanen, data disimpan menggunakan struktur **Apache Parquet** yang dikompresi dan dipartisi.
4. **Pemrosesan:** Dibagi menjadi dua fungsi utama, yaitu **Spark SQL** untuk manipulasi data (agregasi pemasaran harian/bulanan) dan **Spark MLlib** untuk pembuatan model (segmentasi pelanggan dan asosiasi belanja).
5. **Visualisasi:** Setelah data diolah terdistribusi dengan Spark, hasil yang ukurannya sudah merepresentasikan agregat/kesimpulan *(insight)* dikonversi ke **Pandas** melalui `.toPandas()`, kemudian divisualisasikan dengan **Matplotlib/Seaborn** ke manajer dan pemangku kepentingan lainnya.
