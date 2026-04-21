# Bab 3: Tata Kelola IT (*IT Governance*)

## 3.1 Keamanan Data (*Data Security*)

Keamanan data merupakan pilar fundamental dalam tata kelola sistem Big Data yang menangani informasi transaksi pelanggan ritel. Dataset `retail_sales_dataset.csv` memuat atribut-atribut yang tergolong sensitif secara bisnis — meliputi *Customer ID* (1.000 identitas pelanggan unik), riwayat pembelian individu, preferensi kategori produk, serta profil demografis berupa usia dan jenis kelamin. Kebocoran atau penyalahgunaan data semacam ini tidak hanya berpotensi merugikan pelanggan secara personal, tetapi juga dapat menghancurkan reputasi perusahaan dan menimbulkan kerugian finansial yang substansial.

Strategi keamanan data yang diterapkan dalam arsitektur solusi ini mencakup tiga lapisan perlindungan yang saling melengkapi:

**a. Enkripsi Data (*Data Encryption*)**

Seluruh data yang tersimpan dalam ekosistem Big Data — baik di *Data Lake* maupun *Data Warehouse* — dilindungi menggunakan enkripsi simetris AES-256 (*Advanced Encryption Standard* dengan panjang kunci 256-bit) untuk data diam (*data at rest*). Sementara itu, data yang ditransmisikan antar-komponen sistem (misalnya, dari klaster Apache Spark ke *Data Warehouse*) diamankan menggunakan protokol TLS 1.3 (*Transport Layer Security*) untuk data bergerak (*data in transit*). Dengan mekanisme ini, bahkan jika pihak yang tidak berwenang berhasil mengakses media penyimpanan fisik atau menyadap lalu lintas jaringan, data yang diperoleh tidak dapat dibaca tanpa kunci dekripsi yang sah.

Dalam konteks dataset ritel ini, enkripsi memastikan bahwa informasi seperti pola pembelian pelanggan tertentu (misalnya, CUST001 yang membeli produk Beauty seharga 150) tidak dapat dieksploitasi oleh pihak ketiga untuk keperluan yang tidak sah, seperti *profiling* ilegal atau penargetan komersial tanpa persetujuan.

**b. Pengendalian Akses (*Access Control*)**

Sistem pengendalian akses berbasis peran (*Role-Based Access Control* / RBAC) diterapkan untuk memastikan bahwa setiap pengguna hanya dapat mengakses data sesuai dengan wewenang dan tanggung jawab fungsionalnya. Dalam konteks organisasi ritel, matriks hak akses dirancang sebagai berikut:

| Peran (*Role*)            | Hak Akses                                                                 |
|---------------------------|---------------------------------------------------------------------------|
| Data Engineer             | Baca-tulis penuh pada *Data Lake* dan *pipeline* ETL                      |
| Data Scientist            | Baca pada *Data Lake* dan *Data Warehouse*; eksekusi model analitik       |
| Manajer Pemasaran (CMO)   | Baca pada *dashboard* agregat; tidak dapat mengakses data individu mentah |
| Manajer Operasional (COO) | Baca pada laporan operasional dan tren penjualan                          |
| Eksekutif (C-Level)       | Baca pada *dashboard* ringkasan KPI                                       |

Dengan pemisahan hak akses ini, seorang CMO yang hanya membutuhkan informasi agregat (misalnya, "total penjualan kategori Clothing sebesar 155.580") tidak akan memiliki akses ke rekaman transaksi individu pelanggan, sehingga risiko penyalahgunaan data diminimalkan.

**c. Audit dan Pemantauan (*Audit Logging & Monitoring*)**

Seluruh aktivitas akses dan modifikasi data dicatat dalam *audit log* yang bersifat *immutable* (tidak dapat diubah). Log ini mencakup informasi mengenai siapa yang mengakses data, kapan akses dilakukan, data apa yang diakses, dan operasi apa yang dijalankan (baca, tulis, hapus). Sistem pemantauan berbasis *Security Information and Event Management* (SIEM) beroperasi secara waktu-nyata untuk mendeteksi pola akses yang anomali — misalnya, percobaan pengunduhan massal data pelanggan yang tidak lazim pada jam-jam di luar operasional normal.

