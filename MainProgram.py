import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QGraphicsDropShadowEffect, QInputDialog, QFileDialog, QInputDialog, QHeaderView
from PyQt5.QtGui import QPixmap, QColor, QPixmap, QPainter, QPainterPath, QImage, QStandardItemModel, QStandardItem
from PyQt5.QtCore import QRectF,  Qt, QBuffer, QByteArray
from PyQt5 import QtCore
from datetime import datetime, timedelta
import qrcode
from io import BytesIO
from UI.loading import Ui_SplashScreen
from UI.login_ui import Ui_MainWindow as Ui_Login
from UI.register_ui import Ui_MainWindow as Ui_Register
from UI.payment_ui import Ui_MainWindow as Ui_Payment
from UI.home_admin_ui import Ui_MainWindow as Ui_HomeAdmin
from UI.home_user_ui import Ui_MainWindow as Ui_HomeUser
from UI.pilih_film_ui import Ui_MainWindow as Ui_PilihFilm
from UI.laporan_ui import Ui_MainWindow as Ui_Laporan
from UI.update_film_ui import Ui_MainWindow as Ui_UpdateFilm
from UI.update_detail_ui import Ui_MainWindow as Ui_UpdateDetail
from UI.history_ui import Ui_MainWindow as Ui_History
from UI.history_bill_ui import Ui_MainWindow as Ui_HistoryBill
from UI.seats_ui import Ui_MainWindow as Ui_Seats
from UI.detail_ui import Ui_MainWindow as Ui_Detail
from Tools.Database import Database
from UI import resources_rc
db = Database()

counter = 0

# ======================================== LOADING PAGE ========================================= #
class SplashScreen(QMainWindow):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint) 
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self) #<-- Efek bayangan pada frame
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0) 
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress) 
        self.timer.start(35)

        self.ui.label_description.setText("<strong>WELCOME</strong> TO ABSOLUTE CINEMA")
        QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>LOADING</strong> DATABASE"))
        QtCore.QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))
        QtCore.QTimer.singleShot(1000, lambda: self.ui.label_loading.setText("loading.."))
        QtCore.QTimer.singleShot(1500, lambda: self.ui.label_loading.setText("loading..."))
        self.show()

    def progress(self): #<-- Fungsi untuk mengupdate progress bar
        global counter
        self.ui.progressBar.setValue(counter)

        if counter > 100:
            self.timer.stop()
            self.main = LoginWindow()
            self.main.show()
            self.close()

        counter += 1

# ======================================== HALAMAN LOGIN ========================================= #
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.ui.to_login.clicked.connect(self.method_signin)
        self.ui.to_register.clicked.connect(self.open_register)
    
    def method_signin(self): #<-- Fungsi untuk melakukan login
        username = self.ui.isi_username.text()
        password = self.ui.isi_password.text()
        user_data = db.cek_user(username, password) 
        
        if not username or not password :
            self.ui.label_info.setText("Isi semua kolom!")
            self.ui.label_info.setStyleSheet("color: red;")
            return

        if user_data: #<-- Jika data user ditemukan
            self.logged_in_user_id, role = user_data  
            if role == "admin":
                self.Admin()
            elif role == "member":
                self.User()
        else:
            self.ui.label_info.setText("Username atau password salah!")
            self.ui.label_info.setStyleSheet("color: red;")
    
    def keyPressEvent(self, event): #<-- Fungsi untuk menangani event key press
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.ui.to_login.click()

    def Admin(self): #<-- membuka tampilan admin
        self.admin_window = AdminWindow(self.logged_in_user_id)
        self.admin_window.show()
        self.close()

    def User(self): #<-- membuka tampilan user
        self.user_window = UserWindow(self.logged_in_user_id)
        self.user_window.show()
        self.close()

    def open_register(self): #<-- membuka tampilan register
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

# ======================================== HALAMAN REGISTER ========================================= #
class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Register()
        self.ui.setupUi(self)
        self.ui.to_register.clicked.connect(self.handle_signup)
        self.ui.to_login.clicked.connect(self.open_login)
        self.ui.to_register.setEnabled(False)
        self.ui.syarat_1.toggled.connect(self.setuju_ketentuan)

    def handle_signup(self):
        username = self.ui.isi_username.text()
        password = self.ui.isi_password.text()
        confirm_password = self.ui.isi_confirmpw.text()
        
        if not username or not password or not confirm_password: #<-- Cek apakah semua kolom terisi
            self.ui.label_info.setText("Isi semua kolom!")
            self.ui.label_info.setStyleSheet("color: red;")
            return

        if password != confirm_password: #<-- Cek Password
            self.ui.label_info.setText("Password tidak cocok!")
            self.ui.label_info.setStyleSheet("color: red;")
            return

        if db.insert_user(username, password):
            self.ui.label_info.setText("Pendaftaran berhasil!")
            self.ui.label_info.setStyleSheet("color: green;")
            self.open_login()
        else:
            self.ui.label_info.setText("Username sudah terdaftar!")
            self.ui.label_info.setStyleSheet("color: red;")
            
    def setuju_ketentuan(self): #<-- mengaktifkan tombol register jika checkbox disetujui
        if self.ui.syarat_1.isChecked():
            self.ui.to_register.setEnabled(True)
        else:
            self.ui.to_register.setEnabled(False)
    
    def keyPressEvent(self, event): #<-- Fungsi untuk menangani event key press
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.ui.to_register.click()

    def open_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

# ======================================== HALAMAN ADMIN ========================================= #
class AdminWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.ui = Ui_HomeAdmin()
        self.ui.setupUi(self)
        self.user_id = user_id  #<-- Menyimpan user_id 
        self.selected_tanggal = None  #<-- menyimpan tanggal yang dipilih
        self.ui.to_pesanfilm.clicked.connect(self.open_transaction)
        self.ui.tombol_kembali.clicked.connect(self.open_login)
        self.ui.to_updatefilm.clicked.connect(self.open_update_film)
        self.ui.to_laporan.clicked.connect(self.open_laporan)

    def open_transaction(self):
        self.transaction_window = PilihFilmWindow(self.user_id)
        self.transaction_window.show()
        self.close()

    def open_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
        
    def open_update_film(self): 
        self.login_window = update_film_window(self.user_id)
        self.login_window.show()
        self.close()

    def open_laporan(self):
        self.laporan_window = LaporanWindow(self.user_id)
        self.laporan_window.show()
        self.close()

