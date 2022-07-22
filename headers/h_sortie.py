# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_files\sortie.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Sortie(object):
    def setupUi(self, Sortie):
        Sortie.setObjectName("Sortie")
        Sortie.resize(485, 343)
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        Sortie.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/box--minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Sortie.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(Sortie)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(Sortie)
        self.label_4.setMinimumSize(QtCore.QSize(0, 110))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 110))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color: rgb(239, 41, 41);\n"
"color: rgb(255, 255, 255);")
        self.label_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(Sortie)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.lineEditCode = QtWidgets.QLineEdit(Sortie)
        self.lineEditCode.setMinimumSize(QtCore.QSize(358, 30))
        self.lineEditCode.setReadOnly(True)
        self.lineEditCode.setObjectName("lineEditCode")
        self.gridLayout.addWidget(self.lineEditCode, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Sortie)
        self.label_3.setMinimumSize(QtCore.QSize(85, 0))
        self.label_3.setMaximumSize(QtCore.QSize(79, 30))
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.dateEditSrtDate = QtWidgets.QDateEdit(Sortie)
        self.dateEditSrtDate.setWrapping(False)
        self.dateEditSrtDate.setFrame(True)
        self.dateEditSrtDate.setCurrentSection(QtWidgets.QDateTimeEdit.DaySection)
        self.dateEditSrtDate.setCalendarPopup(True)
        self.dateEditSrtDate.setObjectName("dateEditSrtDate")
        self.gridLayout.addWidget(self.dateEditSrtDate, 0, 1, 1, 1)
        self.spinBoxQte = QtWidgets.QSpinBox(Sortie)
        self.spinBoxQte.setMinimumSize(QtCore.QSize(358, 30))
        self.spinBoxQte.setMinimum(1)
        self.spinBoxQte.setMaximum(10000)
        self.spinBoxQte.setObjectName("spinBoxQte")
        self.gridLayout.addWidget(self.spinBoxQte, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(Sortie)
        self.label.setMinimumSize(QtCore.QSize(85, 0))
        self.label.setMaximumSize(QtCore.QSize(79, 30))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.spinBoxPrix = QtWidgets.QSpinBox(Sortie)
        self.spinBoxPrix.setEnabled(False)
        self.spinBoxPrix.setMinimumSize(QtCore.QSize(358, 30))
        self.spinBoxPrix.setMaximum(999999999)
        self.spinBoxPrix.setObjectName("spinBoxPrix")
        self.gridLayout.addWidget(self.spinBoxPrix, 3, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Sortie)
        self.label_2.setMinimumSize(QtCore.QSize(85, 0))
        self.label_2.setMaximumSize(QtCore.QSize(79, 30))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.pushButtonAddSortie = QtWidgets.QPushButton(Sortie)
        self.pushButtonAddSortie.setMinimumSize(QtCore.QSize(101, 35))
        self.pushButtonAddSortie.setObjectName("pushButtonAddSortie")
        self.gridLayout.addWidget(self.pushButtonAddSortie, 4, 1, 1, 1)
        self.pushButtonClose = QtWidgets.QPushButton(Sortie)
        self.pushButtonClose.setMinimumSize(QtCore.QSize(101, 35))
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.gridLayout.addWidget(self.pushButtonClose, 4, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Sortie)
        self.pushButtonClose.clicked.connect(Sortie.close)
        QtCore.QMetaObject.connectSlotsByName(Sortie)

    def retranslateUi(self, Sortie):
        _translate = QtCore.QCoreApplication.translate
        Sortie.setWindowTitle(_translate("Sortie", "Nouvelle Sortie"))
        self.label_4.setText(_translate("Sortie", "Nouvelle Sortie"))
        self.label_5.setText(_translate("Sortie", "Date"))
        self.label_3.setText(_translate("Sortie", "Code"))
        self.label.setText(_translate("Sortie", "Quantité"))
        self.label_2.setText(_translate("Sortie", "Prix"))
        self.pushButtonAddSortie.setText(_translate("Sortie", "Sortie"))
        self.pushButtonClose.setText(_translate("Sortie", "Annuler"))

