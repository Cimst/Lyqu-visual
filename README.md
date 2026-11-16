# LYQU VISUAL — Website Portofolio & CV Dinamis
**Dokumentasi Aplikasi Pemrograman Web Python Flask & SQLite**  
*Backend: Python Flask & SQLite | Frontend: HTML5, Tailwind CSS, JavaScript (Montserrat Typography)*

---

## 📌 Deskripsi Proyek
**LYQU VISUAL** adalah aplikasi web **Portofolio & CV Dinamis** untuk studio fotografi kreatif dan visual director (Zaki Mubarok) yang berbasis di Sleman, D.I. Yogyakarta. 

Aplikasi ini dibangun untuk memenuhi seluruh **Syarat dan Ketentuan Tugas UTS Pemrograman Web** dengan arsitektur dua sisi:
1. **Halaman Publik**: Menampilkan profil studio, filosofi karya, showcase portofolio dinamis, rincian gear kamera, kalkulator paket booking, serta portal proofing RAW.
2. **Halaman Pengelola (Dasbor Admin)**: Dilengkapi sistem autentikasi session dan fungsi **CRUD (Create, Read, Update, Delete)** penuh yang terhubung ke database SQLite untuk mengelola karya portofolio, keahlian gear fotografi, dan informasi biodata CV secara real-time.

---

## 🎯 Kesesuaian dengan Syarat & Ketentuan UTS

| Syarat UTS | Status | Implementasi pada Proyek |
| :--- | :---: | :--- |
| **Tema Portofolio / CV Dinamis** | ✅ **100% Sesuai** | Terdapat halaman publik (`/`, `/portofolio`, `/tentang-gear`) dan halaman dasbor pengelola (`/dashboard`). |
| **Penggunaan Teknologi Python** | ✅ **100% Sesuai** | Backend dibangun dengan **Python 3** menggunakan microframework **Flask** dan database **SQLite3** bawaan Python standard library. |
| **Penggunaan Teknologi Frontend** | ✅ **100% Sesuai** | Frontend menggunakan HTML5 semantik, Tailwind CSS, Vanilla JavaScript, serta Google Fonts Montserrat. |
| **Fitur CRUD & Validasi Penuh** | ✅ **100% Sesuai** | Seluruh fungsi **Create, Read, Update, Delete** untuk portofolio dan skills berfungsi penuh tanpa error, dilengkapi validasi form server-side dan flash message. |
| **Tampilan UI/UX Responsif** | ✅ **100% Sesuai** | Tata letak adaptif dan fleksibel di berbagai resolusi layar (Mobile `< 640px`, Tablet `768px`, Laptop, dan Desktop Widescreen). |
| **Kelengkapan Dokumentasi** | ✅ **100% Sesuai** | `README.md` memuat panduan instalasi, struktur proyek, serta akun login penguji. |

---

## 🔐 Kredensial Login Admin (Penguji / Dosen)

Untuk menguji fitur pengelola dan CRUD di halaman Dasbor:
* **URL Login**: [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login)
* **Username**: `admin`
* **Password**: `admin123`
*(Tersedia proteksi session login. Pengguna yang belum login otomatis diredirect dengan pesan peringatan).*

---

## ✨ Fitur-Fitur Utama

### 1. Halaman Publik Dinamis
* **Slide 01 — Beranda Hero**: Headline dinamis, stempel visual LYQU, dan alur alur 3 bento workflow.
* **Slide 02 — Showcase Portofolio Dinamis**: Menampilkan karya foto langsung dari database SQLite dengan filter genre instan (Wedding, Event, Produk, Portrait).
* **Slide 03 — Tentang, Tim & Gear**: Menampilkan biodata profil, pengalaman, filosofi studio, serta daftar gear kamera Sony Alpha & lensa G-Master.
* **Slide 04 — Paket & Kalender Booking**: Simulasi kalkulator DP 30%, pemilihan slot tanggal, dan formulir inquiry yang langsung tersimpan ke SQLite `bookings`.
* **Slide 05 — Portal Klien**: Simulasi proofing RAW dan akses Google Drive.
* **Slide 06 — FAQ & Kontak**: Pertanyaan umum operasional studio dan tautan konsultasi.
* **Rute Dinamis**:
  * `/product/<id>` : Detail paket layanan individual berdasarkan ID produk.
  * `/user/<username>` : Halaman profil direktori kreator dinamis.

### 2. Halaman Pengelola (Dasbor Admin CRUD)
* **Katalog Portofolio (CRUD)**:
  * **Create**: Menambah karya foto baru dengan opsi **Upload Berkas Foto Langsung** (`multipart/form-data`) atau URL/preset foto.
  * **Read**: Menampilkan tabel seluruh karya yang tersimpan di database beserta thumbnail dan metadata.
  * **Update**: Mengedit karya yang sudah ada melalui halaman form edit `/portfolio/edit/<id>` (didukung ganti berkas foto).
  * **Delete**: Menghapus karya dengan tombol konfirmasi keamanan.
* **Manajemen Reservasi & Pesanan Klien**:
  * Melihat daftar formulir pemesanan masuk dari Slide 04 lengkap dengan nama klien, email, link langsung WhatsApp (`wa.me`), rincian paket, lokasi, tanggal, total biaya, dan DP 30%.
  * Fitur konfirmasi status pesanan (*Menunggu* / *Dikonfirmasi*) dan hapus pesanan.
