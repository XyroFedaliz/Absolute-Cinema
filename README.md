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
AbsoluteCinema/
├── MainProgram.py # Main logic aplikasi
├── Database.py # Fungsi query MySQL
├── db_bioskop_v2.sql # Struktur & data awal database
├── seats_ui.py # UI layout pemilihan kursi
├── payment_ui.py # UI pembayaran
├── historybill_ui.py # UI bukti transaksi
└── README.md # Dokumentasi ini

---

## 💻 Cara Menjalankan

1. Clone repositori:

git clone https://github.com/username/AbsoluteCinema.git
cd AbsoluteCinema

2. Install dependensi:

pip install PyQt5 mysql-connector-python qrcode pillow

3. Import database:

Gunakan tools seperti phpMyAdmin atau MySQL Workbench
Import file db_bioskop_v2.sql

4. Jalankan aplikasi:
   
python MainProgram.py

🛠️ Teknologi yang Digunakan
Python 3
PyQt5 (GUI)
MySQL
qrcode + pillow
Qt Designer (untuk UI)

📄 Lisensi
Proyek ini dibuat untuk tujuan pembelajaran. Bebas digunakan dan dimodifikasi. Tidak diperjualbelikan.

—

📌 Catatan:
- Ganti bagian `https://github.com/username/AbsoluteCinema.git` dengan link GitHub kamu sendiri
- Folder screenshots/ berisi gambar tampilan aplikasi (kalau kamu mau tampilkan)
- Ganti nama author sesuai username GitHub kamu

Kalau mau, saya bantu juga buat file .gitignore, lisensi MIT, atau struktur folder lengkap. Mau sekalian?







