# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from mainform import *
import dbjobs
import os
import sys

APPDIR = os.path.abspath(os.path.dirname(sys.argv[0]))

class Mainformsub(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Mainformsub, self).__init__()
        self.setupUi(self)
        # Prepare GUI, show/hide widgets
        self.prepare_gui()
        # Database part
        self.db = dbjobs.Database(APPDIR + '/database.db')

    def prepare_gui(self):
        # Hide not needed widgets
        self.frame_edit.hide()

    @pyqtSlot()
    def on_btn_search_clicked(self):
        print("search pressed")

    @pyqtSlot()
    def on_btn_edit_cancel_clicked(self):
        self.frame_edit.hide()
        self.frame_search.show()

    @pyqtSlot()
    def on_actionPridat_triggered(self):
        self.frame_search.hide()
        self.frame_edit.show()

    @pyqtSlot()
    def on_actionUpravit_triggered(self):
        self.frame_search.hide()
        self.frame_edit.show()

# End of Mainformsub.py