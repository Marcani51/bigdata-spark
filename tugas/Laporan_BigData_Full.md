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

---

## Bab 3: Tata Kelola IT (*IT Governance*)

### 3.1 Keamanan Data (*Data Security*)

Keamanan data merupakan pilar fundamental dalam tata kelola sistem Big Data yang menangani informasi transaksi pelanggan ritel. Dataset `retail_sales_dataset.csv` memuat atribut-atribut yang tergolong sensitif secara bisnis — meliputi *Customer ID* (1.000 identitas pelanggan unik), riwayat pembelian individu, preferensi kategori produk, serta profil demografis berupa usia dan jenis kelamin. Kebocoran atau penyalahgunaan data semacam ini tidak hanya berpotensi merugikan pelanggan secara personal, tetapi juga dapat menghancurkan reputasi perusahaan dan menimbulkan kerugian finansial yang substansial.

Strategi keamanan data yang diterapkan dalam arsitektur solusi ini mencakup tiga lapisan perlindungan yang saling melengkapi:

**a. Enkripsi Data (*Data Encryption*)**

Seluruh data yang tersimpan dalam ekosistem Big Data dilindungi menggunakan enkripsi simetris AES-256 (*Advanced Encryption Standard* dengan panjang kunci 256-bit) untuk data diam (*data at rest*). Sementara itu, data yang ditransmisikan antar-komponen sistem (misalnya, dari klaster Apache Spark ke penyimpanan Parquet) diamankan menggunakan protokol TLS 1.3 (*Transport Layer Security*) untuk data bergerak (*data in transit*). Dengan mekanisme ini, bahkan jika pihak yang tidak berwenang berhasil mengakses media penyimpanan fisik atau menyadap lalu lintas jaringan, data yang diperoleh tidak dapat dibaca tanpa kunci dekripsi yang sah.

Dalam konteks dataset ritel ini, enkripsi memastikan bahwa informasi seperti pola pembelian pelanggan tertentu (misalnya, CUST001 yang membeli produk Beauty seharga 150) tidak dapat dieksploitasi oleh pihak ketiga untuk keperluan yang tidak sah, seperti *profiling* ilegal atau penargetan komersial tanpa persetujuan.

**b. Pengendalian Akses (*Access Control*)**

Sistem pengendalian akses berbasis peran (*Role-Based Access Control* / RBAC) diterapkan untuk memastikan bahwa setiap pengguna hanya dapat mengakses data sesuai dengan wewenang dan tanggung jawab fungsionalnya. Dalam konteks organisasi ritel, matriks hak akses dirancang sebagai berikut:

| Peran (*Role*)            | Hak Akses                                                                 |
|---------------------------|---------------------------------------------------------------------------|
| Data Engineer             | Baca-tulis penuh pada penyimpanan data dan *pipeline* ETL                 |
| Data Scientist            | Baca pada data mentah dan olahan; eksekusi model analitik                 |
| Manajer Pemasaran (CMO)   | Baca pada *dashboard* agregat; tidak dapat mengakses data individu mentah |
| Manajer Operasional (COO) | Baca pada laporan operasional dan tren penjualan                          |
| Eksekutif (C-Level)       | Baca pada *dashboard* ringkasan KPI                                       |

Dengan pemisahan hak akses ini, seorang CMO yang hanya membutuhkan informasi agregat (misalnya, "total penjualan kategori Clothing sebesar 155.580") tidak akan memiliki akses ke rekaman transaksi individu pelanggan, sehingga risiko penyalahgunaan data diminimalkan.

**c. Audit dan Pemantauan (*Audit Logging & Monitoring*)**

