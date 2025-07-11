# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Laporan.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/ico.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("*{\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    background: transparent;\n"
"    padding:0 ;\n"
"    margin:0 ;\n"
"    color: #fff;\n"
"}\n"
"#centralwidget{\n"
"    background-color: ;\n"
"    background-image: url(:/images/1a800x6001.png);\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.navbar = QtWidgets.QFrame(self.centralwidget)
        self.navbar.setMinimumSize(QtCore.QSize(750, 50))
        self.navbar.setMaximumSize(QtCore.QSize(800, 50))
        self.navbar.setStyleSheet("\n"
"QFrame#navbar {\n"
"    background-color: #1e1e2f;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    font-family: \"Segoe UI\";\n"
"    font-size: 9pt;\n"
"    font-weight: bold;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    color:  rgb(220, 165, 50);\n"
"    background-color: rgba(0, 0, 0, 0.05);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    padding-left: 5px;\n"
"    padding-top: 5px;\n"
"}\n"
"")
        self.navbar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.navbar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.navbar.setObjectName("navbar")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.navbar)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.HLayout_3 = QtWidgets.QHBoxLayout()
        self.HLayout_3.setObjectName("HLayout_3")
        self.tombol_kembali = QtWidgets.QPushButton(self.navbar)
        self.tombol_kembali.setMinimumSize(QtCore.QSize(50, 50))
        self.tombol_kembali.setObjectName("tombol_kembali")
        self.HLayout_3.addWidget(self.tombol_kembali)
        self.icon_vline = QtWidgets.QLabel(self.navbar)
        self.icon_vline.setMinimumSize(QtCore.QSize(20, 35))
        self.icon_vline.setMaximumSize(QtCore.QSize(20, 35))
        self.icon_vline.setText("")
        self.icon_vline.setPixmap(QtGui.QPixmap(":/icons/icons8-line-100.png"))
        self.icon_vline.setScaledContents(True)
        self.icon_vline.setObjectName("icon_vline")
        self.HLayout_3.addWidget(self.icon_vline)
        self.label_home = QtWidgets.QPushButton(self.navbar)
        self.label_home.setMinimumSize(QtCore.QSize(50, 50))
        self.label_home.setObjectName("label_home")
        self.HLayout_3.addWidget(self.label_home)
        spacerItem = QtWidgets.QSpacerItem(250, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.HLayout_3.addItem(spacerItem)
        self.label_admin = QtWidgets.QPushButton(self.navbar)
        self.label_admin.setMinimumSize(QtCore.QSize(50, 50))
        self.label_admin.setObjectName("label_admin")
        self.HLayout_3.addWidget(self.label_admin)
        self.horizontalLayout_4.addLayout(self.HLayout_3)
        self.verticalLayout.addWidget(self.navbar)
        self.frame_1 = QtWidgets.QFrame(self.centralwidget)
        self.frame_1.setStyleSheet("")
        self.frame_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1.setObjectName("frame_1")
        self.widget_2 = QtWidgets.QWidget(self.frame_1)
        self.widget_2.setGeometry(QtCore.QRect(70, 80, 641, 421))
        self.widget_2.setStyleSheet("QLabel{  \n"
"      font-family: \"Segoe UI\";\n"
"    font-size: 9pt;\n"
"    font-weight: bold;\n"
"    color: white;\n"
"}\n"
"\n"
"\n"
"QWidget {\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:20px;\n"
"} \n"
"\n"
"QLineEdit {\n"
"    background-color: rgba(255, 255, 255, 0.1); /* semi transparan */\n"
"    border: 1px solid rgba(0, 0, 0, 0.3);\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    color: black;\n"
"    font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid rgb(223, 190, 56); /* warna fokus */\n"
"    background-color: rgba(255, 255, 255, 0.2);\n"
"    outline: none;\n"
"}\n"
"")
        self.widget_2.setObjectName("widget_2")
        self.label_cari = QtWidgets.QLabel(self.widget_2)
        self.label_cari.setGeometry(QtCore.QRect(20, 20, 41, 31))
        self.label_cari.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_cari.setObjectName("label_cari")
        self.edit_carilaporan = QtWidgets.QLineEdit(self.widget_2)
        self.edit_carilaporan.setGeometry(QtCore.QRect(60, 20, 311, 31))
        self.edit_carilaporan.setStyleSheet("")
        self.edit_carilaporan.setObjectName("edit_carilaporan")
        self.tabel_laporan = QtWidgets.QTableView(self.widget_2)
        self.tabel_laporan.setGeometry(QtCore.QRect(25, 71, 591, 331))
        self.tabel_laporan.setStyleSheet("QTableView {\n"
"    background-color: #fdfdfd; /* Warna latar belakang */\n"
"    border: 1px solid #d6d6d6; /* Border luar */\n"
"    gridline-color: #d6d6d6; /* Warna garis grid */\n"
"    font-size: 14px; /* Ukuran font */\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #FF9933 ; /* Warna latar belakang header */\n"
"    color: white; /* Warna teks header */\n"
"    padding: 5px; /* Padding di header */\n"
"    border: none; /* Hilangkan border header */\n"
"    font-weight: bold; /* Teks tebal */\n"
"    text-align: center; /* Teks rata tengah */\n"
"}\n"
"\n"
"QTableCornerButton::section {\n"
"    background-color: #FF9933; /* Warna sudut tabel */\n"
"    border: none; /* Hilangkan border sudut */\n"
"}\n"
"\n"
"QTableView::item {\n"
"    padding: 5px; /* Padding untuk isi tabel */\n"
"}\n"
"\n"
"QTableView::item:selected {\n"
"    background-color: #ffd700; /* Warna item yang dipilih */\n"
"    color: black; /* Warna teks item yang dipilih */\n"
"}\n"
"")
        self.tabel_laporan.setAlternatingRowColors(True)
        self.tabel_laporan.setSortingEnabled(True)
        self.tabel_laporan.setObjectName("tabel_laporan")
        self.frame_2 = QtWidgets.QFrame(self.frame_1)
        self.frame_2.setGeometry(QtCore.QRect(80, 30, 621, 31))
        self.frame_2.setStyleSheet("QFrame {\n"
"    background-color: rgb(0, 165, 132);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QLabel {\n"
"    font-family: \"Segoe UI\";\n"
"    font-size: 9pt;\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.isi_judulfilm = QtWidgets.QLabel(self.frame_2)
        self.isi_judulfilm.setGeometry(QtCore.QRect(0, 5, 601, 21))
        self.isi_judulfilm.setStyleSheet("")
        self.isi_judulfilm.setAlignment(QtCore.Qt.AlignCenter)
        self.isi_judulfilm.setObjectName("isi_judulfilm")
        self.verticalLayout.addWidget(self.frame_1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Absolute Cinema"))
        self.tombol_kembali.setText(_translate("MainWindow", "KEMBALI"))
        self.label_home.setText(_translate("MainWindow", "HOME"))
        self.label_admin.setText(_translate("MainWindow", "ADMIN"))
        self.label_cari.setText(_translate("MainWindow", "Cari  :"))
        self.isi_judulfilm.setText(_translate("MainWindow", "LAPORAN"))
import resources_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
