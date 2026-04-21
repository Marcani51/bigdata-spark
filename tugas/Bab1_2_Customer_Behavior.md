# Laporan Rancangan Solusi Big Data
**Topik:** Analisis Perilaku Belanja Pelanggan pada Sektor Ritel Menggunakan Dataset Kaggle (*Customer Behavior Analysis in Retail*)

**Sumber Data:** `retail_sales_dataset.csv` — Kaggle Public Dataset

---

## Bab 1: Pendahuluan

### 1.1 Latar Belakang Masalah

Industri ritel global tengah mengalami transformasi fundamental yang didorong oleh ledakan volume data transaksional. Setiap hari, ribuan hingga jutaan rekaman transaksi dihasilkan dari berbagai kanal penjualan — baik toko fisik (*brick-and-mortar*) maupun platform daring (*e-commerce*). Data tersebut merepresentasikan jejak digital perilaku konsumen yang sangat berharga, namun sekaligus menimbulkan tantangan signifikan dalam hal pengelolaan, penyimpanan, dan analisis.

Permasalahan inti yang diangkat dalam laporan ini berfokus pada ketidakmampuan sistem analitik konvensional dalam mengekstraksi wawasan (*insight*) bermakna dari himpunan data transaksi ritel berskala besar secara efisien dan tepat waktu. Basis data relasional tradisional yang beroperasi pada arsitektur monolitik (*single-node*) menghadapi hambatan serius ketika volume data melampaui kapasitas pemrosesan vertikal, sehingga proses segmentasi pelanggan, analisis tren pembelian, dan peramalan permintaan menjadi lambat dan tidak akurat.

Dataset yang digunakan dalam studi ini bersumber dari Kaggle, yaitu `retail_sales_dataset.csv`, yang memuat **1.000 rekaman transaksi** dari **1.000 pelanggan unik** dalam rentang periode **1 Januari 2023 hingga 1 Januari 2024**. Dataset ini mencakup informasi demografis pelanggan (usia, jenis kelamin), kategori produk yang dibeli (Beauty, Clothing, Electronics), kuantitas pembelian, harga per unit, serta total nilai transaksi. Meskipun skala dataset ini tergolong moderat untuk keperluan demonstrasi akademis, arsitektur solusi yang dirancang dalam laporan ini diproyeksikan untuk mampu menangani skala data yang jauh lebih besar dalam skenario produksi nyata.

Urgensi penyelesaian masalah ini terletak pada fakta bahwa pemahaman mendalam terhadap perilaku belanja pelanggan secara langsung memengaruhi kemampuan peritel dalam mengoptimalkan strategi pemasaran, mengelola persediaan barang, dan meningkatkan loyalitas pelanggan. Tanpa kapabilitas analitik skala besar, perusahaan ritel berisiko kehilangan daya saing karena gagal mendeteksi pergeseran preferensi konsumen, meningkatnya tingkat perpindahan pelanggan (*churn*), serta inefisiensi dalam alokasi anggaran promosi.

Sebagai ilustrasi konkret, dataset ini menunjukkan bahwa total pendapatan transaksi mencapai **Rp456.000** (dalam satuan harga dataset) dengan distribusi yang relatif merata di antara tiga kategori produk: Electronics (Rp156.905), Clothing (Rp155.580), dan Beauty (Rp143.515). Analisis Big Data memungkinkan identifikasi pola — misalnya, segmen pelanggan tertentu berdasarkan kelompok usia atau jenis kelamin yang memiliki kecenderungan belanja lebih tinggi pada kategori spesifik — sehingga strategi promosi dapat dirancang secara terpersonalisasi dan efisien.

### 1.2 Konteks Bisnis dan Penggerak Pasar (*Market and Business Drivers*)

Lanskap bisnis ritel pada era digital saat ini dibentuk oleh sejumlah penggerak pasar (*market drivers*) yang secara kumulatif menuntut adopsi solusi berbasis Big Data. Pertama, **intensifikasi persaingan antar-peritel** yang dipicu oleh proliferasi platform *e-commerce* dan *marketplace* digital memaksa setiap pelaku usaha untuk memahami pelanggannya secara granular dan personal. Kedua, **ekspektasi konsumen yang terus meningkat** terhadap pengalaman belanja yang dipersonalisasi — mulai dari rekomendasi produk yang relevan hingga penawaran harga dinamis (*dynamic pricing*) — menuntut kemampuan analitik yang melampaui kapasitas alat bantu tradisional berbasis *spreadsheet* atau *query* SQL sederhana.

