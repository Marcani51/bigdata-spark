# Dashboard Guide — Retail Analytics Dashboard

Panduan untuk menjalankan **Dashboard Interaktif** yang menampilkan hasil analisis Big Data dari pipeline PySpark.

---

## Arsitektur

```
┌─────────────────────────────────────────────────────────────┐
│                      Docker Network                          │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │  Spark   │  │  Spark   │  │ Jupyter  │  │ Streamlit  │  │
│  │  Master  │  │  Worker  │  │ Notebook │  │ Dashboard  │  │
│  │  :8080   │  │  :8081   │  │  :8888   │  │   :8501    │  │
│  └──────────┘  └──────────┘  └────┬─────┘  └─────┬──────┘  │
│                                    │              │          │
│                              ┌─────▼──────────────▼─────┐   │
│                              │  /data/   (CSV sumber)   │   │
│                              │  /output/ (Parquet hasil) │   │
│                              └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Alur data:**
```
CSV → Notebook PySpark (04, 06) → Parquet → Dashboard Streamlit → Browser
```

---

## Prasyarat

Pastikan semua notebook sudah pernah dijalankan minimal sekali:

| Notebook | Status | Output yang dihasilkan |
|---|---|---|
| 04_data_storage_parquet | ✅ Wajib | `/output/retail_parquet/` |
| 06_kmeans_segmentation | ✅ Wajib | `/output/customer_segments/` |

> 💡 Dashboard tetap bisa jalan **tanpa output Parquet** (akan fallback baca CSV langsung), tapi segmentasi K-Means tidak akan muncul.

---

## Cara Jalankan

### Step 1: Build & Start Dashboard

```bash
cd bigdatatugas/dockerspark

# Build image dashboard + jalankan semua service
docker compose up -d --build
```

Tunggu sampai build selesai (~1-2 menit pertama kali karena install dependencies).

### Step 2: Cek Status

```bash
docker compose ps
```

Pastikan semua service `Up`:
```
NAME              STATUS
spark-master      Up
spark-worker      Up
spark-jupyter     Up (healthy)
spark-dashboard   Up (healthy)    ← ini dashboard
```

### Step 3: Buka Dashboard

Buka browser → **http://localhost:8501**

---

## Akses Semua Service

| Service | URL | Fungsi |
|---|---|---|
| 🎯 **Dashboard** | **http://localhosket:8501** | Dashboard interaktif |
| 📓 Jupyter | http://localhost:8888 | Notebook PySpark |
| ⚙️ Spark Master | http://localhost:8080 | Monitoring cluster |
| 🔧 Spark Worker | http://localhost:8081 | Monitoring worker |

---

## Fitur Dashboard

### 1. KPI Cards (Baris Atas)

5 metrik utama yang update otomatis saat filter berubah:

| KPI | Deskripsi |
|---|---|
| Total Revenue | Total pendapatan (semua transaksi) |
| Total Transaksi | Jumlah transaksi |
| Avg per Transaksi | Rata-rata nilai per transaksi |
| Pelanggan Unik | Jumlah pelanggan berbeda |
| Avg Quantity | Rata-rata item per transaksi |

### 2. Analisis Penjualan

- **Revenue per Kategori** — Bar chart horizontal (Beauty, Clothing, Electronics)
- **Tren Bulanan** — Line chart revenue + bar chart jumlah transaksi (dual axis)

### 3. Analisis Demografi

- **Revenue by Gender** — Donut chart (Male vs Female)
- **Distribusi Usia** — Histogram dengan garis mean
- **Avg Spending per Usia** — Bar chart per kelompok usia

### 4. Analisis Mendalam

- **Heatmap Gender × Kategori** — Rata-rata spending per kombinasi
- **Revenue per Price Tier** — Budget / Mid-Range / Premium

### 5. Segmentasi Pelanggan (K-Means)

> ⚠️ Hanya muncul jika notebook 06 sudah dijalankan

- **Scatter Plot** — Pelanggan diplot berdasarkan frequency vs avg spending
- **Profil Segmen** — Deskripsi setiap segment (jumlah, avg spend, freq)

### 6. Data Explorer

- Tabel data mentah (expandable)
- Menampilkan 100 baris pertama setelah filter

---

## Sidebar Filter (Interaktif)

Semua chart berubah otomatis saat filter diubah:

| Filter | Opsi |
|---|---|
| Kategori Produk | Beauty, Clothing, Electronics (multiselect) |
| Gender | Male, Female (multiselect) |
| Rentang Usia | 18–64 (slider) |
| Bulan | Jan–Des (multiselect) |

**Contoh penggunaan:**
- Pilih hanya "Electronics" + "Male" → lihat perilaku belanja pria di elektronik
- Set usia 18-30 → lihat pola belanja anak muda

---

## Perintah Operasional

### Start / Stop

```bash
# Jalankan semua (termasuk dashboard)
docker compose up -d

# Jalankan dashboard saja
docker compose up -d dashboard

# Stop semua
docker compose down

# Rebuild dashboard (setelah edit app.py)
docker compose up -d --build dashboard
```

### Lihat Log

```bash
# Log dashboard
docker compose logs -f dashboard

# Log semua service
docker compose logs -f
```

### Cek Resource

```bash
docker stats
```

---

## Memory Budget

| Container | Memory | Fungsi |
|---|---|---|
| spark-master | 1 GB | Koordinasi cluster |
| spark-worker | 2 GB | Eksekusi Spark job |
| jupyter | 2 GB | PySpark + Notebook |
| **dashboard** | **512 MB** | Streamlit web app |
| **Total** | **~5.5 GB** | Sisa ~10.5 GB untuk macOS |

---

## Troubleshooting

| Masalah | Solusi |
|---|---|
| Dashboard tidak bisa diakses | `docker compose logs dashboard` cek error |
| Build gagal | Cek koneksi internet (perlu download pip packages) |
| Segmentasi tidak muncul | Jalankan notebook 06 dulu, lalu refresh dashboard |
| Chart kosong setelah filter | Filter terlalu ketat, coba reset filter |
| Port 8501 sudah dipakai | Ubah port di docker-compose: `"8502:8501"` |
| Dashboard lambat | Refresh halaman (Ctrl+R), data di-cache otomatis |

---

## Edit Dashboard

File dashboard ada di: `dockerspark/dashboard/app.py`

Setelah edit, rebuild:
```bash
docker compose up -d --build dashboard
```

---

## Struktur File

```
dockerspark/
├── docker-compose.yml
├── data/
│   └── retail_sales_dataset.csv
├── output/
│   ├── retail_parquet/          ← Dari notebook 04
│   └── customer_segments/      ← Dari notebook 06
├── notebooks/
│   ├── 01_setup_connection.ipynb
│   ├── 02_data_ingestion.ipynb
│   ├── 03_data_validation.ipynb
│   ├── 04_data_storage_parquet.ipynb
│   ├── 05_spark_sql_analysis.ipynb
│   ├── 06_kmeans_segmentation.ipynb
│   └── 07_visualization.ipynb
└── dashboard/
    ├── Dockerfile
    ├── requirements.txt
    └── app.py                  ← Kode dashboard
```
