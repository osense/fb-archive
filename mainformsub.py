# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from mainform import *
import dbjobs
import os
import sys
from dialogeditsub import DialogEditSub
import datetime

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
        self.frame_search.adjustSize()

    @pyqtSlot()
    def on_btn_search_clicked(self):
        print("search pressed")

    @pyqtSlot()
    def on_btn_edit_cancel_clicked(self):
        self.frame_edit.hide()
        self.frame_search.show()
        # Clear widgets
        self.edit_city.clear()
        self.edit_date.clear()
        self.edit_hall.clear()
        self.edit_note.clear()
        self.edit_state.clear()
        self.edit_type.clear()
        self.cb_festival.setCurrentIndex(0)
        self.lw_edit_dirigents.clear()
        self.lw_edit_soloists.clear()
        self.lw_edit_works.clear()

    @pyqtSlot()
    def on_actionPridat_triggered(self):
        self.frame_search.hide()
        self.frame_edit.show()
        # Set current datetime
        self.edit_date.setDateTime(datetime.datetime.today())

    @pyqtSlot()
    def on_actionUpravit_triggered(self):
        self.frame_search.hide()
        self.frame_edit.show()

    @pyqtSlot()
    def on_btn_edit_confirm_clicked(self):
        date = self.edit_date.dateTime()
        state = self.edit_state.text().strip()
        city = self.edit_city.text().strip()
        hall = self.edit_hall.text().strip()
        type = self.edit_type.text().strip()
        festival_id = self.cb_festival.currentIndex() or None
        note = self.edit_note.toPlainText().strip() or None
        # Check input data
        if len(state) == 0:
            QMessageBox.warning(self, self.tr('Varování'), self.tr('Stát konání musí být vyplněn.'))
            return
        elif len(city) == 0:
            QMessageBox.warning(self, self.tr('Varování'), self.tr('Město konání musí být vyplněno.'))
            return
        elif len(hall) == 0:
            QMessageBox.warning(self, self.tr('Varování'), self.tr('Sál musí být vyplněn.'))
            return



        print("confirm")

    @pyqtSlot()
    def on_btn_dirigents_add_clicked(self):
        d = DialogEditSub(dirigents=True, caption=self.tr('Zadejte jméno dirigenta'))
        if d.exec_() == QDialog.Accepted:
            self.lw_edit_dirigents.addItem(d.dataDirigent)

    @pyqtSlot()
    def on_btn_soloists_add_clicked(self):
        d = DialogEditSub(soloists=True, caption=self.tr('Zadejte jméno sólistu'))
        if d.exec_() == QDialog.Accepted:
            self.lw_edit_soloists.addItem(d.dataSoloist)

    @pyqtSlot()
    def on_btn_works_add_clicked(self):
        d = DialogEditSub(works=True, caption=self.tr('Zadejte jméno skladatele a název díla'))
        if d.exec_() == QDialog.Accepted:
            self.lw_edit_works.addItem('{} - {}'.format(d.dataComposer, d.dataWork))

    @pyqtSlot()
    def on_btn_dirigents_remove_clicked(self):
        if self.lw_edit_dirigents.currentIndex() != None:
            self.lw_edit_dirigents.takeItem(self.lw_edit_dirigents.currentIndex().row())

    @pyqtSlot()
    def on_btn_soloists_remove_clicked(self):
        if self.lw_edit_soloists.currentIndex() != None:
            self.lw_edit_soloists.takeItem(self.lw_edit_soloists.currentIndex().row())

    @pyqtSlot()
    def on_btn_works_remove_clicked(self):
        if self.lw_edit_works.currentIndex() != None:
            self.lw_edit_works.takeItem(self.lw_edit_works.currentIndex().row())

# End of Mainformsub.py