Seluruh aktivitas akses dan modifikasi data dicatat dalam *audit log* yang bersifat *immutable* (tidak dapat diubah). Log ini mencakup informasi mengenai siapa yang mengakses data, kapan akses dilakukan, data apa yang diakses, dan operasi apa yang dijalankan (baca, tulis, hapus). Sistem pemantauan berbasis *Security Information and Event Management* (SIEM) beroperasi secara waktu-nyata untuk mendeteksi pola akses yang anomali — misalnya, percobaan pengunduhan massal data pelanggan yang tidak lazim pada jam-jam di luar operasional normal.

### 3.2 Kepatuhan Regulasi (*Regulatory Compliance*)

Pengelolaan data pelanggan dalam skala Big Data tunduk pada kerangka regulasi yang ketat, baik di tingkat nasional maupun internasional. Kepatuhan terhadap regulasi bukan sekadar kewajiban hukum, melainkan juga menjadi prasyarat untuk membangun dan mempertahankan kepercayaan pelanggan.

**a. Undang-Undang Pelindungan Data Pribadi (UU PDP) — Indonesia**

Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP) merupakan landasan hukum utama yang mengatur pengumpulan, pemrosesan, dan penyimpanan data pribadi di Indonesia. Dalam konteks dataset ritel yang digunakan, beberapa atribut data terklasifikasi sebagai data pribadi menurut UU PDP, yaitu *Customer ID* (sebagai pengidentifikasi unik individu), usia, dan jenis kelamin.

Implikasi kepatuhan UU PDP terhadap perancangan arsitektur solusi meliputi: (1) kewajiban memperoleh persetujuan eksplisit (*informed consent*) dari pelanggan sebelum data mereka diproses untuk keperluan analitik; (2) kewajiban menyediakan mekanisme bagi pelanggan untuk mengakses, memperbaiki, atau meminta penghapusan data pribadinya (*right to erasure*); dan (3) kewajiban melaporkan insiden kebocoran data kepada otoritas terkait dalam jangka waktu yang ditentukan.

**b. *General Data Protection Regulation* (GDPR) — Uni Eropa**

Meskipun dataset ini beroperasi dalam konteks domestik, penerapan prinsip-prinsip GDPR tetap relevan sebagai acuan praktik terbaik (*best practice*) dalam pelindungan data berskala internasional. Prinsip utama GDPR yang diadopsi mencakup *data minimization* (hanya mengumpulkan data yang benar-benar diperlukan), *purpose limitation* (data hanya digunakan untuk tujuan yang telah dinyatakan), dan *storage limitation* (data tidak disimpan lebih lama dari yang diperlukan).

Dalam praktiknya, kepatuhan terhadap prinsip-prinsip ini berarti bahwa dataset ritel hanya boleh digunakan untuk analisis perilaku belanja dan optimalisasi layanan sebagaimana dinyatakan dalam kebijakan privasi perusahaan — bukan untuk tujuan lain seperti penjualan data ke pihak ketiga tanpa persetujuan pelanggan.

**c. Mekanisme Implementasi Kepatuhan**

Untuk memastikan kepatuhan yang konsisten, organisasi menerapkan beberapa mekanisme operasional: (1) penunjukan *Data Protection Officer* (DPO) yang bertanggung jawab mengawasi kepatuhan regulasi; (2) pelaksanaan *Data Protection Impact Assessment* (DPIA) sebelum memulai proyek analitik baru; dan (3) penyusunan *data processing agreement* dengan seluruh pihak ketiga yang terlibat dalam pemrosesan data, termasuk penyedia layanan *cloud* dan infrastruktur Big Data.

### 3.3 Privasi Data (*Data Privacy*)

Privasi data berkaitan erat dengan keamanan dan kepatuhan, namun memiliki fokus spesifik pada perlindungan identitas serta hak informasional individu pelanggan. Dalam ekosistem Big Data yang memproses ribuan hingga jutaan rekaman transaksi, risiko terungkapnya identitas pelanggan melalui kombinasi atribut data (*re-identification attack*) menjadi perhatian utama.

**a. Anonimisasi Data (*Data Anonymization*)**