---

## 3.2 Kepatuhan Regulasi (*Regulatory Compliance*)

Pengelolaan data pelanggan dalam skala Big Data tunduk pada kerangka regulasi yang ketat, baik di tingkat nasional maupun internasional. Kepatuhan terhadap regulasi bukan sekadar kewajiban hukum, melainkan juga menjadi prasyarat untuk membangun dan mempertahankan kepercayaan pelanggan.

**a. Undang-Undang Pelindungan Data Pribadi (UU PDP) — Indonesia**

Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP) merupakan landasan hukum utama yang mengatur pengumpulan, pemrosesan, dan penyimpanan data pribadi di Indonesia. Dalam konteks dataset ritel yang digunakan, beberapa atribut data terklasifikasi sebagai data pribadi menurut UU PDP, yaitu *Customer ID* (sebagai pengidentifikasi unik individu), usia, dan jenis kelamin.

Implikasi kepatuhan UU PDP terhadap perancangan arsitektur solusi meliputi: (1) kewajiban memperoleh persetujuan eksplisit (*informed consent*) dari pelanggan sebelum data mereka diproses untuk keperluan analitik; (2) kewajiban menyediakan mekanisme bagi pelanggan untuk mengakses, memperbaiki, atau meminta penghapusan data pribadinya (*right to erasure*); dan (3) kewajiban melaporkan insiden kebocoran data kepada otoritas terkait dalam jangka waktu yang ditentukan.

**b. *General Data Protection Regulation* (GDPR) — Uni Eropa**

Meskipun dataset ini beroperasi dalam konteks domestik, penerapan prinsip-prinsip GDPR tetap relevan sebagai acuan praktik terbaik (*best practice*) dalam pelindungan data berskala internasional. Prinsip utama GDPR yang diadopsi mencakup *data minimization* (hanya mengumpulkan data yang benar-benar diperlukan), *purpose limitation* (data hanya digunakan untuk tujuan yang telah dinyatakan), dan *storage limitation* (data tidak disimpan lebih lama dari yang diperlukan).

Dalam praktiknya, kepatuhan terhadap prinsip-prinsip ini berarti bahwa dataset ritel hanya boleh digunakan untuk analisis perilaku belanja dan optimalisasi layanan sebagaimana dinyatakan dalam kebijakan privasi perusahaan — bukan untuk tujuan lain seperti penjualan data ke pihak ketiga tanpa persetujuan pelanggan.

**c. Mekanisme Implementasi Kepatuhan**

Untuk memastikan kepatuhan yang konsisten, organisasi menerapkan beberapa mekanisme operasional: (1) penunjukan *Data Protection Officer* (DPO) yang bertanggung jawab mengawasi kepatuhan regulasi; (2) pelaksanaan *Data Protection Impact Assessment* (DPIA) sebelum memulai proyek analitik baru; dan (3) penyusunan *data processing agreement* dengan seluruh pihak ketiga yang terlibat dalam pemrosesan data, termasuk penyedia layanan *cloud* dan infrastruktur Big Data.

---

## 3.3 Privasi Data (*Data Privacy*)

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

---

## 3.4 Kualitas Data (*Data Quality*)

Kualitas data merupakan prasyarat fundamental yang menentukan validitas dan keandalan seluruh luaran analitik. Prinsip *"garbage in, garbage out"* berlaku secara absolut dalam konteks Big Data — model prediktif atau segmentasi pelanggan yang dihasilkan dari data berkualitas rendah akan menghasilkan wawasan yang menyesatkan dan keputusan bisnis yang merugikan.

**a. Dimensi Kualitas Data**

Kualitas data dalam arsitektur solusi ini diukur berdasarkan enam dimensi standar:

