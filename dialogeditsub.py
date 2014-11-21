#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from dialogedit import *


class DialogAddGroup(QDialog, Ui_DialogAddGroup):
    """
    Dialog to add new group
    """
    def __init__(self, parent=None, f=Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint):
        super(DialogAddGroup, self).__init__(parent, f)
        self.setupUi(self)
        self.adjustSize()