Teknik anonimisasi diterapkan untuk menghilangkan atau mengaburkan atribut yang secara langsung dapat mengidentifikasi individu. Pada dataset `retail_sales_dataset.csv`, kolom *Customer ID* (CUST001 hingga CUST1000) merupakan *pseudo-identifier* yang, jika dikombinasikan dengan atribut usia dan jenis kelamin, berpotensi memungkinkan identifikasi ulang pelanggan tertentu.

Strategi anonimisasi yang diterapkan mencakup:

- **Pseudonimisasi (*Pseudonymization*)**: Mengganti *Customer ID* asli dengan kode acak (*token*) menggunakan fungsi *hash* kriptografis satu arah. Pemetaan antara ID asli dan *token* disimpan secara terpisah dengan enkripsi berlapis dan hanya dapat diakses oleh personel yang berwenang.
- **Generalisasi (*Generalization*)**: Mengubah atribut usia dari nilai spesifik (misalnya, 34 tahun) menjadi rentang kelompok usia (misalnya, 30–39 tahun) untuk keperluan analitik agregat. Teknik ini mengurangi risiko identifikasi tanpa mengorbankan validitas analisis segmentasi demografis.
- **Supresi (*Suppression*)**: Menghapus atribut-atribut yang tidak relevan untuk tujuan analitik dari salinan data yang digunakan dalam lingkungan pengembangan atau pengujian.

**b. *Privacy by Design***

Prinsip *Privacy by Design* mengintegrasikan pertimbangan privasi ke dalam setiap tahap perancangan arsitektur solusi, bukan sebagai fitur tambahan yang ditempelkan kemudian. Dalam implementasinya, setiap komponen *pipeline* data — dari lapisan *ingestion* hingga *processing* — dirancang dengan mekanisme proteksi privasi bawaan. Misalnya, proses agregasi data di Apache Spark secara otomatis menerapkan *k-anonymity* (setiap rekaman dalam hasil *query* harus dimiliki oleh minimal *k* individu) untuk mencegah identifikasi individu melalui *query* analitik.

**c. Pengelolaan Persetujuan (*Consent Management*)**

Sistem pengelolaan persetujuan pelanggan (*consent management platform*) diintegrasikan ke dalam arsitektur untuk merekam dan mengelola preferensi privasi setiap pelanggan secara granular. Pelanggan dapat menentukan jenis data apa yang boleh dikumpulkan, untuk tujuan apa data tersebut digunakan, dan kapan mereka ingin mencabut persetujuannya. Setiap perubahan preferensi privasi secara otomatis terpropagasi ke seluruh komponen *pipeline* data, sehingga pemrosesan data selalu selaras dengan kehendak pelanggan.

### 3.4 Kualitas Data (*Data Quality*)

Kualitas data merupakan prasyarat fundamental yang menentukan validitas dan keandalan seluruh luaran analitik. Prinsip *"garbage in, garbage out"* berlaku secara absolut dalam konteks Big Data — model prediktif atau segmentasi pelanggan yang dihasilkan dari data berkualitas rendah akan menghasilkan wawasan yang menyesatkan dan keputusan bisnis yang merugikan.

**a. Dimensi Kualitas Data**

Kualitas data dalam arsitektur solusi ini diukur berdasarkan enam dimensi standar:

| Dimensi            | Definisi                                                | Contoh pada Dataset                                                         |
|---------------------|---------------------------------------------------------|-----------------------------------------------------------------------------|
| Kelengkapan         | Tidak ada nilai yang hilang (*missing values*)          | Seluruh 1.000 rekaman memiliki nilai lengkap pada 9 kolom                   |
| Konsistensi         | Format data seragam di seluruh rekaman                  | Format tanggal konsisten (YYYY-MM-DD); Gender hanya "Male"/"Female"         |
| Akurasi             | Nilai data merepresentasikan fakta sebenarnya           | Total Amount = Quantity × Price per Unit (validasi kalkulasi)                |
| Ketepatan Waktu     | Data tersedia pada saat dibutuhkan                      | Data transaksi dimuat maksimal H+1 setelah transaksi terjadi                |
| Validitas           | Data sesuai dengan aturan domain yang berlaku           | Usia dalam rentang wajar (18–64); Quantity positif (1–4)                    |
| Keunikan            | Tidak ada duplikasi rekaman                             | Setiap *Transaction ID* (1–1000) bersifat unik                             |

