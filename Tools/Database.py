import qrcode
from io import BytesIO
import mysql.connector

class Database: #<-- Kelas Database untuk mengelola koneksi dan operasi database
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="db_bioskop_v3"
            )
            self.cursor = self.conn.cursor()
            print("Koneksi berhasil ke database!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.conn = None
            self.cursor = None
            
    def reconnect(self): #<-- Method untuk menyambungkan kembali ke database jika koneksi terputus
        """Sambungkan kembali ke database jika koneksi terputus."""
        try:
            if not self.conn.is_connected():
                self.conn.reconnect()
                self.cursor = self.conn.cursor()
                print("Reconnected to the database!")
        except mysql.connector.Error as err:
            print(f"Error reconnecting: {err}")
            
    def cek_user(self, username, password): #<-- Method untuk mengecek apakah user ada di database berdasarkan username dan password
        """Cek login user berdasarkan username dan password."""
        self.reconnect()
        if self.cursor:
            try:
                query = "SELECT id_akun, role FROM akun WHERE username = %s AND password = %s"
                self.cursor.execute(query, (username, password))
                return self.cursor.fetchone()
            except Exception as e:
                print(f"Error checking user: {e}")
                return None


    def insert_user(self, username, password): #<-- Method untuk memasukkan user baru ke dalam database
        """Insert user baru ke dalam database."""
        self.reconnect()
        if self.cursor:
            try:
                query = "INSERT INTO akun (username, password, role) VALUES (%s, %s, 'member')"
                self.cursor.execute(query, (username, password))
                self.conn.commit()
                return True
            except mysql.connector.IntegrityError:
                print("Username sudah terdaftar!")
                return False
            except Exception as e:
                print(f"Error inserting user: {e}")
                return False
        return 
    
    def get_film_by_id(self, film_id): #<-- Method untuk mendapatkan detail film berdasarkan ID
        self.reconnect()
        query = "SELECT nama_film, sutradara, aktor, sinopsis, poster_film, produksi, age FROM film WHERE id_film = %s"
        self.cursor.execute(query, (film_id,))
        return self.cursor.fetchone()

    def update_film(self, film_id, nama, sutradara, aktor, sinopsis, produksi, age, poster_blob): #<-- Method untuk memperbarui detail film di database
        self.reconnect()
        query = """
            UPDATE film SET
                nama_film = %s,
                sutradara = %s,
                aktor = %s,
                sinopsis = %s,
                produksi = %s,
                age = %s,
                poster_film = %s
            WHERE id_film = %s
        """
        self.cursor.execute(query, (nama, sutradara, aktor, sinopsis, produksi, age, poster_blob, film_id))
        self.conn.commit()
    
    def get_all_active_films(self, limit=10): #<-- Method untuk mendapatkan semua film aktif dengan batasan jumlah
        self.reconnect()
        query = "SELECT id_film, poster_film FROM film WHERE is_active = 1 ORDER BY id_film ASC LIMIT %s"
        self.cursor.execute(query, (limit,))
        return self.cursor.fetchall()

    def soft_delete_film(self, film_id): #<-- Method untuk menghapus film secara soft delete dengan mengosongkan detailnya
        self.reconnect()
        query = """
            UPDATE film SET
                nama_film = '',
                sutradara = '',
                aktor = '',
                sinopsis = '',
                poster_film = NULL,
                produksi = '',
                age = '',
                is_active = 0
            WHERE id_film = %s
        """
        self.cursor.execute(query, (film_id,))
        self.conn.commit()
        
    def reactivate_film(self, film_id): #<-- Method untuk mengaktifkan kembali film yang telah dihapus secara soft delete
        self.reconnect()
        query = "UPDATE film SET is_active = 1 WHERE id_film = %s AND is_active = 0"
        self.cursor.execute(query, (film_id,))
        self.conn.commit()
    
    def get_film_status(self, film_id): #<-- Method untuk mendapatkan status film (aktif, tidak aktif, atau tidak ada)
        self.reconnect()
        query = "SELECT is_active FROM film WHERE id_film = %s"
        self.cursor.execute(query, (film_id,))
        result = self.cursor.fetchone()
        if result is None:
            return "not_exist"
        elif result[0] == 1:
            return "active"
        else:
            return "inactive"
    
    def get_poster_by_id(self, film_id): #<-- Method untuk mendapatkan poster film berdasarkan ID
        self.reconnect()
        query = "SELECT poster_film FROM film WHERE id_film = %s AND is_active = 1"
        self.cursor.execute(query, (film_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_detail_film(self, film_id): #<-- Method untuk mendapatkan detail film berdasarkan ID
        self.reconnect()
        query = """
            SELECT tanggal_tayang, waktu_tayang
            FROM detail_film
            WHERE id_film = %s
            ORDER BY tanggal_tayang, waktu_tayang
        """
        self.cursor.execute(query, (film_id,)) 
        return self.cursor.fetchall()
        
    def update_tanggal_film(self, id_film, tanggal_lama, tanggal_baru): #<-- Method untuk memperbarui tanggal tayang film
        self.reconnect()
        query = "UPDATE detail_film SET tanggal_tayang = %s WHERE id_film = %s AND tanggal_tayang = %s"
        self.cursor.execute(query, (tanggal_baru, id_film, tanggal_lama))
        self.conn.commit()

    def update_jam_film(self, id_film, tanggal, jam_lama, jam_baru): #<-- Method untuk memperbarui jam tayang film
        self.reconnect()
        query = """
            UPDATE detail_film
            SET waktu_tayang = %s
            WHERE id_film = %s AND tanggal_tayang = %s AND waktu_tayang = %s
        """
        self.cursor.execute(query, (jam_baru, id_film, tanggal, jam_lama))
        self.conn.commit()

    def get_all_active_films(self, limit=10): #<-- Method untuk mendapatkan semua film aktif dengan batasan jumlah
        self.reconnect()
        self.cursor.execute(
            "SELECT id_film, poster_film, nama_film FROM film WHERE is_active = 1 ORDER BY id_film ASC LIMIT %s",
            (limit,)
        )   
        return self.cursor.fetchall()

    def get_nama_user_by_id(self, user_id): #<-- Method untuk mendapatkan nama user berdasarkan ID
        self.reconnect()
        self.cursor.execute("SELECT username FROM akun WHERE id_akun = %s", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else "USER"
    
    def get_role_by_user_id(self, user_id): #<-- Method untuk mendapatkan role user berdasarkan ID
        self.reconnect()
        self.cursor.execute("SELECT role FROM akun WHERE id_akun = %s", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_detail_film_id(self, id_film, tanggal, jam): #<-- Method untuk mendapatkan ID detail film berdasarkan ID film, tanggal, dan jam tayang
        self.reconnect()
        query = """
            SELECT id_detail_film FROM detail_film
            WHERE id_film = %s AND tanggal_tayang = %s AND waktu_tayang = %s
        """
        self.cursor.execute(query, (id_film, tanggal, jam))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_all_kursi(self): #<-- Method untuk mendapatkan semua kursi yang tersedia
        self.reconnect()
        self.cursor.execute("SELECT id_kursi, nama_kursi, tipe FROM kursi")
        return self.cursor.fetchall()

    def get_kursi_terisi(self, id_detail_film): #<-- Method untuk mendapatkan kursi yang sudah terisi berdasarkan ID detail film
        self.reconnect()
        self.cursor.execute("SELECT id_kursi FROM pemesanan WHERE id_detail_film = %s", (id_detail_film,))
        return [row[0] for row in self.cursor.fetchall()]

    def get_harga_by_detail_id(self, id_detail_film): #<-- Method untuk mendapatkan harga tiket berdasarkan ID detail film
        self.reconnect()
        self.cursor.execute("SELECT harga FROM detail_film WHERE id_detail_film = %s", (id_detail_film,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def get_harga_by_detail_id(self, id_detail_film): #<-- Method untuk mendapatkan harga tiket berdasarkan ID detail film
        self.reconnect()
        self.cursor.execute("SELECT harga FROM detail_film WHERE id_detail_film = %s", (id_detail_film,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def get_film_by_detail_id(self, id_detail_film): #<-- Method untuk mendapatkan nama film berdasarkan ID detail film
        self.reconnect()
        self.cursor.execute("""
            SELECT f.nama_film
            FROM detail_film d
            JOIN film f ON d.id_film = f.id_film
            WHERE d.id_detail_film = %s
        """, (id_detail_film,))
        result = self.cursor.fetchone()
        return result[0] if result else "-"
    
    def get_film_by_detail_id(self, id_detail_film): #<-- Method untuk mendapatkan nama film berdasarkan ID detail film
        self.reconnect()
        self.cursor.execute("""
            SELECT f.nama_film
            FROM detail_film d
            JOIN film f ON d.id_film = f.id_film
            WHERE d.id_detail_film = %s
        """, (id_detail_film,))
        result = self.cursor.fetchone()
        return result[0] if result else "-"

    def get_tipe_kursi(self, nama_kursi): #<-- Method untuk mendapatkan tipe kursi berdasarkan nama kursi
        self.reconnect()
        self.cursor.execute("SELECT tipe FROM kursi WHERE nama_kursi = %s", (nama_kursi,))
        result = self.cursor.fetchone()
        return result[0] if result else "reguler"

    def get_id_kursi_by_name(self, nama_kursi): #<-- Method untuk mendapatkan ID kursi berdasarkan nama kursi
        self.reconnect()
        self.cursor.execute("SELECT id_kursi FROM kursi WHERE nama_kursi = %s", (nama_kursi,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def insert_histori_bill(self, id_akun, id_detail_film, kursi_list, total, metode, qr_text): #<-- Method untuk memasukkan data histori bill ke dalam database
        self.reconnect()
        kursi_str = ", ".join(kursi_list)
        qr = qrcode.make(qr_text)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_bytes = buffer.getvalue()

        self.cursor.execute("""
            INSERT INTO histori_bill (id_akun, id_detail_film, kursi, total, metode_pembayaran, qr_text, qr_image)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (id_akun, id_detail_film, kursi_str, total, metode, qr_text, qr_bytes))
        self.conn.commit()
    
    def insert_pemesanan(self, id_akun, id_detail_film, id_kursi, harga, bank, va): #<-- Method untuk memasukkan data pemesanan dan pembayaran ke dalam database
        self.reconnect()
        try:
            self.cursor.execute("""
                INSERT INTO pemesanan (id_detail_film, id_kursi, id_akun, status, waktu_pesan)
                VALUES (%s, %s, %s, 'terisi', NOW())
            """, (id_detail_film, id_kursi, id_akun))
            id_pemesanan = self.cursor.lastrowid

            self.cursor.execute("""
                INSERT INTO payment (id_pemesanan, metode, total, waktu_bayar)
                VALUES (%s, %s, %s, NOW())
            """, (id_pemesanan, bank + " - VA: " + va, harga))

            self.conn.commit()
            print(f"[LOG] Pemesanan & pembayaran berhasil disimpan (id_pemesanan: {id_pemesanan})")

        except mysql.connector.Error as err:
            print(f"[ERROR] Gagal menyimpan pemesanan: {err}")
            self.conn.rollback()

    def get_detail_film_jadwal(self, id_detail_film):   #<-- Method untuk mendapatkan jadwal tayang film berdasarkan ID detail film
        self.reconnect()
        self.cursor.execute("SELECT tanggal_tayang, waktu_tayang FROM detail_film WHERE id_detail_film = %s", (id_detail_film,))
        result = self.cursor.fetchone()
        return result if result else ("-", "-")
    
    def get_histori_by_user(self, id_akun): #<-- Method untuk mendapatkan histori pembayaran berdasarkan ID akun user
        self.reconnect()
        self.cursor.execute("""
            SELECT id_detail_film, kursi, total, metode_pembayaran, waktu_bayar
            FROM histori_bill
            WHERE id_akun = %s
            ORDER BY waktu_bayar DESC
        """, (id_akun,))
        return self.cursor.fetchall()

    def get_semua_laporan(self): #<-- Method untuk mendapatkan semua laporan histori pembayaran
        self.reconnect()
        query = """
            SELECT h.id_detail_film, 
                h.kursi, 
                h.total, 
                h.metode_pembayaran, 
                h.waktu_bayar, 
                a.username
            FROM histori_bill h
            JOIN akun a ON h.id_akun = a.id_akun
            ORDER BY h.waktu_bayar DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()


    
