# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogedit.ui'
#
# Created: Fri Nov 21 11:09:47 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogEdit(object):
    def setupUi(self, DialogEdit):
        DialogEdit.setObjectName("DialogEdit")
        DialogEdit.resize(222, 154)
        self.gridLayout_4 = QtWidgets.QGridLayout(DialogEdit)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.frame_works = QtWidgets.QFrame(DialogEdit)
        self.frame_works.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_works.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_works.setObjectName("frame_works")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_works)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.frame_works)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.frame_works)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame_works)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame_works)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.gridLayout_4.addWidget(self.frame_works, 0, 0, 1, 1)
        self.frame_dirigent = QtWidgets.QFrame(DialogEdit)
        self.frame_dirigent.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_dirigent.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_dirigent.setObjectName("frame_dirigent")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_dirigent)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtWidgets.QLabel(self.frame_dirigent)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame_dirigent)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_3.addWidget(self.lineEdit_3, 0, 1, 1, 1)
        self.gridLayout_4.addWidget(self.frame_dirigent, 1, 0, 1, 1)
        self.frame_soloists = QtWidgets.QFrame(DialogEdit)
        self.frame_soloists.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_soloists.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_soloists.setObjectName("frame_soloists")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_soloists)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(self.frame_soloists)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.frame_soloists)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_2.addWidget(self.lineEdit_4, 0, 1, 1, 1)
        self.gridLayout_4.addWidget(self.frame_soloists, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_edit_confirm = QtWidgets.QPushButton(DialogEdit)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/Actions-dialog-ok-apply-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_edit_confirm.setIcon(icon)
        self.btn_edit_confirm.setObjectName("btn_edit_confirm")
        self.horizontalLayout.addWidget(self.btn_edit_confirm)
        self.btn_edit_cancel = QtWidgets.QPushButton(DialogEdit)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/Actions-dialog-close-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_edit_cancel.setIcon(icon1)
        self.btn_edit_cancel.setObjectName("btn_edit_cancel")
        self.horizontalLayout.addWidget(self.btn_edit_cancel)
        self.gridLayout_4.addLayout(self.horizontalLayout, 3, 0, 1, 1)

        self.retranslateUi(DialogEdit)
        QtCore.QMetaObject.connectSlotsByName(DialogEdit)

    def retranslateUi(self, DialogEdit):
        _translate = QtCore.QCoreApplication.translate
        DialogEdit.setWindowTitle(_translate("DialogEdit", "Dialog"))
        self.label.setText(_translate("DialogEdit", "Skladatel:"))
        self.label_2.setText(_translate("DialogEdit", "Skladba:"))
        self.label_3.setText(_translate("DialogEdit", "Dirigent:"))
        self.label_4.setText(_translate("DialogEdit", "Solista:"))
        self.btn_edit_confirm.setText(_translate("DialogEdit", "Přidat"))
        self.btn_edit_cancel.setText(_translate("DialogEdit", "Zrušit"))

import resource_rc
