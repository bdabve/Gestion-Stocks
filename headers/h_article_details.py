# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_files\article_details.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ArticleDetails(object):
    def setupUi(self, ArticleDetails):
        ArticleDetails.setObjectName("ArticleDetails")
        ArticleDetails.setWindowModality(QtCore.Qt.WindowModal)
        ArticleDetails.resize(533, 577)
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(11)
        ArticleDetails.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/clipboard-list.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ArticleDetails.setWindowIcon(icon)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ArticleDetails)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelArticlId = QtWidgets.QLabel(ArticleDetails)
        self.labelArticlId.setMinimumSize(QtCore.QSize(0, 84))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(14)
        self.labelArticlId.setFont(font)
        self.labelArticlId.setStyleSheet("background-color: rgb(0, 170, 127);\n"
"color: rgb(255, 255, 255);")
        self.labelArticlId.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.labelArticlId.setAlignment(QtCore.Qt.AlignCenter)
        self.labelArticlId.setObjectName("labelArticlId")
        self.verticalLayout_2.addWidget(self.labelArticlId)
        self.frame = QtWidgets.QFrame(ArticleDetails)
        self.frame.setMinimumSize(QtCore.QSize(0, 417))
        self.frame.setStyleSheet("border-color: rgb(85, 0, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setContentsMargins(10, -1, -1, -1)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setMinimumSize(QtCore.QSize(126, 0))
        self.label_2.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_10.addWidget(self.label_2)
        self.labelCat = QtWidgets.QLabel(self.frame)
        self.labelCat.setMinimumSize(QtCore.QSize(341, 0))
        self.labelCat.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.labelCat.setFont(font)
        self.labelCat.setStyleSheet("")
        self.labelCat.setText("")
        self.labelCat.setObjectName("labelCat")
        self.horizontalLayout_10.addWidget(self.labelCat)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, -1, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setMinimumSize(QtCore.QSize(126, 0))
        self.label.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.labelCode = QtWidgets.QLabel(self.frame)
        self.labelCode.setMinimumSize(QtCore.QSize(341, 0))
        self.labelCode.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.labelCode.setFont(font)
        self.labelCode.setStyleSheet("")
        self.labelCode.setText("")
        self.labelCode.setObjectName("labelCode")
        self.horizontalLayout.addWidget(self.labelCode)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, -1, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setMinimumSize(QtCore.QSize(126, 0))
        self.label_3.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.labelDesig = QtWidgets.QLabel(self.frame)
        self.labelDesig.setMinimumSize(QtCore.QSize(341, 0))
        self.labelDesig.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.labelDesig.setFont(font)
        self.labelDesig.setStyleSheet("")
        self.labelDesig.setText("")
        self.labelDesig.setObjectName("labelDesig")
        self.horizontalLayout_2.addWidget(self.labelDesig)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(10, -1, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setMinimumSize(QtCore.QSize(126, 0))
        self.label_5.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.labelRef = QtWidgets.QLabel(self.frame)
        self.labelRef.setMinimumSize(QtCore.QSize(341, 0))
        self.labelRef.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.labelRef.setFont(font)
        self.labelRef.setStyleSheet("")
        self.labelRef.setText("")
        self.labelRef.setObjectName("labelRef")
        self.horizontalLayout_3.addWidget(self.labelRef)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(10, -1, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setMinimumSize(QtCore.QSize(126, 0))
        self.label_7.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("")
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.labelEmp = QtWidgets.QLabel(self.frame)
        self.labelEmp.setMinimumSize(QtCore.QSize(341, 0))
        self.labelEmp.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.labelEmp.setFont(font)
        self.labelEmp.setStyleSheet("")
        self.labelEmp.setText("")
        self.labelEmp.setObjectName("labelEmp")
        self.horizontalLayout_4.addWidget(self.labelEmp)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(10, -1, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setMinimumSize(QtCore.QSize(126, 0))
        self.label_9.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("")
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_5.addWidget(self.label_9)
        self.labelUM = QtWidgets.QLabel(self.frame)
        self.labelUM.setMinimumSize(QtCore.QSize(341, 0))
        self.labelUM.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.labelUM.setFont(font)
        self.labelUM.setStyleSheet("")
        self.labelUM.setText("")
        self.labelUM.setObjectName("labelUM")
        self.horizontalLayout_5.addWidget(self.labelUM)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(10, -1, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setMinimumSize(QtCore.QSize(126, 0))
        self.label_11.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("")
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_6.addWidget(self.label_11)
        self.labelQte = QtWidgets.QLabel(self.frame)
        self.labelQte.setMinimumSize(QtCore.QSize(341, 0))
        self.labelQte.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.labelQte.setFont(font)
        self.labelQte.setStyleSheet("")
        self.labelQte.setText("")
        self.labelQte.setObjectName("labelQte")
        self.horizontalLayout_6.addWidget(self.labelQte)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(10, -1, -1, -1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_13 = QtWidgets.QLabel(self.frame)
        self.label_13.setMinimumSize(QtCore.QSize(126, 0))
        self.label_13.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("")
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_7.addWidget(self.label_13)
        self.labelPrix = QtWidgets.QLabel(self.frame)
        self.labelPrix.setMinimumSize(QtCore.QSize(341, 0))
        self.labelPrix.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.labelPrix.setFont(font)
        self.labelPrix.setStyleSheet("")
        self.labelPrix.setText("")
        self.labelPrix.setObjectName("labelPrix")
        self.horizontalLayout_7.addWidget(self.labelPrix)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(10, -1, -1, -1)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_15 = QtWidgets.QLabel(self.frame)
        self.label_15.setMinimumSize(QtCore.QSize(126, 0))
        self.label_15.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("")
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_8.addWidget(self.label_15)
        self.labelValeur = QtWidgets.QLabel(self.frame)
        self.labelValeur.setMinimumSize(QtCore.QSize(341, 0))
        self.labelValeur.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.labelValeur.setFont(font)
        self.labelValeur.setStyleSheet("")
        self.labelValeur.setText("")
        self.labelValeur.setObjectName("labelValeur")
        self.horizontalLayout_8.addWidget(self.labelValeur)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.line_2 = QtWidgets.QFrame(self.frame)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setContentsMargins(10, -1, -1, -1)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setMinimumSize(QtCore.QSize(126, 0))
        self.label_4.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_11.addWidget(self.label_4)
        self.labelNote = QtWidgets.QLabel(self.frame)
        self.labelNote.setMinimumSize(QtCore.QSize(341, 0))
        self.labelNote.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        self.labelNote.setFont(font)
        self.labelNote.setStyleSheet("")
        self.labelNote.setText("")
        self.labelNote.setWordWrap(True)
        self.labelNote.setObjectName("labelNote")
        self.horizontalLayout_11.addWidget(self.labelNote)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.verticalLayout_2.addWidget(self.frame)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setContentsMargins(-1, 5, -1, 5)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.toolButtonMovement = QtWidgets.QToolButton(ArticleDetails)
        self.toolButtonMovement.setMinimumSize(QtCore.QSize(120, 36))
        self.toolButtonMovement.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolButtonMovement.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.toolButtonMovement.setArrowType(QtCore.Qt.DownArrow)
        self.toolButtonMovement.setObjectName("toolButtonMovement")
        self.horizontalLayout_9.addWidget(self.toolButtonMovement)
        self.toolButtonAction = QtWidgets.QToolButton(ArticleDetails)
        self.toolButtonAction.setMinimumSize(QtCore.QSize(120, 36))
        self.toolButtonAction.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolButtonAction.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.toolButtonAction.setObjectName("toolButtonAction")
        self.horizontalLayout_9.addWidget(self.toolButtonAction)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem)
        self.pushButtonClose = QtWidgets.QPushButton(ArticleDetails)
        self.pushButtonClose.setMinimumSize(QtCore.QSize(100, 36))
        self.pushButtonClose.setAutoDefault(False)
        self.pushButtonClose.setDefault(True)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.horizontalLayout_9.addWidget(self.pushButtonClose)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)

        self.retranslateUi(ArticleDetails)
        self.pushButtonClose.clicked.connect(ArticleDetails.close)
        QtCore.QMetaObject.connectSlotsByName(ArticleDetails)

    def retranslateUi(self, ArticleDetails):
        _translate = QtCore.QCoreApplication.translate
        ArticleDetails.setWindowTitle(_translate("ArticleDetails", "ArticleDetails"))
        self.labelArticlId.setText(_translate("ArticleDetails", "Fiche de Stock N° "))
        self.label_2.setText(_translate("ArticleDetails", "Cat ID"))
        self.label.setText(_translate("ArticleDetails", "Code"))
        self.label_3.setText(_translate("ArticleDetails", "Designation"))
        self.label_5.setText(_translate("ArticleDetails", "Reference"))
        self.label_7.setText(_translate("ArticleDetails", "Emplacement"))
        self.label_9.setText(_translate("ArticleDetails", "U-Mesure"))
        self.label_11.setText(_translate("ArticleDetails", "Quantité"))
        self.label_13.setText(_translate("ArticleDetails", "Prix"))
        self.label_15.setText(_translate("ArticleDetails", "Valeur"))
        self.label_4.setText(_translate("ArticleDetails", "Observation"))
        self.toolButtonMovement.setText(_translate("ArticleDetails", "Movement"))
        self.toolButtonAction.setText(_translate("ArticleDetails", "Action"))
        self.pushButtonClose.setText(_translate("ArticleDetails", "Close"))