**b. Proses Pembersihan Data (*Data Cleaning*)**

Tahap pembersihan data dieksekusi secara otomatis dalam *pipeline* ETL sebelum data dimuat ke penyimpanan analitik. Proses ini mencakup beberapa langkah terstruktur:

Pertama, **deteksi dan penanganan nilai hilang (*missing values*)**: Setiap kolom diperiksa untuk memastikan kelengkapan data. Rekaman dengan nilai hilang pada atribut kritis (seperti *Transaction ID*, *Customer ID*, atau *Total Amount*) ditandai untuk investigasi manual, sementara nilai hilang pada atribut non-kritis dapat diisi menggunakan teknik imputasi statistik (misalnya, median atau modus).

Kedua, **validasi format dan tipe data**: Format tanggal divalidasi terhadap pola YYYY-MM-DD, nilai numerik (*Age, Quantity, Price per Unit, Total Amount*) dipastikan bertipe integer positif, dan nilai kategorikal (*Gender, Product Category*) diverifikasi terhadap daftar nilai yang diizinkan (*whitelist*) — yaitu Male/Female untuk Gender, serta Beauty/Clothing/Electronics untuk Product Category.

Ketiga, **validasi logika bisnis (*business rule validation*)**: Aturan derivasi diperiksa untuk memastikan konsistensi antar-kolom. Secara spesifik, nilai *Total Amount* harus sama dengan hasil perkalian *Quantity* dan *Price per Unit*. Rekaman yang melanggar aturan ini ditandai sebagai anomali dan diarahkan ke antrean investigasi.

Keempat, **deteksi dan penghapusan duplikasi**: Rekaman duplikat diidentifikasi berdasarkan kombinasi *Transaction ID* atau kombinasi *Customer ID + Date + Product Category + Quantity*. Data duplikat dihapus dengan mempertahankan rekaman yang paling lengkap dan terbaru.

**c. Pemantauan Kualitas Data Berkelanjutan (*Continuous Data Quality Monitoring*)**

Kualitas data bukan merupakan aktivitas satu kali, melainkan proses berkelanjutan yang memerlukan pemantauan sistematis. Sistem pemantauan kualitas data otomatis (*data quality monitoring*) diimplementasikan untuk mengevaluasi metrik kualitas pada setiap siklus pemrosesan *batch*. Metrik-metrik tersebut divisualisasikan dalam *dashboard* khusus yang dapat diakses oleh tim *Data Engineering*, sehingga degradasi kualitas data dapat terdeteksi dan ditindaklanjuti secara proaktif sebelum berdampak pada luaran analitik.

Ambang batas (*threshold*) kualitas data ditetapkan secara eksplisit — misalnya, tingkat kelengkapan data minimum 99,5%, tingkat konsistensi format minimum 100%, dan tingkat keberhasilan validasi logika bisnis minimum 99,9%. Jika metrik kualitas pada suatu siklus pemrosesan jatuh di bawah ambang batas yang ditetapkan, sistem secara otomatis mengirimkan peringatan kepada tim terkait dan menahan pemuatan data ke penyimpanan analitik hingga isu kualitas terselesaikan.

---

## Bab 4: Data

### 4.1 Deskripsi Data

Dataset yang digunakan dalam studi ini bersumber dari platform Kaggle dengan nama berkas `retail_sales_dataset.csv`. Dataset ini merupakan data terstruktur (*structured data*) dalam format *Comma-Separated Values* (CSV) yang merekam transaksi penjualan ritel selama periode satu tahun. Berikut adalah ringkasan karakteristik umum dataset:

