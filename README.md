# 🎬 AbsoluteCinema - Sistem Pemesanan Tiket Bioskop (Desktop App)

AbsoluteCinema adalah aplikasi pemesanan tiket bioskop berbasis desktop (GUI PyQt5 + MySQL). Aplikasi ini mendukung fitur login, pengelolaan film (oleh admin), pemilihan jadwal tayang dan kursi, hingga proses pembayaran dan bukti transaksi dalam bentuk QR Code.

---

## 🚀 Fitur Utama

- 👥 Login dan Register untuk user dan admin
- 🎥 Pengelolaan Film (judul, sinopsis, poster, jadwal tayang)
- 📆 Pemilihan tanggal & jam tayang
- 🪑 Pemilihan kursi berdasarkan layout tetap (44 kursi A1–G6)
- 💳 Pembayaran dengan metode Virtual Account (BCA, BRI, Mandiri, DANA)
- 🧾 Bukti transaksi dalam bentuk QR Code
- 📚 Riwayat transaksi (history_bill)

---

## 📸 Tampilan Aplikasi

![home](screenshots/home.png)
![kursi](screenshots/seats.png)
![payment](screenshots/payment.png)
![history](screenshots/history.png)

> Gambar di atas merupakan contoh layout tampilan pengguna.

---

## 🧩 Struktur Folder
```   
AbsoluteCinema/
├── MainProgram.py # Entry point aplikasi
├── resources_rc.py # Resource gambar/icon (dari Qt Designer)
│
├── Tools/
│ ├── Database.py # Semua fungsi koneksi & query MySQL
│ └── db_bioskop_v3.sql # Struktur & data awal database
│
├── UI/ # Semua tampilan (UI) dari halaman aplikasi
│ ├── detail_ui.py
│ ├── history_bill_ui.py
│ ├── history_ui.py
│ ├── home_admin_ui.py
│ ├── home_user_ui.py
│ ├── laporan_ui.py
│ ├── loading.py
│ ├── login_ui.py
│ ├── payment_ui.py
│ ├── pilih_film_ui.py
│ ├── register_ui.py
│ ├── resources_rc.py
│ ├── seats_ui.py
│ ├── update_detail_ui.py
│ └── update_film_ui.py
```   
---

## 💻 Cara Menjalankan

1. Clone repositori:
```
git clone https://github.com/username/AbsoluteCinema.git
cd AbsoluteCinema
```
2. Install dependensi:
```
pip install PyQt5 mysql-connector-python qrcode pillow
```
3. Import database:

Gunakan tools seperti phpMyAdmin atau MySQL Workbench
Import file db_bioskop_v2.sql

4. Jalankan aplikasi:
```   
python MainProgram.py
```
---
🛠️ Teknologi yang Digunakan
Python 3
PyQt5 (GUI)
MySQL
qrcode + pillow
Qt Designer (untuk UI)

---

📄 Lisensi
Proyek ini dibuat untuk tujuan pembelajaran. Bebas digunakan dan dimodifikasi. Tidak diperjualbelikan.