Ketiga, **kebutuhan efisiensi operasional** dalam manajemen rantai pasok (*supply chain*) mengharuskan peritel memiliki kemampuan peramalan permintaan (*demand forecasting*) yang akurat. Penumpukan stok barang yang tidak terjual (*overstock*) maupun kehabisan stok (*stockout*) sama-sama merugikan dari sisi finansial. Keempat, **dorongan untuk meningkatkan *Customer Lifetime Value* (CLV)** dan menurunkan *Customer Acquisition Cost* (CAC) menjadikan analisis perilaku belanja sebagai fondasi strategis yang tidak dapat diabaikan.

Implementasi solusi Big Data dalam konteks ini bukan sekadar proyek teknologi informasi, melainkan investasi strategis dengan pengembalian (*Return on Investment* / ROI) yang terukur. Berdasarkan karakteristik dataset yang digunakan, di mana rata-rata nilai transaksi per pelanggan sebesar **456,0** (satuan harga dataset) dengan kuantitas rata-rata **2,5 item per transaksi**, analisis segmentasi pelanggan berbasis pendekatan RFM (*Recency, Frequency, Monetary*) memungkinkan peritel mengalokasikan sumber daya promosi secara presisi — memberikan insentif yang lebih besar kepada segmen pelanggan bernilai tinggi (*High Value*) ketimbang menerapkan diskon massal yang tidak efisien.

Distribusi demografis dalam dataset menunjukkan komposisi gender yang hampir seimbang (**490 pelanggan laki-laki** dan **510 pelanggan perempuan**) dengan rentang usia **18 hingga 64 tahun** (rata-rata 41,4 tahun). Data ini mengindikasikan potensi segmentasi multi-dimensi yang kaya: peritel dapat merancang strategi pemasaran yang berbeda untuk segmen usia muda (18–30 tahun) yang mungkin lebih responsif terhadap kampanye digital, dibandingkan segmen usia dewasa (45–64 tahun) yang mungkin memerlukan pendekatan komunikasi yang berbeda.

### 1.3 Pemangku Kepentingan (*Stakeholders*)

Keberhasilan implementasi solusi Big Data untuk analisis perilaku pelanggan ritel mensyaratkan keterlibatan aktif dan terkoordinasi dari beberapa pemangku kepentingan utama dalam organisasi. Setiap pemangku kepentingan memiliki kebutuhan informasi dan ekspektasi luaran yang berbeda, sehingga desain arsitektur solusi harus mampu mengakomodasi seluruh kebutuhan tersebut secara simultan.

**1. Manajer Pemasaran (*Chief Marketing Officer* / CMO)**

Pemangku kepentingan ini membutuhkan wawasan terperinci mengenai profil dan segmentasi pelanggan guna merancang kampanye pemasaran yang terpersonalisasi. Dari perspektif dataset yang digunakan, CMO memerlukan analisis distribusi pembelian berdasarkan kategori produk (Beauty: 307 transaksi, Clothing: 351 transaksi, Electronics: 342 transaksi), pola pembelian berdasarkan demografi (usia dan jenis kelamin), serta identifikasi segmen pelanggan dengan nilai transaksi tertinggi. Informasi ini memungkinkan CMO mengoptimalkan alokasi anggaran iklan dan merancang program loyalitas yang tepat sasaran.

**2. Manajer Operasional dan Rantai Pasok (*Chief Operating Officer* / COO)**

COO membutuhkan hasil peramalan permintaan (*demand forecasting*) dan analisis tren penjualan temporal untuk memastikan ketersediaan stok barang yang optimal. Data transaksi harian sepanjang periode Januari 2023 hingga Januari 2024 memungkinkan identifikasi pola musiman (*seasonality*) dan fluktuasi permintaan, sehingga pengadaan barang dapat direncanakan secara proaktif. Harga per unit dalam dataset yang bervariasi pada lima tingkatan (25, 30, 50, 300, dan 500) mengindikasikan segmentasi produk berdasarkan rentang harga yang dapat dimanfaatkan untuk strategi pengadaan diferensial.

**3. Divisi Ilmu Data dan Rekayasa Data (*Data Science & Data Engineering*)**

Tim teknis ini berperan sebagai arsitek dan pelaksana pembangunan *pipeline* data, model analitik, dan infrastruktur komputasi. Mereka bertanggung jawab atas perancangan skema *Extract-Transform-Load* (ETL), pemilihan algoritma pemodelan prediktif, serta pemeliharaan dan optimasi klaster pemrosesan. Dalam konteks dataset ini, tim data engineering perlu memastikan bahwa *pipeline* ingesti mampu menangani format CSV dengan sembilan kolom atribut secara konsisten dan melakukan validasi kualitas data pada setiap siklus pemrosesan.