# ======================================== HALAMAN HOME USER ========================================= #
class UserWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.ui = Ui_HomeUser()
        self.ui.setupUi(self)
        self.user_id = user_id #<-- Menyimpan user_id
        self.ui.to_pesanfilm.clicked.connect(self.open_transaction)
        self.ui.to_history.clicked.connect(self.open_history)
        self.ui.tombol_kembali.clicked.connect(self.open_login)
        nama = db.get_nama_user_by_id(self.user_id) #<-- menampilkan nama user
        if nama:
            self.ui.label_username.setText(str(nama))
        self.load_all_posters()
            
    def set_rounded_pixmap(self, label, pixmap): #<-- mengatur pixmap gambar agar sesuai dengan label
        size = label.size()
        rounded_pixmap = QPixmap(size)
        rounded_pixmap.fill(Qt.transparent)
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        rect = QRectF(0, 0, size.width(), size.height())
        tl = 0
        tr = 20
        br = 0
        bl = 35  
        
        #<-- Mengatur path untuk rounded corners
        path.moveTo(rect.left() + tl, rect.top())
        path.lineTo(rect.right() - tr, rect.top())
        path.quadTo(rect.right(), rect.top(), rect.right(), rect.top() + tr)
        path.lineTo(rect.right(), rect.bottom() - br)
        path.quadTo(rect.right(), rect.bottom(), rect.right() - br, rect.bottom())
        path.lineTo(rect.left() + bl, rect.bottom())
        path.quadTo(rect.left(), rect.bottom(), rect.left(), rect.bottom() - bl)
        path.lineTo(rect.left(), rect.top() + tl)
        path.quadTo(rect.left(), rect.top(), rect.left() + tl, rect.top())
        #<-- Mengatur clip path untuk menggambar rounded corners
        painter.setClipPath(path)
        
        scaled = pixmap.scaled(size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        x = (size.width() - scaled.width()) // 2
        y = (size.height() - scaled.height()) // 2
        painter.drawPixmap(x, y, scaled)
        painter.end()
        #<-- Mengatur pixmap pada label
        label.setPixmap(rounded_pixmap)
        label.setAlignment(Qt.AlignCenter)
    
    def load_all_posters(self): #<-- Fungsi untuk memuat semua poster film
        all_films = db.get_all_active_films(limit=5)
        for i, film in enumerate(all_films):
            id_film, poster_blob, nama_film = film
            #<-- Mengambil label poster dan judul berdasarkan index
            label_poster = getattr(self.ui, f'isi_poster{i+1}', None)
            label_judul = getattr(self.ui, f'isi_judul{i+1}', None)

            if label_poster and poster_blob:
                pixmap = QPixmap()
                pixmap.loadFromData(poster_blob)
                self.set_rounded_pixmap(label_poster, pixmap)
            else:
                label_poster.setText("No image")

            if label_judul:
                label_judul.setText(nama_film)
    
    def open_transaction(self):
        self.transaction_window = PilihFilmWindow(self.user_id)
        self.transaction_window.show()
        self.close()
    
    def open_history(self):
        self.history_window = HistoryWindow(self.user_id)
        self.history_window.show()
        self.close()

    def open_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

# ======================================== HALAMAN UPDATE FILM (ADMIN) ========================================= #
class update_film_window(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id  
        self.ui = Ui_UpdateFilm()
        self.ui.setupUi(self)
        self.ui.tombol_kembali.clicked.connect(self.open_admin)
        self.ui.label_home.clicked.connect(self.refresh) 
        self.load_all_posters() #<-- Memuat semua poster film yang ada di database
        self.update_button_labels() #<-- Memperbarui label tombol update/add film
        
        self.ui.delete1.clicked.connect(lambda: self.handle_deletefilm(1)) #<-- Menghubungkan tombol delete dengan fungsi handle_deletefilm sesuai dengan ID film
        self.ui.delete2.clicked.connect(lambda: self.handle_deletefilm(2))
        self.ui.delete3.clicked.connect(lambda: self.handle_deletefilm(3))
        self.ui.delete4.clicked.connect(lambda: self.handle_deletefilm(4))
        self.ui.delete5.clicked.connect(lambda: self.handle_deletefilm(5))
        self.ui.delete6.clicked.connect(lambda: self.handle_deletefilm(6))
        self.ui.delete7.clicked.connect(lambda: self.handle_deletefilm(7))
        self.ui.delete8.clicked.connect(lambda: self.handle_deletefilm(8))
        self.ui.delete9.clicked.connect(lambda: self.handle_deletefilm(9))
        self.ui.delete10.clicked.connect(lambda: self.handle_deletefilm(10))
        
        self.ui.update1.clicked.connect(lambda: self.handle_update_film(1)) #<-- Menghubungkan tombol update dengan fungsi handle_update_film sesuai dengan ID film
        self.ui.update2.clicked.connect(lambda: self.handle_update_film(2))
        self.ui.update3.clicked.connect(lambda: self.handle_update_film(3))
        self.ui.update4.clicked.connect(lambda: self.handle_update_film(4))
        self.ui.update5.clicked.connect(lambda: self.handle_update_film(5))
        self.ui.update6.clicked.connect(lambda: self.handle_update_film(6))
        self.ui.update7.clicked.connect(lambda: self.handle_update_film(7))
        self.ui.update8.clicked.connect(lambda: self.handle_update_film(8))
        self.ui.update9.clicked.connect(lambda: self.handle_update_film(9))
        self.ui.update10.clicked.connect(lambda: self.handle_update_film(10))
        
        self.ui.isi_poster1 #<-- Mengambil semua label poster yang ada di UI
        self.ui.isi_poster2
        self.ui.isi_poster3
        self.ui.isi_poster4
        self.ui.isi_poster5
        self.ui.isi_poster6
        self.ui.isi_poster7
        self.ui.isi_poster8
        self.ui.isi_poster9
        self.ui.isi_poster10
        
    def set_rounded_pixmap(self, label, pixmap): #<-- Fungsi untuk mengatur pixmap gambar agar sesuai dengan label
        size = label.size()
        rounded_pixmap = QPixmap(size)
        rounded_pixmap.fill(Qt.transparent)
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        rect = QRectF(0, 0, size.width(), size.height())
        tl = 0
        tr = 20
        br = 0
        bl = 35  
        #<-- Mengatur path untuk rounded corners
        path.moveTo(rect.left() + tl, rect.top())
        path.lineTo(rect.right() - tr, rect.top())
        path.quadTo(rect.right(), rect.top(), rect.right(), rect.top() + tr)
        path.lineTo(rect.right(), rect.bottom() - br)
        path.quadTo(rect.right(), rect.bottom(), rect.right() - br, rect.bottom())
        path.lineTo(rect.left() + bl, rect.bottom())
        path.quadTo(rect.left(), rect.bottom(), rect.left(), rect.bottom() - bl)
        path.lineTo(rect.left(), rect.top() + tl)
        path.quadTo(rect.left(), rect.top(), rect.left() + tl, rect.top())
        #<-- Mengatur clip path untuk menggambar rounded corners
        painter.setClipPath(path)
        #<-- Mengatur ukuran pixmap agar sesuai dengan label
        scaled = pixmap.scaled(size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        x = (size.width() - scaled.width()) // 2
        y = (size.height() - scaled.height()) // 2
        painter.drawPixmap(x, y, scaled)
        painter.end()
        
        label.setPixmap(rounded_pixmap)
        label.setAlignment(Qt.AlignCenter)
        
    def load_all_posters(self): #<-- Fungsi untuk memuat semua poster film dari database
        for film_id in range(1, 11):
            label = getattr(self.ui, f'isi_poster{film_id}', None) #<-- Mengambil label poster berdasarkan ID film
            if label:
                poster_blob = db.get_poster_by_id(film_id) #<-- Mengambil poster dari database berdasarkan ID film
                if poster_blob:
                    pixmap = QPixmap()
                    pixmap.loadFromData(poster_blob)
                    self.set_rounded_pixmap(label, pixmap)
                else:
                    label.clear()

    def refresh_ui(self):
        self.load_all_posters()

    def handle_deletefilm(self, film_id): #<-- Fungsi untuk menghapus film berdasarkan ID
        reply = QMessageBox.question(
            self, 'Konfirmasi', f'Yakin ingin menghapus film ID {film_id}?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            db.soft_delete_film(film_id)
            QMessageBox.information(self, 'Sukses', 'Film berhasil di-nonaktifkan.')
            self.refresh_ui()

    def update_button_labels(self): #<-- Fungsi untuk memperbarui label tombol update/add film
        for i in range(1, 11):
            button = getattr(self.ui, f'update{i}', None)
            if button:
                status = db.get_film_status(i) #<-- Mengambil status film berdasarkan ID
                if status == "active":
                    button.setText("Update")
                elif status == "inactive":
                    button.setText("Add")
    
    def handle_update_film(self, film_id): #<-- Fungsi untuk menangani update film berdasarkan ID
        self.update_detail_window = update_detail_window(film_id, self.user_id)
        self.update_detail_window.show()
        self.close()
    
    def refresh(self):
        self.login_window = update_film_window(self.user_id)
        self.login_window.show()
        self.close()

    def open_admin(self):
        self.admin_window = AdminWindow(self.user_id)
        self.admin_window.show()
        self.close()

# ====================================== HALAMAN UPDATE DETAIL FILM (ADMIN) ====================================== #
class update_detail_window(QMainWindow):
    def __init__(self, film_id, user_id):
        super().__init__()
        self.film_id = film_id #<-- Menyimpan ID film
        self.user_id = user_id #<-- Menyimpan user_id
        self.ui = Ui_UpdateDetail()
        self.ui.setupUi(self)
        self.ui.tombol_kembali.clicked.connect(self.open_update_film)
        self.ui.tombol_save.clicked.connect(self.handle_save)
        self.ui.import_poster.clicked.connect(self.upload_image)
        self.ui.update_tanggal.clicked.connect(self.handle_update_tanggal)
        self.ui.update_waktu.clicked.connect(self.handle_update_jam)
        self.selected_tanggal = None  #<-- Untuk menyimpan tanggal
        self.selected_jam = None #<-- Untuk menyimpan jam
        self.selected_jam_index = None #<-- Untuk menyimpan index jam
        self.setup_jam_selection()
        self.setup_tanggal_selection()
        self.load_film_data()
        
        self.ui.jam_1.clicked.connect(lambda: self.handle_update_jam(0))   #<-- Menghubungkan tombol jam dengan fungsi handle_update_jam sesuai dengan index jam
        self.ui.jam_2.clicked.connect(lambda: self.handle_update_jam(1))
        self.ui.jam_3.clicked.connect(lambda: self.handle_update_jam(2))
        self.ui.jam_4.clicked.connect(lambda: self.handle_update_jam(3))
        self.ui.jam_5.clicked.connect(lambda: self.handle_update_jam(4))
        self.ui.jam_6.clicked.connect(lambda: self.handle_update_jam(5))
        
    def load_film_data(self): #<-- Fungsi untuk memuat data film berdasarkan ID
        film_data = db.get_film_by_id(self.film_id) #<-- Mengambil data film dari database berdasarkan ID film
        if film_data:
            nama, sutradara, aktor, sinopsis, poster_blob, produksi, age = film_data
            self.ui.isi_judulfilm.setText(nama)
            self.ui.edit_sutradara.setText(sutradara)
            self.ui.edit_aktor.setText(aktor)
            self.ui.edit_sinopsis.setText(sinopsis)
            self.ui.edit_produksi.setText(produksi)
            self.ui.edit_age.setText(age)
            
            if poster_blob:
                pixmap = QPixmap()
                pixmap.loadFromData(poster_blob)
                self.set_rounded_pixmap(self.ui.isi_posterfilm, pixmap)
        
        jadwal = db.get_detail_film(self.film_id) #<-- Mengambil jadwal film dari database berdasarkan ID film
        self.jadwal_all = jadwal #<-- Menyimpan semua jadwal film

        self.tanggal_unik = sorted(set([tgl for tgl, _ in jadwal]))
        tanggal_labels = [ #<-- dan menampilkan tanggal pada label
            self.ui.tanggal_1, self.ui.tanggal_2, self.ui.tanggal_3,
            self.ui.tanggal_4, self.ui.tanggal_5
        ]
        self.tanggal_label_map = {}  #<-- Untuk menyimpan mapping antara label dan tanggal
        for i, tgl in enumerate(self.tanggal_unik[:5]):
            label = tanggal_labels[i] #<-- Mengambil label tanggal berdasarkan index
            if tgl:
                label.setText(tgl.strftime("%d-%m-%Y"))
                self.tanggal_label_map[label] = tgl
            else:
                label.setText("-")
        if self.tanggal_unik:
            self.tampilkan_jam_untuk_tanggal(self.tanggal_unik[0])
        
        self.selected_jam = None #<-- Untuk menyimpan jam
    
    def select_tanggal_label(self, label): #<-- Fungsi untuk memilih tanggal berdasarkan label yang diklik
        if label in self.tanggal_label_map:
            self.selected_tanggal = self.tanggal_label_map[label]
            tanggal_str = self.selected_tanggal.strftime("%Y-%m-%d")
            print(f"Tanggal dipilih: {tanggal_str}")
            self.ui.label_tanggaltayang.setText(f"Tanggal dipilih: {tanggal_str}") 
            self.tampilkan_jam_untuk_tanggal(self.selected_tanggal)
        
    def select_tanggal(self, index): #<-- Fungsi untuk memilih tanggal berdasarkan index
        if index < len(self.tanggal_unik): 
            self.selected_tanggal = self.tanggal_unik[index] 
            self.tampilkan_jam_untuk_tanggal(self.selected_tanggal)
    
    def setup_jam_selection(self): #<-- Fungsi untuk mengatur pemilihan jam
        self.ui.jam_1.mousePressEvent = lambda e, i=0: self.select_jam(i) 
        self.ui.jam_2.mousePressEvent = lambda e, i=1: self.select_jam(i)
        self.ui.jam_3.mousePressEvent = lambda e, i=2: self.select_jam(i)
        self.ui.jam_4.mousePressEvent = lambda e, i=3: self.select_jam(i)
        self.ui.jam_5.mousePressEvent = lambda e, i=4: self.select_jam(i)
        self.ui.jam_6.mousePressEvent = lambda e, i=5: self.select_jam(i)
 
    def setup_tanggal_selection(self): #<-- Fungsi untuk mengatur pemilihan tanggal
        self.ui.tanggal_1.mousePressEvent = lambda e: self.select_tanggal_label(self.ui.tanggal_1)
        self.ui.tanggal_2.mousePressEvent = lambda e: self.select_tanggal_label(self.ui.tanggal_2)
        self.ui.tanggal_3.mousePressEvent = lambda e: self.select_tanggal_label(self.ui.tanggal_3)
        self.ui.tanggal_4.mousePressEvent = lambda e: self.select_tanggal_label(self.ui.tanggal_4)
        self.ui.tanggal_5.mousePressEvent = lambda e: self.select_tanggal_label(self.ui.tanggal_5)

    def select_jam(self, index): #<-- Fungsi untuk memilih jam berdasarkan index
        if self.selected_tanggal:
            jam_list = [jam for tgl, jam in self.jadwal_all if tgl == self.selected_tanggal]
            if index < len(jam_list):
                self.selected_jam = jam_list[index]
                self.selected_jam_index = index
                jam_str = self.format_jam(self.selected_jam)
                print(f"Jam dipilih (jam_{index+1}): {jam_str}") 
                self.ui.label_waktutayang.setText(f"Jam dipilih: {jam_str}")
   
    def format_jam(self, jam): #<-- Fungsi untuk memformat jam menjadi string
        if isinstance(jam, timedelta):
            total_seconds = jam.total_seconds()
            h = int(total_seconds // 3600)
            m = int((total_seconds % 3600) // 60)
            return f"{h:02d}:{m:02d}"
        else:
            return jam.strftime("%H:%M")
    
    def tampilkan_jam_untuk_tanggal(self, tanggal_obj): #<-- Fungsi untuk menampilkan jam untuk tanggal yang dipilih
        jam_labels = [
            self.ui.jam_1, self.ui.jam_2, self.ui.jam_3,
            self.ui.jam_4, self.ui.jam_5, self.ui.jam_6
        ]
        jam_list = [jam for tgl, jam in self.jadwal_all if tgl == tanggal_obj]

        for i in range(len(jam_labels)): #<-- Mengatur setiap label jam dengan jam yang sesuai
            if i < len(jam_list):
                jam = jam_list[i]
                if isinstance(jam, timedelta):
                    total_seconds = jam.total_seconds()
                    h = int(total_seconds // 3600)
                    m = int((total_seconds % 3600) // 60)
                    jam_labels[i].setText(f"{h:02d}:{m:02d}")
                else:
                    jam_labels[i].setText(jam.strftime("%H:%M")) 
            else:
                jam_labels[i].setText("-")

    def handle_update_tanggal(self): #<-- Fungsi untuk menangani update tanggal
        if not self.selected_tanggal:
            QMessageBox.warning(self, "Peringatan", "Silakan pilih tanggal terlebih dahulu.")
            return

        new_date, ok = QInputDialog.getText(self, "Update Tanggal", "Masukkan tanggal baru (YYYY-MM-DD):")
        if ok and new_date:
            tanggal_lama = self.selected_tanggal.strftime("%Y-%m-%d")
            db.update_tanggal_film(self.film_id, tanggal_lama, new_date)
            QMessageBox.information(self, "Sukses", f"Semua jam untuk tanggal {tanggal_lama} berhasil diubah menjadi {new_date}")
            self.load_film_data()
    
    def format_jam_full(self, jam): #<-- Fungsi untuk memformat jam menjadi string dengan format HH:MM:SS
        if isinstance(jam, timedelta):
            total_seconds = jam.total_seconds()
            h = int(total_seconds // 3600)
            m = int((total_seconds % 3600) // 60)
            return f"{h:02d}:{m:02d}:00"
        else:
            return jam.strftime("%H:%M:%S")
    
    def handle_update_jam(self): #<-- Fungsi untuk menangani update jam
        if self.selected_tanggal is None or self.selected_jam_index is None:
            QMessageBox.warning(self, "Peringatan", "Silakan klik tanggal dan jam terlebih dahulu.")
            return

        jam_input, ok = QInputDialog.getText( #<-- Mengambil input jam baru dari user
            self,
            "Update Jam",
            f"Masukkan jam baru untuk jam_{self.selected_jam_index + 1} (HH:MM):"
        )
        if not ok or not jam_input:
            return

        tanggal_str = self.selected_tanggal.strftime("%Y-%m-%d") #<-- Mengubah tanggal yang dipilih menjadi string sesuai format
        jam_list = [jam for tgl, jam in self.jadwal_all if tgl == self.selected_tanggal]
        if self.selected_jam_index >= len(jam_list):
            QMessageBox.warning(self, "Error", "Index jam tidak valid.")
            return

        jam_lama = jam_list[self.selected_jam_index]
        jam_lama_str = self.format_jam_full(jam_lama)
        jam_baru_str = jam_input.strip() + ":00"

        db.update_jam_film(self.film_id, tanggal_str, jam_lama_str, jam_baru_str) #<-- Mengupdate jam film di database
        QMessageBox.information(self, "Sukses", f"Jam ke-{self.selected_jam_index + 1} berhasil diubah.") 
        self.load_film_data()
          
    def set_rounded_pixmap(self, label, pixmap): #<-- Fungsi untuk mengatur pixmap gambar agar sesuai dengan label
        size = label.size()
        rounded_pixmap = QPixmap(size)
        rounded_pixmap.fill(Qt.transparent)
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        rect = QRectF(0, 0, size.width(), size.height())
        tl = 0
        tr = 20
        br = 0
        bl = 35  
        #<-- Mengatur path untuk rounded corners
        path.moveTo(rect.left() + tl, rect.top())
        path.lineTo(rect.right() - tr, rect.top())
        path.quadTo(rect.right(), rect.top(), rect.right(), rect.top() + tr)
        path.lineTo(rect.right(), rect.bottom() - br)
        path.quadTo(rect.right(), rect.bottom(), rect.right() - br, rect.bottom())
        path.lineTo(rect.left() + bl, rect.bottom())
        path.quadTo(rect.left(), rect.bottom(), rect.left(), rect.bottom() - bl)
        path.lineTo(rect.left(), rect.top() + tl)
        path.quadTo(rect.left(), rect.top(), rect.left() + tl, rect.top())
        #<-- Mengatur clip path untuk menggambar rounded corners
        painter.setClipPath(path)
        #<-- Mengatur ukuran pixmap agar sesuai dengan label
        scaled = pixmap.scaled(size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        x = (size.width() - scaled.width()) // 2
        y = (size.height() - scaled.height()) // 2
        painter.drawPixmap(x, y, scaled)
        painter.end()

        label.setPixmap(rounded_pixmap)
        label.setAlignment(Qt.AlignCenter)

    def upload_image(self): #<-- Fungsi untuk mengupload gambar poster film
        options = QFileDialog.Options()
        poster, _ = QFileDialog.getOpenFileName(self, "Pilih Gambar", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        if poster:
            pixmap = QPixmap(poster) 
            self.set_rounded_pixmap(self.ui.isi_posterfilm, pixmap)

        nama_film, ok = QInputDialog.getText(self, "Tambah Film", "Masukkan judul film:")
        if ok and nama_film:
            self.ui.isi_judulfilm.setText(nama_film)
        
    def handle_save(self): #<-- Fungsi untuk menyimpan data film yang telah diupdate
        nama_film = self.ui.isi_judulfilm.text()
        sutradara = self.ui.edit_sutradara.text()
        produksi = self.ui.edit_produksi.text()
        aktor = self.ui.edit_aktor.text() 
        age = self.ui.edit_age.text()
        sinopsis = self.ui.edit_sinopsis.toPlainText()

        if not nama_film or not sutradara or not aktor or not age or not sinopsis or not produksi:
            QMessageBox.warning(self, 'Peringatan', 'Isi semua kolom!')
            return
        pixmap = self.ui.isi_posterfilm.pixmap()
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QBuffer.WriteOnly)
        pixmap.save(buffer, "PNG")
        poster_blob = byte_array.data()
        
        db.update_film(self.film_id, nama_film, sutradara, aktor, sinopsis, produksi, age, poster_blob) #<-- Mengupdate data film di database
        db.reactivate_film(self.film_id) #<-- Mengaktifkan kembali film yang telah diupdate
        QMessageBox.information(self, 'Sukses', 'Data film berhasil diperbarui!')
        
    def open_update_film(self):
        self.update_film_window = update_film_window(self.user_id)
        self.update_film_window.show()
        self.close()

# ======================================== HALAMAN PILIH FILM ========================================= #
class PilihFilmWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id 
        self.ui = Ui_PilihFilm()
        self.ui.setupUi(self)
        self.ui.label_home.clicked.connect(self.open_home)
        self.ui.isi_judul1.clicked.connect(lambda: self.handle_pesan_film(1)) #<-- Menghubungkan klik pada label judul film dengan fungsi handle_pesan_film sesuai dengan ID film
        self.ui.isi_judul2.clicked.connect(lambda: self.handle_pesan_film(2))
        self.ui.isi_judul3.clicked.connect(lambda: self.handle_pesan_film(3))
        self.ui.isi_judul4.clicked.connect(lambda: self.handle_pesan_film(4))
        self.ui.isi_judul5.clicked.connect(lambda: self.handle_pesan_film(5))
        nama = db.get_nama_user_by_id(self.user_id)
        if nama:
            self.ui.label_user.setText(str(nama))
            
        self.load_all_posters()

    def set_rounded_pixmap(self, label, pixmap): #<-- Fungsi untuk mengatur pixmap gambar agar sesuai dengan label
        size = label.size()
        rounded_pixmap = QPixmap(size)
        rounded_pixmap.fill(Qt.transparent)
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        rect = QRectF(0, 0, size.width(), size.height())
        tl = 0
        tr = 20
        br = 0
        bl = 35  

        path.moveTo(rect.left() + tl, rect.top())
        path.lineTo(rect.right() - tr, rect.top())
        path.quadTo(rect.right(), rect.top(), rect.right(), rect.top() + tr)
        path.lineTo(rect.right(), rect.bottom() - br)
        path.quadTo(rect.right(), rect.bottom(), rect.right() - br, rect.bottom())
        path.lineTo(rect.left() + bl, rect.bottom())
        path.quadTo(rect.left(), rect.bottom(), rect.left(), rect.bottom() - bl)
        path.lineTo(rect.left(), rect.top() + tl)
        path.quadTo(rect.left(), rect.top(), rect.left() + tl, rect.top())

        painter.setClipPath(path)
        
        scaled = pixmap.scaled(size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        x = (size.width() - scaled.width()) // 2
        y = (size.height() - scaled.height()) // 2
        painter.drawPixmap(x, y, scaled)
        painter.end()

        label.setPixmap(rounded_pixmap)
        label.setAlignment(Qt.AlignCenter)

    def load_all_posters(self): #<-- Fungsi untuk memuat semua poster film dari database
        all_films = db.get_all_active_films(limit=10)
        for i, film in enumerate(all_films):
            id_film, poster_blob, nama_film = film

            label_poster = getattr(self.ui, f'isi_poster{i+1}', None)
            label_judul = getattr(self.ui, f'isi_judul{i+1}', None)

            if label_poster and poster_blob:
                pixmap = QPixmap()
                pixmap.loadFromData(poster_blob)
                self.set_rounded_pixmap(label_poster, pixmap)
            else:
                label_poster.setText("No image")

            if label_judul:
                label_judul.setText(nama_film)

    def handle_pesan_film(self, id_film): #<-- Fungsi untuk menangani pemesanan film berdasarkan ID
        self.detail_window = DetailFilmWindow(self.user_id, id_film)
        self.detail_window.show()
        self.close()

    def open_home(self): #<-- Fungsi untuk membuka tampilan home
        role = db.get_role_by_user_id(self.user_id)
        if role == 'admin':
            self.admin_home = AdminWindow(self.user_id)
            self.admin_home.show()
        else:
            self.user_home = UserWindow(self.user_id)
            self.user_home.show()
        self.close()

# ======================================== HALAMAN DETAIL FILM ========================================= #
class DetailFilmWindow(QMainWindow):
    def __init__(self, user_id, id_film):
        super().__init__()
        self.user_id = user_id #<-- Menyimpan user_id
        self.id_film = id_film #<-- Menyimpan ID film
        self.ui = Ui_Detail()
        self.ui.setupUi(self)
        self.ui.label_home.clicked.connect(self.open_pilih_film)
        nama = db.get_nama_user_by_id(self.user_id)
        if nama:
            self.ui.label_username.setText(str(nama))
            
        self.selected_tanggal = None #<-- Untuk menyimpan tanggal yang dipilih
        self.jadwal_all = [] #<-- Untuk menyimpan semua jadwal film
        self.setup_jam_selection()
        self.load_film_details()
        self.load_film_details()
        self.load_jadwal_film()
    
    def load_jadwal_film(self): #<-- Fungsi untuk memuat jadwal film berdasarkan ID
        jadwal = db.get_detail_film(self.id_film)
        self.jadwal_all = jadwal

        self.tanggal_unik = sorted(set([tgl for tgl, _ in jadwal]))
        tanggal_labels = [
            self.ui.tanggal_1, self.ui.tanggal_2, self.ui.tanggal_3,
            self.ui.tanggal_4, self.ui.tanggal_5
        ]
        self.tanggal_label_map = {}

        for i, tgl in enumerate(self.tanggal_unik[:5]): 
            label = tanggal_labels[i] #<-- Mengambil label tanggal berdasarkan index
            if tgl:
                label.setText(tgl.strftime("%d-%m-%Y"))
                self.tanggal_label_map[label] = tgl
                label.mousePressEvent = lambda event, l=label: self.select_tanggal_label(l)
            else:
                label.setText("-")
        
        if self.tanggal_unik:
            self.selected_tanggal = self.tanggal_unik[0]
            self.tampilkan_jam_untuk_tanggal(self.selected_tanggal) 
            
    def setup_jam_selection(self): #<-- Fungsi untuk mengatur pemilihan jam
        jam_labels = [
            self.ui.jam_1, self.ui.jam_2, self.ui.jam_3,
            self.ui.jam_4, self.ui.jam_5, self.ui.jam_6
        ]

        for label in jam_labels:
            label.mousePressEvent = lambda event, l=label: self.handle_jam_pilih(l)

    def tampilkan_jam_untuk_tanggal(self, tanggal): #<-- Fungsi untuk menampilkan jam untuk tanggal yang dipilih
        jam_labels = [
            self.ui.jam_1, self.ui.jam_2, self.ui.jam_3,
            self.ui.jam_4, self.ui.jam_5, self.ui.jam_6
        ]

        for label in jam_labels:
            label.setText("")

        jam_list = [jam for tgl, jam in self.jadwal_all if tgl == tanggal]

        for i, jam in enumerate(jam_list[:6]):
            if isinstance(jam, timedelta):
                hours = int(jam.total_seconds() // 3600)
                minutes = int((jam.total_seconds() % 3600) // 60)
                jam_str = f"{hours:02d}:{minutes:02d}"
            else:
                jam_str = jam.strftime("%H:%M")
            jam_labels[i].setText(jam_str)

    def select_tanggal_label(self, label): #<-- Fungsi untuk memilih tanggal berdasarkan label yang diklik
        self.selected_tanggal = self.tanggal_label_map.get(label)
        if self.selected_tanggal:
            print(f"[LOG] Tanggal dipilih: {self.selected_tanggal.strftime('%Y-%m-%d')}")
            self.tampilkan_jam_untuk_tanggal(self.selected_tanggal)
        
    def handle_jam_pilih(self, label): #<-- Fungsi untuk menangani pemilihan jam ketika label jam diklik
        jam_text = label.text()
        if not jam_text or not self.selected_tanggal:
            return
        print(f"[LOG] Jam dipilih: {jam_text}")
        jam_obj = jam_text + ":00"  
        tanggal_str = self.selected_tanggal.strftime("%Y-%m-%d")
        detail_id = db.get_detail_film_id(self.id_film, tanggal_str, jam_obj) #<-- Mengambil ID detail film
        if detail_id:
            self.open_seats(detail_id)
    
    def format_jam(self, jam):
        if isinstance(jam, timedelta):
            total_seconds = jam.total_seconds()
            h = int(total_seconds // 3600)
            m = int((total_seconds % 3600) // 60)
            return f"{h:02d}:{m:02d}"
        return str(jam)

    def load_film_details(self): #<-- Fungsi untuk memuat detail film berdasarkan ID
        film_data = db.get_film_by_id(self.id_film)
        if film_data:
            nama, sutradara, aktor, sinopsis, poster_blob, produksi, age = film_data
            self.ui.isi_judulfilm.setText(nama)
            self.ui.isi_sutradara.setText(sutradara)
            self.ui.isi_aktor.setText(aktor)
            self.ui.isi_sinopsis.setWordWrap(True)
            self.ui.isi_sinopsis.setText(sinopsis)
            self.ui.isi_sinopsis.adjustSize()
            self.ui.isi_produksi.setText(produksi)
            self.ui.isi_age.setText(age)

            if poster_blob:
                pixmap = QPixmap()
                pixmap.loadFromData(poster_blob)
                scaled = pixmap.scaled(self.ui.isi_posterfilm.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                self.ui.isi_posterfilm.setPixmap(scaled)

    def open_seats(self, id_detail_film): #<-- Fungsi untuk membuka tampilan SeatsWindow
        self.seats_window = SeatsWindow(self.user_id, id_detail_film)
        self.seats_window.show()
        self.close()

    def open_pilih_film(self): #<-- Fungsi untuk membuka tampilan PilihFilmWindow
        self.pilih_film_window = PilihFilmWindow(self.user_id)
        self.pilih_film_window.show()
        self.close()

# ======================================== HALAMAN PILIH KURSI/SEATS ========================================= #
class SeatsWindow(QMainWindow):
    def __init__(self, user_id, id_detail_film): #<-- Inisialisasi user_id dan id_detail_film
        super().__init__()
        self.user_id = user_id
        self.id_detail_film = id_detail_film
        self.ui = Ui_Seats()
        self.ui.setupUi(self)
        self.ui.tombol_lanjut.clicked.connect(self.handle_lanjut_pesan)
        self.ui.tombol_kembali.clicked.connect(self.open_pilih_film)
        
        nama = db.get_nama_user_by_id(self.user_id)
        if nama:
            self.ui.label_user.setText(str(nama))
        
        self.load_seats()

    def load_seats(self): #<-- Fungsi untuk memuat kursi yang tersedia dan terisi
        self.kursi_buttons = {}
        self.kursi_terisi = set()
        self.kursi_dipilih = set()

        semua_kursi = db.get_all_kursi()
        terisi = db.get_kursi_terisi(self.id_detail_film) #<-- Mengambil kursi yang terisi berdasarkan ID detail film
        self.kursi_terisi = set(terisi)

        for id_kursi, nama_kursi, tipe in semua_kursi:
            button = getattr(self.ui, f"{nama_kursi}", None)
            if button:
                self.kursi_buttons[nama_kursi] = (button, id_kursi, tipe) #<-- Menyimpan button, ID kursi, dan tipe kursi dalam dictionary
                if id_kursi in self.kursi_terisi:
                    button.setStyleSheet("background-color: #7d5a2e;")
                    button.setEnabled(False)
                else:
                    button.setStyleSheet("background-color: #ffc107;")
                    button.clicked.connect(lambda _, n=nama_kursi: self.toggle_kursi(n)) 

        self.update_display() #<-- Memperbarui tampilan kursi yang dipilih dan subtotal
    
    def toggle_kursi(self, nama_kursi): #<-- Fungsi untuk toggle kursi yang dipilih
        if nama_kursi in self.kursi_dipilih:
            self.kursi_dipilih.remove(nama_kursi)
            self.kursi_buttons[nama_kursi][0].setStyleSheet("background-color: #ffc107;")
        else: 
            self.kursi_dipilih.add(nama_kursi)
            self.kursi_buttons[nama_kursi][0].setStyleSheet("background-color: #4caf50;")

        self.update_display()
    
    def update_display(self):
        self.ui.isi_kursidipilih.setText(", ".join(sorted(self.kursi_dipilih)))

        harga_base = db.get_harga_by_detail_id(self.id_detail_film)
        total = 0 #<-- Inisialisasi total harga
        for nama in self.kursi_dipilih:
            _, _, tipe = self.kursi_buttons[nama]
            total += harga_base * (2 if tipe == "double" else 1) #<-- Menghitung total harga berdasarkan tipe kursi
        self.ui.isi_subtotal.setText(f"Rp {total:,}".replace(",", "."))
        self.total_harga = total #<-- Menyimpan total harga
    
    def handle_lanjut_pesan(self): #<-- Fungsi untuk menangani lanjut ke pembayaran
        if not self.kursi_dipilih:
            QMessageBox.warning(self, "Pilih Kursi", "Silakan pilih minimal satu kursi terlebih dahulu.")
            return
 
        msg = QMessageBox.question(
            self, "Konfirmasi",
            f"Anda memilih kursi: {', '.join(sorted(self.kursi_dipilih))}\nLanjut ke pembayaran?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if msg != QMessageBox.Yes: 
            return

        kursi_terpilih = sorted(self.kursi_dipilih)  #<-- Mengurutkan kursi yang dipilih
        self.payment_window = PaymentWindow(self.user_id, self.id_detail_film, kursi_terpilih)
        self.payment_window.show()
        self.close()

    def open_pilih_film(self):
        self.pilih_film_window = PilihFilmWindow(self.user_id)
        self.pilih_film_window.show()
        self.close()

# ======================================== HALAMAN PAYMENT ========================================= #
class PaymentWindow(QMainWindow):
    def __init__(self, user_id, id_detail_film, kursi_dipilih):
        super().__init__()
        self.user_id = user_id #<-- Menyimpan user_id 
        self.id_detail_film = id_detail_film #<-- Menyimpan ID detail film 
        self.kursi_dipilih = kursi_dipilih #<-- Menyimpan kursi yang dipilih 
        self.ui = Ui_Payment()
        self.ui.setupUi(self)
        self.ui.tombol_lanjut.clicked.connect(self.handle_lanjut) 
        self.ui.tombol_lanjut.setEnabled(False) #<-- Menonaktifkan tombol lanjut sampai syarat disetujui
        self.ui.checkBox.stateChanged.connect(self.check_syarat)
        self.ui.checkBox_2.stateChanged.connect(self.check_syarat)
        nama = db.get_nama_user_by_id(self.user_id)
        if nama:
            self.ui.user_name.setText(str(nama))
        self.setup_payment_ui()
        
    def setup_payment_ui(self): #<-- Fungsi untuk mengatur tampilan pembayaran
        film = db.get_film_by_detail_id(self.id_detail_film)
        harga_satuan = db.get_harga_by_detail_id(self.id_detail_film)
        nama_user = db.get_nama_user_by_id(self.user_id)

        self.ui.isi_namafilm.setText(film)
        self.ui.isi_kursidipilih.setText(", ".join(self.kursi_dipilih))
        self.ui.isi_namauser.setText(str(nama_user))

        jumlah_kursi = len(self.kursi_dipilih) #<-- Menghitung jumlah kursi yang dipilih
        harga_total = 0
        for nama_kursi in self.kursi_dipilih:
            tipe = db.get_tipe_kursi(nama_kursi) #<-- Mengambil tipe kursi berdasarkan nama kursi
            harga_total += harga_satuan * (2 if tipe == "double" else 1)

        fee = int(harga_total * 0.05) #<-- Menghitung fee 5% dari total harga
        total = harga_total + fee #<-- Menghitung total pembayaran

        self.ui.isi_harga.setText(f"Rp {harga_total:,}".replace(",", "."))
        self.ui.isi_fee.setText(f"Rp {fee:,}".replace(",", "."))
        self.ui.isi_totalharga.setText(f"Rp {total:,}".replace(",", "."))

        self.harga_total = harga_total
        self.fee = fee
        self.total_bayar = total

        bank = self.ui.comboBox_payment.currentText().strip() #<-- Mengambil bank yang dipilih dari combobox
        self.ui.comboBox_payment.currentTextChanged.connect(self.update_va)
        self.update_va(bank)
        self.nama_user = nama_user  
        self.nama_film = film 
    
    def update_va(self, bank_nama): #<-- Fungsi untuk memperbarui Virtual Account (VA) berdasarkan bank yang dipilih
        prefix = {
            "BCA": "014",
            "Mandiri": "008",
            "BRI": "002",
            "DANA": "999"
        }
        bank_code = prefix.get(bank_nama.strip(), "000") #<-- Mengambil kode bank
        va = f"{bank_code}{self.user_id:04d}{self.id_detail_film:04d}" #<-- Membuat Virtual Account (VA) berdasarkan kode bank, user_id, dan id_detail_film
        self.ui.isi_VA.setText(va)

    def handle_lanjut(self): #<-- Fungsi untuk menangani lanjut ke pembayaran
        if not self.ui.checkBox.isChecked() or not self.ui.checkBox_2.isChecked():
            QMessageBox.warning(self, "Syarat", "Harap setujui semua syarat terlebih dahulu.")
            return

        va = self.ui.isi_VA.text()
        bank = self.ui.comboBox_payment.currentText().strip()

        for nama_kursi in self.kursi_dipilih:
            id_kursi = db.get_id_kursi_by_name(nama_kursi)
            db.insert_pemesanan( #<-- Menyimpan pemesanan kursi ke database
                self.user_id, self.id_detail_film, id_kursi,
                harga=self.harga_total,
                bank=bank, va=va
            )
        
        qr_data = f"{self.nama_film} | Kursi: {', '.join(self.kursi_dipilih)} | VA: {va}" #<-- Membuat data untuk QR Code
        db.insert_histori_bill( #<-- Menyimpan histori pembayaran ke database
            id_akun=self.user_id, 
            id_detail_film=self.id_detail_film,
            kursi_list=self.kursi_dipilih,
            total=self.total_bayar,
            metode=f"{bank} - VA: {va}",
            qr_text=qr_data
        )

        QMessageBox.information(self, "Berhasil", "Pembayaran berhasil! Silakan cek histori.")
        self.open_history(self.nama_user, self.nama_film, self.kursi_dipilih, self.total_bayar, va)

    def check_syarat(self): #<-- Fungsi untuk memeriksa apakah syarat sudah disetujui
        ready = self.ui.checkBox.isChecked() and self.ui.checkBox_2.isChecked()
        self.ui.tombol_lanjut.setEnabled(ready)

    def open_history(self, nama_user, nama_film, kursi_list, total_bayar, va): #<-- Penyimpanan pada open halaman Historybill
        self.history_window = HistoryBillWindow(
            user_id=self.user_id, 
            id_detail_film=self.id_detail_film,
            nama_user=nama_user,
            nama_film=nama_film,
            kursi_list=kursi_list,
            total=total_bayar,
            va=va
        )
        self.history_window.show()
        self.close() 

# ======================================== HALAMAN HISTORY BILL ========================================= #
class HistoryBillWindow(QMainWindow):
    def __init__(self, user_id, id_detail_film, nama_user, nama_film, kursi_list, total, va):
        super().__init__()
        self.ui = Ui_HistoryBill() 
        self.user_id = user_id #<-- Menyimpan user_id
        self.id_detail_film = id_detail_film #<-- Menyimpan ID detail film
        self.nama_user = nama_user #<-- Menyimpan nama user
        self.nama_film = nama_film
        self.kursi_list = kursi_list
        self.total = total
        self.va = va
        self.ui.setupUi(self)
        self.ui.tombol_kembali.clicked.connect(self.go_home)
        nama = db.get_nama_user_by_id(self.user_id)
        if nama:
            self.ui.label_username.setText(str(nama))
        self.set_detail_transaksi()

    def set_detail_transaksi(self): #<-- Fungsi untuk mengatur detail transaksi pada tampilan HistoryBill
        tanggal, jam = db.get_detail_film_jadwal(self.id_detail_film)
        studio = "1"
        nomor_pemesanan = f"{self.user_id:03d}{self.id_detail_film:03d}{datetime.now().strftime('%H%M%S')}"
        self.ui.label_tanggaltransaksi.setText(datetime.now().strftime("%d-%m-%Y"))
        self.ui.isi_nomorpesan.setText(nomor_pemesanan)
        self.ui.isi_nomorVA.setText(self.va)
        self.ui.isi_filmdipilih.setText(self.nama_film)
        self.ui.isi_kursidipilih.setText(", ".join(self.kursi_list))
        
        if isinstance(jam, timedelta):
            total_seconds = jam.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            jam_str = f"{hours:02d}:{minutes:02d}"
        else:
            jam_str = jam.strftime("%H:%M")
        self.ui.isi_timefilm.setText(jam_str)
        self.ui.isi_totalpayment.setText(f"Rp {self.total:,}".replace(",", "."))
        self.ui.isi_nomorstudio.setText(studio)
        
        if isinstance(jam, timedelta):
            total_seconds = jam.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            jam_str = f"{hours:02d}:{minutes:02d}"
            
        else:
            jam_str = jam.strftime("%H:%M")
        qr_data = f"{self.nama_film} | {tanggal} {jam_str} | Kursi: {', '.join(self.kursi_list)} | VA: {self.va}"
        self.generate_qrcode(qr_data)

    def generate_qrcode(self, text): #<-- Fungsi untuk menghasilkan QR Code dari data transaksi
        qr = qrcode.make(text)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        qimg = QImage.fromData(buffer.getvalue())
        pixmap = QPixmap.fromImage(qimg)
        self.ui.isi_qrcode.setPixmap(pixmap.scaled(
            self.ui.isi_qrcode.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))

    def go_home(self): #<-- Fungsi untuk kembali ke tampilan home
        role = db.get_role_by_user_id(self.user_id) #<-- Mengambil role user
        if role == 'admin':
            self.admin_home = AdminWindow(self.user_id)
            self.admin_home.show()
        else:
            self.user_home = UserWindow(self.user_id)
            self.user_home.show()
        self.close()

# ======================================== HALAMAN HISTORY ========================================= #
class HistoryWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.ui = Ui_History()
        self.ui.setupUi(self)
        self.ui.tabel_laporan.horizontalHeader().setStretchLastSection(True)
        self.ui.tabel_laporan.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.load_histori()
        self.ui.tombol_kembali.clicked.connect(self.go_home)
        self.ui.tabel_laporan.doubleClicked.connect(self.buka_detail_histori)
        self.ui.edit_carilaporan.textChanged.connect(self.filter_histori)
        nama = db.get_nama_user_by_id(self.user_id)
        if nama:
            self.ui.label_admin.setText(str(nama))

    def load_histori(self): #<-- Fungsi untuk memuat histori pemesanan berdasarkan user_id
        data = db.get_histori_by_user(self.user_id)
        self.histori_data = data
        self.update_table_with_data(data)

    def update_table_with_data(self, data): #<-- Fungsi untuk memperbarui tabel dengan data histori
        model = QStandardItemModel(len(data), 6)
        model.setHorizontalHeaderLabels(["No", "Film", "Kursi", "Total", "Metode", "Waktu"])

        for row, (id_detail, kursi, total, metode, waktu) in enumerate(data):
            nama_film = db.get_film_by_detail_id(id_detail)
            def item(text):
                i = QStandardItem(text)
                i.setForeground(Qt.black)
                return i 
            model.setItem(row, 0, item(str(row + 1))) 
            model.setItem(row, 1, item(nama_film))
            model.setItem(row, 2, item(kursi))
            model.setItem(row, 3, item(f"Rp {total:,}".replace(",", ".")))
            model.setItem(row, 4, item(metode))
            model.setItem(row, 5, item(str(waktu)))
        self.ui.tabel_laporan.setModel(model)
        self.ui.tabel_laporan.resizeColumnsToContents()

    def buka_detail_histori(self, index): #<-- Fungsi untuk membuka detail histori ketika baris tabel diklik
        row = index.row()
        id_detail_film, kursi, total, metode, _ = self.histori_data[row]
        nama_film = db.get_film_by_detail_id(id_detail_film)
        va = metode.split(" - VA: ")[-1] if "VA" in metode else metode

        kursi_list = [k.strip() for k in kursi.split(",")] #<-- Mengubah kursi menjadi list
        self.detail = HistoryBillWindow(
            user_id=self.user_id,
            id_detail_film=id_detail_film,
            nama_user=db.get_nama_user_by_id(self.user_id),
            nama_film=nama_film,
            kursi_list=kursi_list,
            total=total,
            va=va
        )
        self.detail.show()

    def filter_histori(self, text): #<-- Fungsi untuk memfilter histori berdasarkan input teks
        text = text.lower()
        filtered = []
        for row in self.histori_data:
            id_detail, kursi, total, metode, waktu = row
            nama_film = db.get_film_by_detail_id(id_detail)
            if (text in nama_film.lower() or
                text in kursi.lower() or
                text in metode.lower()):
                filtered.append(row)
        self.update_table_with_data(filtered)
    
    def go_home(self): #<-- Fungsi untuk kembali ke tampilan home
        self.user_home = UserWindow(self.user_id)
        self.user_home.show()
        self.close()

# ======================================== HALAMAN LAPORAN (ADMIN) ========================================= #
class LaporanWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.ui = Ui_Laporan()
        self.ui.setupUi(self)
        self.ui.tabel_laporan.horizontalHeader().setStretchLastSection(True)
        self.ui.tabel_laporan.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.load_histori()
        self.ui.tabel_laporan.doubleClicked.connect(self.buka_detail_histori)
        self.ui.tombol_kembali.clicked.connect(self.go_home)
        self.ui.edit_carilaporan.textChanged.connect(self.filter_histori)

    def load_histori(self): #<-- Fungsi untuk memuat semua laporan dari database
        data = db.get_semua_laporan()
        self.histori_data = data
        self.update_table_with_data(data)

    def update_table_with_data(self, data): #<-- Fungsi untuk memperbarui tabel dengan data laporan
        baris_data = len(data)
        model = QStandardItemModel(baris_data + 1, 7)
        model.setHorizontalHeaderLabels(["No", "User", "Film", "Kursi", "Total", "Metode", "Waktu"])

        total_semua = 0 #<-- Inisialisasi total semua transaksi

        for row, (id_detail, kursi, total, metode, waktu, username) in enumerate(data): #<-- Iterasi data laporan
            nama_film = db.get_film_by_detail_id(id_detail)
            total_semua += total 

            def item(text):
                i = QStandardItem(str(text))
                i.setForeground(Qt.black)
                return i
            #<-- Mengatur item pada setiap baris tabel
            model.setItem(row, 0, item(str(row + 1)))
            model.setItem(row, 1, item(username))
            model.setItem(row, 2, item(nama_film))
            model.setItem(row, 3, item(kursi))
            model.setItem(row, 4, item(f"Rp {total:,}".replace(",", ".")))
            model.setItem(row, 5, item(metode))
            model.setItem(row, 6, item(str(waktu)))

        def bold_item(text): #<-- Fungsi untuk membuat item dengan teks tebal dan latar belakang berwarna
            i = QStandardItem(str(text))
            font = i.font()
            font.setBold(True)
            i.setFont(font)
            i.setForeground(Qt.black)
            i.setBackground(QColor(255, 255, 180))  
            return i

        model.setItem(baris_data, 0, bold_item("Total :")) #<-- Menambahkan baris total di akhir tabel
        model.setItem(baris_data, 1, bold_item(f"Rp {int(total_semua):,}".replace(",", "."))) 
        model.setItem(baris_data, 2, bold_item(""))
        model.setItem(baris_data, 3, bold_item(""))
        model.setItem(baris_data, 4, bold_item(""))
        model.setItem(baris_data, 5, bold_item("")) 
        model.setItem(baris_data, 6, bold_item("")) 

        self.ui.tabel_laporan.setModel(model)
        self.ui.tabel_laporan.resizeColumnsToContents()

    def buka_detail_histori(self, index): #<-- Fungsi untuk membuka detail laporan ketika baris tabel diklik
        row = index.row()
        id_detail_film, kursi, total, metode, waktu, username = self.histori_data[row]
        nama_film = db.get_film_by_detail_id(id_detail_film)
        va = metode.split(" - VA: ")[-1] if "VA" in metode else metode

        kursi_list = [k.strip() for k in kursi.split(",")]
        self.detail = HistoryBillWindow(
            user_id=self.user_id,
            id_detail_film=id_detail_film,
            nama_user=username,
            nama_film=nama_film,
            kursi_list=kursi_list,
            total=total,
            va=va
        )
        self.detail.show()

    def filter_histori(self, text): #<-- Fungsi untuk memfilter laporan berdasarkan input teks
        text = text.lower()
        filtered = []

        for row in self.histori_data:
            id_detail, kursi, total, metode, waktu, username = row
            nama_film = db.get_film_by_detail_id(id_detail)

            if (text in nama_film.lower() or
                text in kursi.lower() or
                text in metode.lower() or
                text in username.lower()):
                filtered.append(row)
        self.update_table_with_data(filtered) #<-- Memperbarui tabel dengan data
    
    def go_home(self):
        self.admin_home = AdminWindow(self.user_id)
        self.admin_home.show()
        self.close()
            
# ======================================== MAIN PROGRAM ========================================= #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    window.show()
    sys.exit(app.exec_())
