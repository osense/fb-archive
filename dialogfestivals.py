# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogfestivals.ui'
#
# Created: Fri Nov 28 11:12:39 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(388, 386)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.btn_dirigents_add = QtWidgets.QToolButton(Dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/Actions-list-add-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_dirigents_add.setIcon(icon)
        self.btn_dirigents_add.setAutoRaise(True)
        self.btn_dirigents_add.setObjectName("btn_dirigents_add")
        self.gridLayout.addWidget(self.btn_dirigents_add, 0, 1, 1, 1)
        self.btn_dirigents_remove = QtWidgets.QToolButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/Actions-list-remove-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_dirigents_remove.setIcon(icon1)
        self.btn_dirigents_remove.setAutoRaise(True)
        self.btn_dirigents_remove.setObjectName("btn_dirigents_remove")
        self.gridLayout.addWidget(self.btn_dirigents_remove, 0, 2, 1, 1)
        self.lw_festivals = QtWidgets.QListWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lw_festivals.sizePolicy().hasHeightForWidth())
        self.lw_festivals.setSizePolicy(sizePolicy)
        self.lw_festivals.setObjectName("lw_festivals")
        self.gridLayout.addWidget(self.lw_festivals, 1, 0, 1, 3)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_close = QtWidgets.QPushButton(Dialog)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/Actions-dialog-close-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_close.setIcon(icon2)
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout.addWidget(self.btn_close)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Správa festivalů"))
        self.label_7.setText(_translate("Dialog", "Festivaly"))
        self.btn_dirigents_add.setText(_translate("Dialog", "..."))
        self.btn_dirigents_remove.setText(_translate("Dialog", "..."))
        self.btn_close.setText(_translate("Dialog", "Zavřít"))

import resource_rc
