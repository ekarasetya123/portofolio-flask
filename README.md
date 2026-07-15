# Aplikasi Portofolio Flask

Aplikasi portofolio dinamis yang dibangun dengan Python Flask, yang menyediakan panel admin untuk mengelola proyek, keterampilan, profil, dan pesan.

## Fitur

- **Halaman Publik**: Beranda, Tentang, Portofolio, Detail Proyek, Kontak
- **Panel Admin**: Sistem login aman dengan Flask-Login
- **Operasi CRUD**: Membuat, membaca, memperbarui, dan menghapus proyek, keterampilan, dan profil
- **Sistem Pesan**: Pengiriman formulir kontak disimpan ke dalam database dengan status sudah/belum dibaca
- **Upload Gambar**: Upload file yang aman dengan validasi untuk proyek dan foto profil
- **Desain Responsif**: Layout yang ramah mobile dengan CSS custom
- **UI Modern**: Desain bersih dan profesional dengan mikro-interaksi
- **Siap untuk Deployment**: Dikonfigurasi untuk Gunicorn dengan Procfile dan runtime.txt

## Stack Teknologi

- **Backend**: Python 3.x, Flask
- **Database**: SQLite (melalui SQLAlchemy ORM)
- **Autentikasi**: Flask-Login
- **Forms**: Flask-WTF dengan perlindungan CSRF
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Deployment**: Gunicorn, kompatibel dengan Heroku, Railway, Render, PythonAnywhere

## Struktur Proyek

```
portofolio-flask/
├── app.py                
├── config.py               Konfigurasi
├── models.py               Model basis data
├── forms.py                Definisi WTForms
├── requirements.txt        Dependensi Python
├── Procfile                Konfigurasi Gunicorn untuk deployment
├── runtime.txt             Spesifikasi versi Python
├── .gitignore              Atribut diabaikan oleh Git
├── .env.example            Template variabel lingkungan
├── README.md               File ini
├
├── templates/
│   ├── base.html           Template dasar
│   ├── index.html          Halaman beranda
│   ├── about.html          Halaman tentang
│   ├── portfolio.html      Daftar portofolio
│   ├── project_detail.html # Halaman detail proyek individu
│   ├── contact.html        Formulir kontak
│   └── admin/              Template admin
│       ├── login.html
│       ├── index.html      Panel admin
│       ├── projects.html
│       ├── add_project.html
│       ├── edit_project.html
│       ├── profile.html
│       ├── skills.html
│       ├── edit_skill.html
│       ├── add_skill.html
│       └── messages.html
│
├── static/
│   ├── css/
│   │   └── style.css       Stylesheet kustom
│   ├── js/
│   │   └── main.js         Fungsionalitas JavaScript
│   └── uploads/            File yang diunggah (gambar)
│       └── .gitkeep
```

## Instalasi

1. Clone repositori:
   ```bash
   git clone <url-repositori>
   cd portofolio-flask
   ```