| Karakteristik           | Nilai                                      |
|-------------------------|---------------------------------------------|
| Nama Berkas             | `retail_sales_dataset.csv`                  |
| Format Data             | CSV (*Comma-Separated Values*)              |
| Jumlah Rekaman          | 1.000 transaksi                             |
| Jumlah Atribut (Kolom)  | 9 kolom                                     |
| Ukuran Berkas           | ~51 KB                                      |
| Periode Data            | 1 Januari 2023 – 1 Januari 2024            |
| Jumlah Pelanggan Unik   | 1.000 pelanggan                             |
| Jenis Data              | Terstruktur (*Structured Data*)             |

Dataset ini termasuk dalam klasifikasi **data terstruktur** karena seluruh rekaman tersusun dalam format tabular dengan skema kolom yang konsisten dan tipe data yang terdefinisi. Tidak terdapat data semi-terstruktur (seperti JSON atau XML) maupun data tidak terstruktur (seperti teks bebas, gambar, atau video) dalam dataset ini. Namun, dalam skenario produksi nyata, data ritel biasanya dilengkapi oleh sumber data semi-terstruktur (log aktivitas web dalam format JSON) dan tidak terstruktur (ulasan produk dalam format teks bebas, foto produk) yang dapat diintegrasikan ke dalam arsitektur Big Data yang telah dirancang pada Bab 2.

Berikut adalah deskripsi terperinci untuk setiap atribut (kolom) dalam dataset:

| No | Nama Kolom        | Tipe Data | Deskripsi                                                                                                  | Contoh Nilai        |
|----|-------------------|-----------|------------------------------------------------------------------------------------------------------------|---------------------|
| 1  | Transaction ID    | Integer   | Pengidentifikasi unik untuk setiap transaksi. Bernilai sekuensial dari 1 hingga 1.000.                    | 1, 500, 1000        |
| 2  | Date              | Date      | Tanggal terjadinya transaksi dalam format YYYY-MM-DD.                                                      | 2023-11-24          |
| 3  | Customer ID       | String    | Pengidentifikasi unik pelanggan dengan format "CUST" diikuti nomor urut tiga digit.                        | CUST001, CUST500    |
| 4  | Gender            | String    | Jenis kelamin pelanggan. Terdiri dari dua nilai kategorikal: "Male" dan "Female".                           | Male, Female        |
| 5  | Age               | Integer   | Usia pelanggan dalam satuan tahun. Rentang nilai: 18 hingga 64 tahun (rata-rata: 41,4 tahun).              | 34, 26, 50          |
| 6  | Product Category  | String    | Kategori produk yang dibeli. Terdiri dari tiga nilai: "Beauty", "Clothing", dan "Electronics".              | Beauty, Clothing    |
| 7  | Quantity          | Integer   | Jumlah unit produk yang dibeli dalam satu transaksi. Rentang nilai: 1 hingga 4 (rata-rata: 2,5).           | 1, 2, 3, 4          |
| 8  | Price per Unit    | Integer   | Harga satuan produk. Terdapat lima tingkatan harga diskrit: 25, 30, 50, 300, dan 500.                      | 25, 50, 500         |
| 9  | Total Amount      | Integer   | Nilai total transaksi, merupakan hasil perkalian Quantity × Price per Unit. Rentang: 25 hingga 2.000.       | 150, 1000, 2000     |

**Distribusi Data Berdasarkan Kategori Produk**

Distribusi transaksi di antara tiga kategori produk menunjukkan komposisi yang relatif seimbang, mengindikasikan bahwa dataset ini cukup representatif untuk analisis lintas-kategori:

