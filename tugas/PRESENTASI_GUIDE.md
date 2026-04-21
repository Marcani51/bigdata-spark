# Skenario Presentasi: Solusi Analitik Big Data Ritel
**Estimasi Waktu**: 15 - 20 Menit

Dokumen ini adalah panduan langkah demi langkah (skenario) untuk mempresentasikan project Solusi Big Data Anda kepada dosen atau *stakeholder* terkait. Menggabungkan perspektif bisnis dan pamernya sisi arsitektur teknis.

---

## 💻 Persiapan Sebelum Presentasi (Standby di Layar)

Sebelum mulai *share screen* atau presentasi, pastikan Anda telah membuka tab-tab berikut agar transisi dari menceritakan teori hingga mendemokan eksekusinya terlihat mulus:

1. **Terminal / VS Code**: Buka dan ketik `docker-compose ps` untuk menunjukkan bukti nyata bahwa *cluster processing* (Master, Worker, dlsb) sedang aktif berjalan.
2. **Tab 1 - Dokumen/PPT**: Berisi latar belakang masalah atau diagram arsitektur.
3. **Tab 2 - Spark UI (http://localhost:8080)**: Untuk memamerkan kapabilitas Master dan Worker.
4. **Tab 3 - Jupyter Lab (http://localhost:8888)**: Buka kode `pipeline.ipynb` untuk demo proses Engineering-nya.
5. **Tab 4 - Dashboard (http://localhost:8501)**: Sediakan Streamlit dashboard yang sudah siap jalan untuk presentasi akhir yang lebih *business-oriented*.

---

## 🎬 Skenario Berjalan (Step-by-step)

### 1. Pembukaan & Latar Belakang (⏱️ 2-3 Menit)
*🎯 Fokus: Menjawab **"Mengapa project ini ada?"***  
*📺 Menampilkan: Laporan (Bab 1) / Slide PPT Latar Belakang.*

* **Ucapan**: 
  > "Selamat pagi/siang, izinkan saya mempresentasikan Solusi Analitik Big Data untuk meneliti segmentasi dan perilaku belanja konsumen di industri ritel. Kami memanfaatkan dataset bersumber dari Kaggle yang mencakup 1.000 rekaman transaksi konsumen statis."
* **Poin Kunci**:
  * Industri ritel modern menghasilkan volume data berlebih. Alat tradisional (seperti excel biasa) lambat mengolah wawasan.
  * Masalah Utama: **Membedah perilaku belanja personal setiap klien** untuk mencegah promosi yang tidak tepat sasaran / *budget marketing* yang terbuang sia-sia.

### 2. Arsitektur Teknis & Keamanan Data (⏱️ 3-4 Menit)
*🎯 Fokus: Membuktikan bobot teknis bahwa sistem ini menggunakan arsitektur standard-industri.*  
*📺 Menampilkan: Menunjukkan bagian gambaran Arsitektur (Bisa dari Laporan Bab 2 / SETUP_GUIDE).*

* **Ucapan**:
  > "Untuk merespon skalabilitas ke depannya, kami mendesain arsitektur menggunakan Apache Spark dengan sistem Master/Worker di dalam lingkungan containerized Docker."
* **Poin Kunci**:
  * Alur: CSV Lokal -> Diproses berantai oleh PySpark -> di Load ke Parquet -> dibaca visualisasinya di Dashboard.
  * **(Nilai Plus) IT Governance**: Sertakan juga *Data Privacy*. Katakan: *"Kami menjunjung privasi dengan melakukan pseudonimisasi ID Customer, mematuhi standar perlindungan privasi yang ada agar data klien aman saat melakukan segmentasi/clustering."*

### 3. Demo Data Pipeline & Engineering (⏱️ 5-7 Menit)
*🎯 Fokus: Pamerkan "Dapur" pengolahan dan machine learning (Data Engineering).*  
*📺 Menampilkan: Spark UI, kemudian pindah ke Jupyter Notebook.*

* **Visual Pertama (Spark UI)**: Tunjukkan di browser.
  > "Bisa dilihat di layar, job kita diproses dan didelegasikan secara mulus. Eksekusinya mengadopsi ekosistem *distributed cluster*, merepresentasikan bagaimana Big Data bekerja secara murni."
* **Visual Kedua (Jupyter Notebook)**, *Scroll* perlahan untuk poin-poin berikut:
  1. **Ingestion & Validation**: "Berikut blok kode di mana program menyaring data, menendang baris *null* serta mengecek keabsahan kalkulasi (`Total_Amount = Quantity * Price`). Kami secara eksplisit memvalidasi skema sejak awal."
  2. **Data Storage (Parquet)**: Tunjukkan blok *writer* ke Parquet format. Sebutkan bahwa cara simpan *columnar* ini menghemat ukuran simpan hingga 70%.
  3. **SQL Analytics**: Perlihatkan contoh query SQL yang dipakai Spark.
  4. **Machine Learning Tool**: *Ini bagian Krusial.* Tunjukkan blok Pyspark `MLlib` dengan Algoritma K-Means. *"Kami mengkluster pelanggan ke kelompok 3 segmen nilai langsung murni me-utilisasi ekosistem dalam Spark tanpa perlu aplikasi machine learning eksternal pihak ke tiga."*

### 4. Puncak Presentasi / Showcase (⏱️ 4-5 Menit)
*🎯 Fokus: Demo sisi bisnis (Executive Report).*  
*📺 Menampilkan: Streamlit Dashboard di browser.*

* **Ucapan**: 
  > "Seluruh kapabilitas infrastruktur rumit di balik layar tadi membuahkan output yang *ready-to-use* layaknya *executive real-time dashboard* ini."
* **Pamerkan Interaktifnya**:
  * Pamerkan **KPI Cards**.
  * Klik filter *sidebar*. Ubah Kategori misalnya, lalu minta saksi/presentator lawan mengecek grafik diagram secara instan terubah *real-time*.
  * Sorot **Grafik Segmentasi**. Katakan, *"Dari visual data ini, manajemen bisa merumuskan *Demand Forecasting* per-kategori spesifik sekaligus mendeteksi *Customer Lifetime Value* dari segmentasi yang terbukti tinggi daya uang belanjanya."*

### 5. Penutup (⏱️ 1-2 Menit)
*🎯 Fokus: Dampak project dan *Long-term Mindset*.*  
*📺 Menampilkan: PPT Titik Kesimpulan / Biarkan pada Layar Dashboard.*

* **Ucapan / Poin**:
  > "Terima kasih, kesimpulannya, arsitektur yang kami terapkan tidak sekedar membabat dataset 1.000 baris. Model PySpark yang sudah berdiri ini adalah fondasi matang yang mampu menampung jutaan baris *historical data* apabila disuntik besok—tanpa merombak kode. Ini membuktikan wujud nyata pengarsitekturan Big Data dan implementasi Machine Learning yang bisa dijadikan acuan aksi *campaign* di level manajemen." 

---

## 💡 "Bonus Hacks" Cara Jawab saat Q&A (Tanya Jawab)

*   **Tanya**: *"Mengapa tidak pakai Pandas Python biasa aja? Kan Datanya kecil cuma 1.000 baris CSV?"*
    > **Jawab**: "Betul, Pandas cukup untuk 1.000 baris, tetapi ini adalah studi perancangan (*design approach*) untuk skenario 'Big Data'. Pandas berjalan pada struktur '*monolithic/single-node*', jika bulan depan data naik ke 100 Juta Transaksi maka program akan *Crash Out of Memory*. Dengan Spark Master-Worker, kita mensimulasikan lingkungan terdistribusi yang sangat scalable; program yang sama tetap jalan lancar tanpa macet hanya bermodal menancapkan server worker baru ke jaringan."
*   **Tanya**: *"Tadi kamu ganti dari CSV ke file Parquet, apa fungsi nyatanya?"*
    > **Jawab**: "Parquet bersifat '*Columnar*'. Ketika Streamlit Dashboard hanya meminta total Revenue, Parquet menyuplai **satu persis kolom** tersebut tanpa harus bersusah payah me-*load* kolom usia atau gender yang memakan Memory PC. Operasi IO read-nya jadi jauh lebih kencang dibanding membaca ulang CSV."

Semoga sukses presentasinya!