**4. Manajemen Eksekutif (*C-Level / Board of Directors*)**

Pimpinan tertinggi memerlukan *dashboard* ringkasan eksekutif yang menyajikan metrik kinerja utama (*Key Performance Indicators* / KPI) seperti total pendapatan, pertumbuhan penjualan per kategori, dan tingkat retensi pelanggan. Visualisasi data yang intuitif dan pembaruan yang tepat waktu menjadi persyaratan utama bagi pemangku kepentingan pada tingkatan ini.

Pemetaan kebutuhan seluruh pemangku kepentingan di awal tahap perancangan ini bertujuan memastikan bahwa arsitektur solusi Big Data yang dibangun tidak sekadar memenuhi persyaratan teknis, melainkan secara langsung berkontribusi pada pencapaian matriks kinerja strategis organisasi.

---

## Bab 2: Rancangan Solusi Big Data

### 2.1 Arsitektur Solusi Big Data Secara Umum

Untuk menjawab kebutuhan analisis perilaku belanja pelanggan ritel, dirancang arsitektur solusi Big Data yang bersifat praktis dan dapat diimplementasikan secara langsung. Arsitektur ini berpusat pada **Apache Spark (PySpark)** sebagai kerangka kerja utama yang menangani seluruh siklus hidup data — mulai dari penyerapan (*ingestion*), penyimpanan terstruktur (*storage*), hingga pemrosesan analitik dan pemodelan prediktif (*processing*).

Pemilihan PySpark sebagai inti arsitektur didasarkan pada pertimbangan berikut. Pertama, PySpark menyediakan ekosistem terpadu (*unified engine*) yang mampu menangani seluruh tahapan *pipeline* data dalam satu platform, sehingga mengeliminasi kompleksitas integrasi antar-komponen yang terpisah. Kedua, PySpark dapat dijalankan dalam moda lokal (*local mode*) pada satu mesin untuk keperluan pengembangan dan demonstrasi, sekaligus dapat diskalakan ke klaster terdistribusi (*cluster mode*) ketika volume data meningkat dalam skenario produksi. Ketiga, PySpark menggunakan antarmuka pemrograman berbasis Python — bahasa yang paling lazim digunakan dalam ekosistem ilmu data — sehingga mempersingkat kurva pembelajaran dan mempercepat siklus pengembangan.

Alur arsitektur solusi secara keseluruhan dapat dirangkum sebagai berikut:

```
CSV (Sumber Data) → PySpark (Load & Validasi) → Spark DataFrame / Parquet (Penyimpanan)
    → Spark SQL (Analisis Eksploratif) → Spark MLlib (Segmentasi & Prediksi)
    → Export CSV / Pandas (Visualisasi & Pelaporan)
```

Arsitektur ini bersifat modular dan memungkinkan perluasan di masa depan. Apabila skala data bertumbuh secara signifikan, komponen-komponen tambahan seperti Apache Kafka (untuk *streaming ingestion*), Data Lake berbasis HDFS (untuk penyimpanan data mentah berskala besar), atau Apache Flink (untuk pemrosesan waktu-nyata) dapat diintegrasikan ke dalam arsitektur tanpa perombakan fundamental.

### 2.2 Metode Pengumpulan Data (*Data Ingestion*)

Proses penyerapan data merupakan tahap pertama dalam *pipeline* analitik, di mana data mentah dari sumber eksternal dimuat ke dalam lingkungan pemrosesan. Strategi penyerapan yang diterapkan adalah **pemrosesan terkumpul (*batch ingestion*)** menggunakan fungsi baca bawaan PySpark.

Dataset `retail_sales_dataset.csv` merupakan berkas statis (*flat file*) yang memuat 1.000 rekaman transaksi historis. Karakteristik data yang bersifat statis dan tidak berubah secara real-time menjadikan pendekatan *batch* sebagai pilihan yang paling efisien dan realistis. PySpark menyediakan fungsi `spark.read.csv()` yang secara native mampu membaca berkas CSV dengan inferensi skema otomatis (*inferSchema*), penanganan baris kepala (*header*), serta validasi tipe data pada setiap kolom.

Proses *ingestion* dengan PySpark mencakup langkah-langkah berikut:

1. **Pembacaan data**: Berkas CSV dimuat ke dalam Spark DataFrame dengan spesifikasi skema yang mencakup sembilan kolom atribut — *Transaction ID* (integer), *Date* (date), *Customer ID* (string), *Gender* (string), *Age* (integer), *Product Category* (string), *Quantity* (integer), *Price per Unit* (integer), dan *Total Amount* (integer).