| Kategori Produk | Jumlah Transaksi | Persentase | Total Pendapatan | Rata-rata per Transaksi |
|-----------------|------------------|------------|------------------|-------------------------|
| Clothing        | 351              | 35,1%      | 155.580          | 443,2                   |
| Electronics     | 342              | 34,2%      | 156.905          | 458,8                   |
| Beauty          | 307              | 30,7%      | 143.515          | 467,5                   |
| **Total**       | **1.000**        | **100%**   | **456.000**      | **456,0**               |

**Distribusi Data Berdasarkan Demografi Pelanggan**

Komposisi pelanggan berdasarkan jenis kelamin menunjukkan distribusi yang hampir seimbang — 510 pelanggan perempuan (51%) dan 490 pelanggan laki-laki (49%). Distribusi usia membentang dari 18 hingga 64 tahun dengan rata-rata 41,4 tahun, mencerminkan basis pelanggan yang mencakup segmen usia muda (*young adult*), dewasa (*adult*), dan pra-lansia (*pre-senior*).

**Karakteristik Volume dan Varietas Data**

Dari perspektif Big Data, dataset ini dapat dianalisis melalui kerangka 3V (*Three V's of Big Data*):

1. **Volume**: Dataset saat ini berukuran ~51 KB dengan 1.000 rekaman. Meskipun volume ini tergolong kecil untuk demonstrasi, arsitektur PySpark yang dirancang mampu menangani dataset berskala terabyte tanpa modifikasi fundamental pada kode pemrosesan.

2. **Velocity**: Data pada dataset ini bersifat statis (*batch*) dengan pembaruan berkala. Dalam skenario produksi, kecepatan arus data dapat meningkat hingga ribuan transaksi per detik dari berbagai kanal penjualan.

3. **Variety**: Dataset ini hanya memuat satu jenis data terstruktur (CSV). Dalam ekosistem ritel nyata, variasi data mencakup data terstruktur (transaksi), semi-terstruktur (log web dalam JSON), dan tidak terstruktur (ulasan pelanggan, foto produk).

### 4.2 Model Data

Model data yang dirancang untuk mendukung analisis perilaku belanja pelanggan mengadopsi pendekatan **Spark DataFrame Schema** yang memetakan setiap atribut dataset ke tipe data yang sesuai untuk pemrosesan optimal di lingkungan PySpark.

**a. Skema Data (*Data Schema*)**

Skema data mendefinisikan struktur formal dari dataset yang akan diproses oleh PySpark. Berikut adalah pemetaan skema yang dirancang:

```
StructType([
    StructField("Transaction_ID", IntegerType(), nullable=False),
    StructField("Date", DateType(), nullable=False),
    StructField("Customer_ID", StringType(), nullable=False),
    StructField("Gender", StringType(), nullable=False),
    StructField("Age", IntegerType(), nullable=False),
    StructField("Product_Category", StringType(), nullable=False),
    StructField("Quantity", IntegerType(), nullable=False),
    StructField("Price_per_Unit", IntegerType(), nullable=False),
    StructField("Total_Amount", IntegerType(), nullable=False)
])
```

Pendefinisian skema secara eksplisit (*explicit schema definition*) dipilih ketimbang inferensi otomatis (*inferSchema*) karena dua alasan. Pertama, pendefinisian eksplisit mengeliminasi ambiguitas tipe data yang dapat terjadi pada inferensi otomatis — misalnya, kolom *Transaction ID* yang mungkin terdeteksi sebagai *string* ketimbang *integer* jika ada inkonsistensi format. Kedua, pendefinisian eksplisit meningkatkan performa pemuatan data karena Spark tidak perlu melakukan pemindaian awal (*pre-scan*) terhadap seluruh dataset untuk menentukan tipe data setiap kolom.

**b. Model Relasional untuk Analitik**

Meskipun dataset asli tersimpan dalam satu tabel tunggal (*flat table*), untuk keperluan analitik yang lebih kompleks, data dimodelkan ke dalam struktur dimensional menggunakan transformasi PySpark. Model ini terdiri dari:

**Tabel Fakta — Transaksi (*fact_transactions*)**

Tabel fakta menyimpan setiap rekaman transaksi dengan referensi ke dimensi-dimensi terkait:

| Kolom             | Tipe    | Keterangan                          |
|--------------------|---------|-------------------------------------|
| transaction_id     | Integer | *Primary Key*                       |
| date               | Date    | Tanggal transaksi                   |
| customer_id        | String  | *Foreign Key* ke dimensi pelanggan  |
| product_category   | String  | *Foreign Key* ke dimensi produk     |
| quantity           | Integer | Jumlah unit yang dibeli             |
| price_per_unit     | Integer | Harga satuan                        |
| total_amount       | Integer | Nilai total transaksi               |

**Tabel Dimensi — Pelanggan (*dim_customers*)**

Tabel dimensi pelanggan diderivasi dari tabel fakta menggunakan operasi `select` dan `distinct` pada PySpark:

| Kolom         | Tipe    | Keterangan                            |
|---------------|---------|---------------------------------------|
| customer_id   | String  | *Primary Key* (CUST001 – CUST1000)    |
| gender        | String  | Jenis kelamin (Male / Female)         |
| age           | Integer | Usia pelanggan (18 – 64)              |
| age_group     | String  | Kelompok usia (kolom turunan)         |

Kolom *age_group* merupakan atribut turunan (*derived attribute*) yang mengklasifikasikan usia ke dalam segmen: "18-25" (Muda), "26-35" (Dewasa Muda), "36-45" (Dewasa), "46-55" (Dewasa Atas), dan "56-64" (Pra-Lansia). Segmentasi ini mempermudah analisis pola belanja berdasarkan kelompok usia.

**Tabel Dimensi — Produk (*dim_products*)**

| Kolom             | Tipe    | Keterangan                              |
|--------------------|---------|----------------------------------------|
| product_category   | String  | *Primary Key* (Beauty / Clothing / Electronics) |
| price_tier         | String  | Tier harga (kolom turunan)              |

Kolom *price_tier* mengklasifikasikan harga per unit ke dalam tiga segmen: "Budget" (25–30), "Mid-Range" (50), dan "Premium" (300–500). Klasifikasi ini memungkinkan analisis preferensi pelanggan berdasarkan daya beli.

**Tabel Dimensi — Waktu (*dim_time*)**

| Kolom         | Tipe    | Keterangan                          |
|---------------|---------|-------------------------------------|
| date          | Date    | *Primary Key*                       |
| year          | Integer | Tahun (2023 / 2024)                 |
| month         | Integer | Bulan (1 – 12)                      |
| quarter       | Integer | Kuartal (Q1 – Q4)                   |
| day_of_week   | String  | Hari dalam minggu                   |

Dimensi waktu diderivasi dari kolom *Date* menggunakan fungsi temporal bawaan PySpark (`year()`, `month()`, `quarter()`, `dayofweek()`). Model dimensional ini memungkinkan analisis tren penjualan pada berbagai granularitas temporal — dari harian hingga kuartalan.

**c. Hubungan Antar-Entitas**

Hubungan antar-tabel dalam model dimensional ini mengikuti pola *star schema* di mana tabel fakta (*fact_transactions*) berada di pusat dan terhubung ke tiga tabel dimensi melalui kunci asing (*foreign key*):

```
                    dim_customers
                         |
                    customer_id
                         |
dim_time ---date--- fact_transactions ---product_category--- dim_products
```

Model *star schema* ini dipilih karena menyederhanakan *query* analitik — setiap pertanyaan bisnis dapat dijawab melalui operasi *join* tunggal antara tabel fakta dan satu atau lebih tabel dimensi, tanpa memerlukan *join* berantai yang kompleks. Dalam implementasi PySpark, *join* antar-DataFrame dilakukan menggunakan operasi `join()` dengan strategi *broadcast join* untuk tabel dimensi yang berukuran kecil, sehingga memaksimalkan performa eksekusi.