2. Buat lingkungan virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Pada Windows: venv\Scripts\activate
   ```

3. Instal dependensi:
   ```bash
   pip install -r requirements.txt
   ```

4. Siapkan variabel lingkungan:
   ```bash
   cp .env.example .env
   # Edit .env dengan nilai sesungguhnya
   ```

5. Inisialisasi basis data:
   ```bash
   flask init-db
   ```

6. Isi basis data dengan data awal:
   ```bash
   python seed.py
   ```

7. Jalankan aplikasi:
   ```bash
   flask run
   ```
   Atau untuk produksi:
   ```bash
   gunicorn app:app
   ```

## Variabel Lingkungan

Buat file `.env` berdasarkan `.env.example` dengan variabel berikut:

- `SECRET_KEY`: Kunci rahasia untuk sesi Flask dan perlindungan CSRF
- `FLASK_ENV`: Lingkungan (development/production)
- `FLASK_APP`: Titik masuk (biasanya `app.py`)
- `DATABASE_URL`: String koneksi basis data (default: SQLite)
- `UPLOAD_FOLDER`: Direktori untuk file yang diunggah
- `MAX_CONTENT_LENGTH`: Maksimum ukuran file upload dalam byte
- `ADMIN_USERNAME`: Nama pengguna admin default (untuk penyetelan awal)
- `ADMIN_EMAIL`: Email admin default (untuk penyetelan awal)
- `ADMIN_PASSWORD`: Kata sandi admin default (untuk penyetelan awal - ubah setelah login pertama!)

## Fitur secara Detail

### Otentikasi

- Sistem login aman dengan hash kata sandi
- Akses dashboard hanya untuk admin
- Pengelolaan sesi dengan Flask-Login

### Manajemen Proyek

- Tambah, edit, hapus proyek
- Upload gambar proyek dengan validasi
- Tambah tautan GitHub dan demo langsung
- Kategorisasi proyek dengan tag teknologi

### Manajemen Profil

- Perbarui informasi pribadi, headline, dan bio
- Unggah foto profil
- Kelola keterampilan dengan tingkat kemahiran

### Bagian Keterampilan

- Tambah keterampilan dengan persentase kemahiran (0-100%)
- Bar progres visual untuk tingkat keterampilan

### Sistem Kontak

- Formulir kontak dengan validasi
- Pesan disimpan dalam basis data
- Fungsionalitas menandai sebagai sudah/belum dibaca
- Hapus pesan

## Fitur Desain

- **CSS Kustom**: Tanpa Bootstrap atau Tailwind - penamaan gaya sepenuhnya kustom dengan Bootstrap 5 sebagai dasar
- **Tipografi**: Playfair Display untuk judul, Inter untuk teks tubuh
- **Skema Warna**: Palet minimalis gelap profesional dengan aksen mint
- **Layout Responsif**: Bekerja di ponsel, tablet, dan desktop
- **Mikro-interaksi**: Efek hover, transisi, animasi
- **Umpan Balik Visual**: Validasi formulir, pesan flash, keadaan loading

## Model Basis Data

- **Pengguna**: Model otentikasi (mewarisi dari Flask-Login UserMixin)
- **Profil**: Model singleton untuk informasi pribadi
- **Keterampilan**: Keterampilan dengan nama, kategori, dan tingkat kemahiran
- **Proyek**: Proyek portofolio dengan gambar, deskripsi, tautan
- **Pesan**: Pengiriman formulir kontak

## Deployment

Aplikasi ini siap untuk deployment ke platform seperti:

- **Heroku**: Menggunakan Procfile dan requirements.txt
- **Railway**: Mendeteksi otomatis aplikasi Python
- **Render**: Bekerja dengan layanan web Python standar
- **PythonAnywhere**: Kompatibel dengan panduan deployment Flask mereka
- **Docker**: Dapat dengan mudah dikontainerkan

### Contoh Deployment ke Heroku
```bash
heroku create nama-aplikasi-anda
git push heroku main
heroku run python seed.py
```

## Fitur Keamanan

- Perlindungan CSRF pada semua formulir
- Hash kata sandi yang aman dengan Werkzeug
- Validasi upload file (tipe dan ukuran)
- Sanitisasi dan validasi input
- Konfigurasi berdasarkan lingkungan
- Pencegahan injeksi SQL melalui ORM
- Proteksi rute admin

## Kustomisasi

1. **Styling**: Ubah `static/css/style.css` untuk warna, font, dan tata letak
2. **Konten**: Perbarui data awal di `app.py` pada perintah `init-db` atau melalui panel admin
3. **Fitur**: Tambah model baru di `models.py` dan operasi CRUD yang sesuai
4. **Template**: Ubah template HTML di direktori `templates/`

## Lisensi

Proyek ini bersifat terbuka sumber dan tersedia di bawah Lisensi MIT.

## Pengakuan

- Dibuat sebagai proyek capstone yang menunjukkan pengembangan full-stack Flask
- Terinspirasi oleh desain portofolio modern
- Dibangun dengan praktik terbaik untuk keamanan dan pemeliharaan