2. **Validasi awal**: Setelah pemuatan, dilakukan pemeriksaan kelengkapan data (*null check*), verifikasi jumlah baris (harus sesuai dengan ekspektasi 1.000 rekaman), serta validasi rentang nilai pada kolom numerik (misalnya, usia antara 18–64, kuantitas antara 1–4).

3. **Transformasi tipe data**: Kolom tanggal yang awalnya bertipe *string* dikonversi ke tipe *DateType* agar memungkinkan operasi temporal seperti pengelompokan berdasarkan bulan, kuartal, atau hari dalam seminggu.

Keunggulan pendekatan ini terletak pada kesederhanaannya yang tidak mengorbankan skalabilitas. Skrip PySpark yang sama yang memproses 1.000 baris data pada moda lokal dapat dijalankan tanpa modifikasi substansial pada klaster terdistribusi yang memproses jutaan baris, karena Spark secara otomatis mendistribusikan beban komputasi ke seluruh simpul (*node*) yang tersedia.

Sebagai catatan untuk skenario pengembangan di masa depan, apabila peritel membutuhkan penyerapan data secara *real-time* (misalnya, dari sistem *Point-of-Sale* atau platform *e-commerce*), arsitektur ini dapat diperluas dengan menambahkan **Apache Kafka** sebagai *message broker* yang mengalirkan data transaksi ke Spark Structured Streaming.

### 2.3 Teknologi Penyimpanan Data (*Data Storage*)

Strategi penyimpanan data dalam arsitektur ini menggunakan **Spark DataFrame** sebagai representasi data utama selama pemrosesan, dengan opsi persistensi ke format **Apache Parquet** untuk penyimpanan jangka panjang yang efisien.

**a. Spark DataFrame (Penyimpanan Selama Pemrosesan)**

Setelah berkas CSV dimuat melalui proses *ingestion*, data direpresentasikan sebagai Spark DataFrame — struktur data tabular terdistribusi yang tersimpan dalam memori (*in-memory*) klaster Spark. DataFrame menyediakan antarmuka yang familiar bagi pengguna Python (serupa dengan Pandas DataFrame) sekaligus memanfaatkan mesin eksekusi terdistribusi Spark untuk performa optimal.

Spark DataFrame dipilih sebagai wadah pemrosesan utama karena beberapa alasan. Pertama, operasi *lazy evaluation* yang diterapkan Spark memungkinkan optimasi otomatis terhadap rencana eksekusi (*query plan*) sebelum komputasi benar-benar dijalankan, sehingga operasi yang tidak efisien dapat dieliminasi secara otomatis oleh *Catalyst Optimizer*. Kedua, DataFrame mendukung operasi SQL standar melalui Spark SQL, sehingga analis yang terbiasa dengan *query* relasional dapat langsung bekerja tanpa mempelajari API baru. Ketiga, data dalam DataFrame dapat di-*cache* ke memori untuk mempercepat akses berulang pada operasi analitik iteratif seperti pelatihan model *machine learning*.

**b. Format Apache Parquet (Penyimpanan Persisten)**

Untuk keperluan penyimpanan jangka panjang, data yang telah dibersihkan dan ditransformasi disimpan dalam format **Apache Parquet** — format berkas kolumnar (*columnar storage format*) yang dioptimasi untuk beban kerja analitik. Dibandingkan format CSV yang digunakan pada dataset sumber, Parquet menawarkan tiga keunggulan signifikan: kompresi data yang jauh lebih efisien (hingga 75% lebih kecil), performa pembacaan yang lebih cepat karena hanya kolom yang relevan yang perlu dibaca (*column pruning*), serta preservasi informasi tipe data sehingga tidak diperlukan inferensi skema ulang pada setiap pembacaan.

Dalam praktiknya, data disimpan dalam struktur berpartisi (*partitioned storage*) berdasarkan kolom yang sering digunakan sebagai filter — misalnya, partisi berdasarkan *Product Category* atau periode waktu (bulan/kuartal). Skema partisi ini mempercepat *query* analitik secara drastis karena Spark hanya perlu membaca partisi yang relevan (*partition pruning*), bukan memindai seluruh dataset.

Pada skenario di mana skala data bertumbuh signifikan, arsitektur penyimpanan dapat diperluas dengan memisahkan data mentah ke dalam *Data Lake* berbasis HDFS dan data olahan ke dalam *Data Warehouse* relasional. Namun, untuk skala dataset saat ini (1.000 rekaman, 51 KB), pendekatan Spark DataFrame + Parquet sudah sangat memadai dan efisien.

### 2.4 Kerangka Pemrosesan Data (*Processing Framework*)