* **Keahlian & Gear CV (CRUD)**:
  * Menambah dan menghapus daftar gear kamera, software post-processing, dan sertifikasi.
* **Pengaturan Biodata CV (Update)**:
  * Memperbarui nama lengkap, role visual director, bio ringkas, jumlah proyek, domisili, dan kontak resmi secara real-time.
* **Validasi Server-Side**:
  * Pengecekan input kosong, panjang karakter minimal, format data, serta umpan balik interaktif melalui *Flash Messages* dengan auto-dismiss 4 detik.

### 3. REST API Endpoint
* `GET /api/portfolios` : Mengembalikan data JSON daftar karya portofolio.
* `GET /api/cv-profile` : Mengembalikan data JSON profil CV dan daftar skills.
* `POST /api/booking-inquiry` : Menerima dan menyimpan data reservasi sesi ke tabel SQLite `bookings`.
* `GET /health` : Status kesehatan server dan koneksi database.

---

## 💻 Panduan Instalasi & Menjalankan Aplikasi Secara Lokal

### Prasyarat
* Komputer dengan **Python 3.9** atau versi lebih baru terinstal.
* Git (opsional).

### Langkah 1: Clone Repositori
```bash
git clone <URL_REPOSITORY_GITHUB_ANDA>
cd lyqu-visual-website
```

### Langkah 2: Buat dan Aktifkan Virtual Environment (Disarankan)
* **Windows (Command Prompt / PowerShell)**:
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```
* **macOS / Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### Langkah 3: Install Dependensi
```bash
pip install -r requirements.txt
```

### Langkah 4: Jalankan Server Flask
```bash
python app.py
```

### Langkah 5: Buka di Browser
Akses aplikasi melalui browser favorit Anda:
* **Halaman Publik**: [http://127.0.0.1:5000](http://127.0.0.1:5000)
* **Dasbor Pengelola**: [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login)

*(Catatan: Database SQLite `database.db` akan dibuat dan diinisialisasi otomatis beserta data awal saat pertama kali aplikasi dijalankan).*

---

## 📁 Struktur Direktori Proyek

```text
lyqu-visual-website/
├── app.py                      # File utama aplikasi Flask (Routing, Controller, Auth)
├── db.py                       # Modul database SQLite (Inisialisasi & Query Helper CRUD)
├── database.db                 # File database SQLite (dihasilkan otomatis)
├── requirements.txt            # Daftar pustaka Python (Flask, Gunicorn)
├── Procfile                    # Konfigurasi deployment server cloud (Render / Railway)
├── README.md                   # Dokumentasi lengkap proyek UTS
├── templates/                  # Template HTML Jinja2
│   ├── base.html               # Template dasar (Head, Fonts Montserrat, Deck Wrapper)
│   ├── index.html              # Halaman beranda utama
│   ├── login.html              # Halaman autentikasi admin pengelola
│   ├── dashboard.html          # Dasbor manajemen pengelola portofolio & CV (CRUD)
│   ├── portfolio_edit.html     # Halaman formulir edit karya (Update CRUD)
│   ├── profile.html            # Halaman profil CV publik
│   ├── partials/               # Komponen parsial (Navbar, Modals, Deck)
│   │   ├── navbar.html         # Unified Floating Glass Navbar & Drawer
│   │   ├── modals.html         # Modal Google SSO & Invoice QRIS DP 30%
│   │   └── deck.html           # Penggabung 6 section slide
│   └── sections/               # Bagian slide presentasi studio
│       ├── beranda.html        # Slide 01: Hero blueprint & 3 bento workflow
│       ├── portofolio.html     # Slide 02: Bento showcase portofolio dinamis
│       ├── tentang-gear.html   # Slide 03: Biodata CV, tim & gear kamera
│       ├── paket-booking.html  # Slide 04: Paket harga, kalender & split ticket
│       ├── portal-proofing.html# Slide 05: Proofing RAW klien & G-Drive
│       └── faq-kontak.html     # Slide 06: FAQ operasional & footer kontak
└── static/                     # Aset statis web
    ├── css/
    │   └── style.css           # Styling kustom, animasi SVG, dan layouting
    ├── js/
    │   ├── main.js             # Logika interaktif, filter galeri, dan kalkulator
    │   ├── data.js             # Data cadangan fallback & konfigurasi
    │   └── tailwind.config.js  # Konfigurasi kustom tema Tailwind (Warna, Font)
    └── images/                 # Aset grafis, foto portofolio & logo resmi
        └── logo/               # Varian logo resmi LYQU VISUAL (PNG Transparan)
```

---

## 🌐 Panduan Deployment Online (Untuk Pengumpulan UTS)

Jika ingin mengunggah ke layanan hosting gratis (contoh: **Render.com**):
1. Unggah proyek ke akun GitHub pribadi Anda (`git push origin main`).
2. Masuk ke [Render.com](https://render.com) dan buat **New Web Service**.
3. Hubungkan repositori GitHub proyek ini.
4. Masukkan konfigurasi:
   * **Runtime**: `Python 3`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `gunicorn app:app`
5. Klik **Deploy Web Service** dan salin URL publik yang dihasilkan (contoh: `https://lyqu-visual.onrender.com`).

---

## 👨‍💻 Identitas Mahasiswa
* **Nama Studio / Brand**: LYQU VISUAL STUDIO
* **Lead Photographer / Visual Director**: Zaki Mubarok
* **Mata Kuliah**: Pemrograman Web (Praktikum & Teori)
* **Tahun Akademik**: 2026