| Dimensi            | Definisi                                                | Contoh pada Dataset                                                         |
|---------------------|---------------------------------------------------------|-----------------------------------------------------------------------------|
| Kelengkapan         | Tidak ada nilai yang hilang (*missing values*)          | Seluruh 1.000 rekaman memiliki nilai lengkap pada 9 kolom                   |
| Konsistensi         | Format data seragam di seluruh rekaman                  | Format tanggal konsisten (YYYY-MM-DD); Gender hanya "Male"/"Female"         |
| Akurasi             | Nilai data merepresentasikan fakta sebenarnya           | Total Amount = Quantity × Price per Unit (validasi kalkulasi)                |
| Ketepatan Waktu     | Data tersedia pada saat dibutuhkan                      | Data transaksi dimuat ke *warehouse* maksimal H+1 setelah transaksi terjadi |
| Validitas           | Data sesuai dengan aturan domain yang berlaku           | Usia dalam rentang wajar (18–64); Quantity positif (1–4)                    |
| Keunikan            | Tidak ada duplikasi rekaman                             | Setiap *Transaction ID* (1–1000) bersifat unik                             |

**b. Proses Pembersihan Data (*Data Cleaning*)**

Tahap pembersihan data dieksekusi secara otomatis dalam *pipeline* ETL sebelum data dimuat ke *Data Warehouse*. Proses ini mencakup beberapa langkah terstruktur:

Pertama, **deteksi dan penanganan nilai hilang (*missing values*)**: Setiap kolom diperiksa untuk memastikan kelengkapan data. Rekaman dengan nilai hilang pada atribut kritis (seperti *Transaction ID*, *Customer ID*, atau *Total Amount*) ditandai untuk investigasi manual, sementara nilai hilang pada atribut non-kritis dapat diisi menggunakan teknik imputasi statistik (misalnya, median atau modus).

Kedua, **validasi format dan tipe data**: Format tanggal divalidasi terhadap pola YYYY-MM-DD, nilai numerik (*Age, Quantity, Price per Unit, Total Amount*) dipastikan bertipe integer positif, dan nilai kategorikal (*Gender, Product Category*) diverifikasi terhadap daftar nilai yang diizinkan (*whitelist*) — yaitu Male/Female untuk Gender, serta Beauty/Clothing/Electronics untuk Product Category.

Ketiga, **validasi logika bisnis (*business rule validation*)**: Aturan derivasi diperiksa untuk memastikan konsistensi antar-kolom. Secara spesifik, nilai *Total Amount* harus sama dengan hasil perkalian *Quantity* dan *Price per Unit*. Rekaman yang melanggar aturan ini ditandai sebagai anomali dan diarahkan ke antrean investigasi.

Keempat, **deteksi dan penghapusan duplikasi**: Rekaman duplikat diidentifikasi berdasarkan kombinasi *Transaction ID* atau kombinasi *Customer ID + Date + Product Category + Quantity*. Data duplikat dihapus dengan mempertahankan rekaman yang paling lengkap dan terbaru.

**c. Pemantauan Kualitas Data Berkelanjutan (*Continuous Data Quality Monitoring*)**

Kualitas data bukan merupakan aktivitas satu kali, melainkan proses berkelanjutan yang memerlukan pemantauan sistematis. Sistem pemantauan kualitas data otomatis (*data quality monitoring*) diimplementasikan untuk mengevaluasi metrik kualitas pada setiap siklus pemrosesan *batch*. Metrik-metrik tersebut divisualisasikan dalam *dashboard* khusus yang dapat diakses oleh tim *Data Engineering*, sehingga degradasi kualitas data dapat terdeteksi dan ditindaklanjuti secara proaktif sebelum berdampak pada luaran analitik.

Ambang batas (*threshold*) kualitas data ditetapkan secara eksplisit — misalnya, tingkat kelengkapan data minimum 99,5%, tingkat konsistensi format minimum 100%, dan tingkat keberhasilan validasi logika bisnis minimum 99,9%. Jika metrik kualitas pada suatu siklus pemrosesan jatuh di bawah ambang batas yang ditetapkan, sistem secara otomatis mengirimkan peringatan kepada tim terkait dan menahan pemuatan data ke *Data Warehouse* hingga isu kualitas terselesaikan.
