# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/total_article.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TotalArticle(object):
    def setupUi(self, TotalArticle):
        TotalArticle.setObjectName("TotalArticle")
        TotalArticle.resize(516, 312)
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(13)
        TotalArticle.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(TotalArticle)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(TotalArticle)
        self.label_4.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(99, 110, 114);")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(TotalArticle)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.labelArticle = QtWidgets.QLabel(TotalArticle)
        self.labelArticle.setMinimumSize(QtCore.QSize(0, 0))
        self.labelArticle.setText("")
        self.labelArticle.setObjectName("labelArticle")
        self.horizontalLayout.addWidget(self.labelArticle)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(15)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(TotalArticle)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.labelValeur = QtWidgets.QLabel(TotalArticle)
        self.labelValeur.setMinimumSize(QtCore.QSize(0, 0))
        self.labelValeur.setText("")
        self.labelValeur.setObjectName("labelValeur")
        self.horizontalLayout_2.addWidget(self.labelValeur)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(15)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(TotalArticle)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.labelTotalQte = QtWidgets.QLabel(TotalArticle)
        self.labelTotalQte.setMinimumSize(QtCore.QSize(0, 0))
        self.labelTotalQte.setText("")
        self.labelTotalQte.setObjectName("labelTotalQte")
        self.horizontalLayout_3.addWidget(self.labelTotalQte)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.line = QtWidgets.QFrame(TotalArticle)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.buttonBox = QtWidgets.QDialogButtonBox(TotalArticle)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(TotalArticle)
        self.buttonBox.accepted.connect(TotalArticle.accept)
        self.buttonBox.rejected.connect(TotalArticle.reject)
        QtCore.QMetaObject.connectSlotsByName(TotalArticle)

    def retranslateUi(self, TotalArticle):
        _translate = QtCore.QCoreApplication.translate
        TotalArticle.setWindowTitle(_translate("TotalArticle", "Total Des Article"))
        self.label_4.setText(_translate("TotalArticle", "Total"))
        self.label.setText(_translate("TotalArticle", "Total Des Articles"))
        self.label_2.setText(_translate("TotalArticle", "Total Des Valeurs"))
        self.label_3.setText(_translate("TotalArticle", "Total Des Quantité"))