**Apache Spark (PySpark)** berfungsi sebagai kerangka kerja pemrosesan tunggal yang menangani seluruh operasi analitik — dari eksplorasi data hingga pemodelan prediktif. Spark beroperasi dengan paradigma komputasi berbasis memori (*in-memory processing*) yang mampu mengeksekusi tugas analitik hingga 100 kali lebih cepat dibandingkan pendekatan *MapReduce* konvensional yang bergantung pada operasi baca-tulis cakram (*disk I/O*).

Kapabilitas pemrosesan Spark yang dimanfaatkan dalam solusi ini mencakup tiga komponen utama:

**a. Spark SQL (Analisis Eksploratif dan Pelaporan)**

Spark SQL menyediakan antarmuka *query* relasional untuk analisis eksploratif terhadap dataset transaksi ritel. Melalui Spark SQL, operasi analitik dapat diekspresikan dalam sintaks SQL standar yang familiar, sekaligus dieksekusi secara terdistribusi oleh mesin Spark.

Contoh analisis yang dapat dijalankan langsung menggunakan Spark SQL pada dataset ini meliputi: perhitungan total pendapatan per kategori produk (Electronics: 156.905, Clothing: 155.580, Beauty: 143.515), identifikasi rata-rata nilai transaksi per kategori (Beauty: 467,5; Electronics: 458,8; Clothing: 443,2), analisis distribusi pembelian berdasarkan demografi (gender dan kelompok usia), serta deteksi tren penjualan temporal berdasarkan bulan atau kuartal sepanjang periode Januari 2023 hingga Januari 2024.

**b. Spark MLlib (Segmentasi Pelanggan dan Pemodelan Prediktif)**

Spark MLlib merupakan pustaka *machine learning* terintegrasi yang memungkinkan pembangunan model analitik langsung di atas Spark DataFrame tanpa memerlukan pemindahan data ke *framework* eksternal. Dalam konteks analisis perilaku belanja pelanggan, dua teknik utama yang diterapkan adalah:

1. **Segmentasi Pelanggan dengan K-Means Clustering**: Algoritma K-Means diterapkan untuk mengelompokkan 1.000 pelanggan ke dalam segmen-segmen berbeda berdasarkan fitur perilaku belanja — seperti total nilai pembelian, rata-rata kuantitas per transaksi, dan preferensi kategori produk. Hasil segmentasi ini memungkinkan tim pemasaran merancang strategi yang terpersonalisasi untuk setiap segmen (misalnya, segmen *High Value*, *Medium Value*, dan *Low Value*).

2. **Analisis Asosiasi dengan FP-Growth**: Algoritma *Frequent Pattern Growth* digunakan untuk mengidentifikasi pola asosiasi antar-kategori produk — misalnya, apakah pelanggan yang membeli produk Beauty cenderung juga membeli produk Clothing dalam periode waktu yang berdekatan. Informasi ini bernilai tinggi untuk strategi *cross-selling* dan *bundling* produk.

**c. Integrasi dengan Pandas dan Matplotlib (Visualisasi Hasil)**

Setelah proses analitik di Spark selesai, hasil agregasi dan prediksi dikonversi dari Spark DataFrame ke Pandas DataFrame menggunakan fungsi `.toPandas()` untuk keperluan visualisasi. Pustaka **Matplotlib** dan **Seaborn** digunakan untuk menghasilkan grafik dan *chart* yang intuitif — seperti diagram batang distribusi penjualan per kategori, *scatter plot* segmentasi pelanggan hasil K-Means, serta *heatmap* korelasi antar-atribut demografis dan perilaku belanja.

Alur pemrosesan lengkap dari ingesti hingga visualisasi dapat dirangkum dalam satu *pipeline* PySpark yang kohesif: memuat CSV → membersihkan dan memvalidasi data → mengeksekusi *query* analitik dengan Spark SQL → melatih model segmentasi dengan MLlib → mengekspor hasil ke Pandas → memvisualisasikan wawasan dengan Matplotlib. Seluruh *pipeline* ini dapat dijalankan dalam satu sesi Jupyter Notebook yang terintegrasi dengan PySpark, menjadikannya mudah untuk direproduksi, didokumentasikan, dan dipresentasikan.

Apabila di masa depan kebutuhan analitik berkembang ke arah pemrosesan waktu-nyata (*real-time*) — misalnya untuk deteksi anomali transaksi secara instan atau personalisasi rekomendasi produk secara dinamis — arsitektur ini dapat diperluas dengan menambahkan **Apache Flink** sebagai mesin pemrosesan *stream* pelengkap tanpa mengganggu *pipeline batch* yang sudah berjalan.
