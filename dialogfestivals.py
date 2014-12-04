# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogfestivals.ui'
#
# Created: Thu Dec  4 18:33:30 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogFestivals(object):
    def setupUi(self, DialogFestivals):
        DialogFestivals.setObjectName("DialogFestivals")
        DialogFestivals.resize(387, 386)
        self.gridLayout_2 = QtWidgets.QGridLayout(DialogFestivals)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtWidgets.QLabel(DialogFestivals)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.btn_festivals_add = QtWidgets.QToolButton(DialogFestivals)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/Actions-list-add-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_festivals_add.setIcon(icon)
        self.btn_festivals_add.setAutoRaise(True)
        self.btn_festivals_add.setObjectName("btn_festivals_add")
        self.gridLayout.addWidget(self.btn_festivals_add, 0, 1, 1, 1)
        self.btn_festivals_remove = QtWidgets.QToolButton(DialogFestivals)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/Actions-list-remove-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_festivals_remove.setIcon(icon1)
        self.btn_festivals_remove.setAutoRaise(True)
        self.btn_festivals_remove.setObjectName("btn_festivals_remove")
        self.gridLayout.addWidget(self.btn_festivals_remove, 0, 2, 1, 1)
        self.lw_festivals = QtWidgets.QListWidget(DialogFestivals)
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
        self.btn_close = QtWidgets.QPushButton(DialogFestivals)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/Actions-dialog-close-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_close.setIcon(icon2)
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout.addWidget(self.btn_close)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(DialogFestivals)
        self.btn_close.clicked.connect(DialogFestivals.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogFestivals)

    def retranslateUi(self, DialogFestivals):
        _translate = QtCore.QCoreApplication.translate
        DialogFestivals.setWindowTitle(_translate("DialogFestivals", "Správa festivalů"))
        self.label_7.setText(_translate("DialogFestivals", "Festivaly"))
        self.btn_festivals_add.setText(_translate("DialogFestivals", "..."))
        self.btn_festivals_remove.setText(_translate("DialogFestivals", "..."))
        self.btn_close.setText(_translate("DialogFestivals", "Zavřít"))

import resource_rc
