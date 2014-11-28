# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from mainform import *
import dbjobs
import os
import sys
from dialogeditsub import DialogEditSub
from dialogfestivalssub import DialogFestivalsSub
from concertstablemodel import ConcertsTableModel
import datetime

# Constants
TIMEOUT_INFO = 3000
TIMEOUT_ERROR = 6000
WORK_STR_SEPARATOR = ' - '
APPDIR = os.path.abspath(os.path.dirname(sys.argv[0]))


class Mainformsub(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Mainformsub, self).__init__()
        self.setupUi(self)
        # Database part
        self.dbjobs = dbjobs.Database(APPDIR + '/database.db')
        # Prepare GUI, show/hide widgets
        self.prepare_gui()
        self.show_all_concerts()
        self.frame_search.adjustSize()

    ### MAIN FUNCTIONS ##############################################################################################################################

    def prepare_gui(self):
        # Hide not needed widgets
        self.frame_edit.hide()
        self.frame_search.adjustSize()
        # Create auto completer
        self.completer = QCompleter()
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer_model = QStringListModel()
        self.completer.setModel(self.completer_model)
        # Completion database functions connected with particular widgets
        self.completion_dict = {self.edit_state: {'db_func': self.dbjobs.get_completion_for_state}, 
                                self.edit_city: {'db_func': self.dbjobs.get_completion_for_city}, 
                                self.edit_hall: {'db_func': self.dbjobs.get_completion_for_hall}, 
                                self.edit_type: {'db_func': self.dbjobs.get_completion_for_type}, }
        # Set auto completer for widgets
        self.edit_state.setCompleter(self.completer)
        self.edit_hall.setCompleter(self.completer)
        self.edit_city.setCompleter(self.completer)
        self.edit_type.setCompleter(self.completer)
        # Connect widgets to completer function
        self.edit_state.textEdited.connect(self.getCompleterData)
        self.edit_hall.textEdited.connect(self.getCompleterData)
        self.edit_city.textEdited.connect(self.getCompleterData)
        self.edit_type.textEdited.connect(self.getCompleterData)
        # Main table with concerts
        headerdata = [self.tr('Datum'), self.tr('Stát'), self.tr('Město'), self.tr('Sál'), self.tr('Typ koncertu'), \
                      self.tr('Festival'), self.tr('Skladatel, skladba'), self.tr('Dirigenti'), self.tr('Solisti'), self.tr('Poznámka'), ]
        self.concerts_model = ConcertsTableModel(self, headerdata)
        # Proxy model is set here for sorting
        self.sort_proxy_model = QSortFilterProxyModel()
        self.sort_proxy_model.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.sort_proxy_model.setSourceModel(self.concerts_model)
        self.tableView.setModel(self.sort_proxy_model)
        # Set column size for main table
        self.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(8, QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeToContents)


    def getCompleterData(self, text):
        """
        Shows expressions for completion due to edit type
        """
        lineedit = self.sender()
        data = self.completion_dict[lineedit]['db_func'](text)
        stringlist = []
        if data != None:
            for item in data:
                stringlist += item
            if len(stringlist) == 7:
                stringlist[6] = '...'
            self.completer_model.setStringList(stringlist)

    def closeEvent(self, ce):
        """
        Close database
        """
        ce.accept()
        self.dbjobs.close()

    ### SEARCH FUNCTIONS ############################################################################################################################

    @pyqtSlot()
    def on_btn_search_clicked(self):
        print("search pressed")
        self.dbjobs.add_dirigent(1, "asdfasdfasdfasdfasdfs")
        self.dbjobs.add_(1, "asdfasdfasdfasdfasdfs")
        self.dbjobs.add_dirigent(1, "asdfasdfasdfasdfasdfs")

    def show_all_concerts(self):
        """
        Shows all concerts from the database in tableview
        """
        self.concerts_model.clear()
        self.concerts_model.beginResetModel()
        data = self.dbjobs.get_all_concerts()
        for row in data:
            concert_id = row[0]
            date = row[1]
            state = row[2]
            city = row[3]
            hall = row[4]
            type = row[5]
            note = row[6]
            festival = row[7]
            works = self.dbjobs.get_works(concert_id)
            joined_works = []
            for work in works:
                joined_works.append(WORK_STR_SEPARATOR.join(work))
            works = ', '.join(joined_works)
            dirigents = ', '.join([i for sub in self.dbjobs.get_dirigents(concert_id) for i in sub])
            soloists = ', '.join([i for sub in self.dbjobs.get_soloists(concert_id) for i in sub])
            new_row = [date, state, city, hall, type, festival, works, dirigents, soloists, note]
            self.concerts_model.addRow(new_row)
        self.concerts_model.endResetModel()

    ### ADD and EDIT FUNCTIONS ######################################################################################################################

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
        # Add festivals to combobox
        self.refresh_festivals()

    @pyqtSlot()
    def on_actionUpravit_triggered(self):
        self.frame_search.hide()
        self.frame_edit.show()

    @pyqtSlot()
    def on_btn_edit_confirm_clicked(self):
        dt = self.edit_date.dateTime()
        date = datetime.datetime(dt.date().year(), dt.date().month(), dt.date().day(), dt.time().hour(), dt.time().minute())
        state = self.edit_state.text().strip()
        city = self.edit_city.text().strip()
        hall = self.edit_hall.text().strip()
        type = self.edit_type.text().strip()
        festival_id = self.cb_festival.itemData(self.cb_festival.currentIndex(), Qt.UserRole)
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
        try:
            # Insert concert into DB
            concert_id = self.dbjobs.add_concert(festival_id, date, state, city, hall, type, note)
            # Insert dirigents into DB
            for i in range(self.lw_edit_dirigents.count()):
                self.dbjobs.add_dirigent(concert_id, self.lw_edit_dirigents.item(i).text())
            # Insert soloists into DB
            for i in range(self.lw_edit_soloists.count()):
                self.dbjobs.add_soloist(concert_id, self.lw_edit_soloists.item(i).text())
            # Insert works into DB
            for i in range(self.lw_edit_works.count()):
                data = self.lw_edit_works.item(i).text().split(WORK_STR_SEPARATOR)
                self.dbjobs.add_work(concert_id, data[0], data[1])

            self.statusbar.showMessage(self.tr('Záznam byl úspěšne přidán.'), TIMEOUT_INFO)
            self.on_btn_edit_cancel_clicked()
            self.show_all_concerts()
        except:
            print(sys.exc_info())
            self.statusbar.showMessage(self.tr('Záznam se nepodařilo přidat!'), TIMEOUT_ERROR)

    @pyqtSlot()
    def on_btn_dirigents_add_clicked(self):
        d = DialogEditSub(self, dirigents=True, caption=self.tr('Zadejte jméno dirigenta'))
        if d.exec_() == QDialog.Accepted:
            self.lw_edit_dirigents.addItem(d.dataDirigent)

    @pyqtSlot()
    def on_btn_soloists_add_clicked(self):
        d = DialogEditSub(self, soloists=True, caption=self.tr('Zadejte jméno sólistu'))
        if d.exec_() == QDialog.Accepted:
            self.lw_edit_soloists.addItem(d.dataSoloist)

    @pyqtSlot()
    def on_btn_works_add_clicked(self):
        d = DialogEditSub(self, works=True, caption=self.tr('Zadejte jméno skladatele a název díla'))
        if d.exec_() == QDialog.Accepted:
            self.lw_edit_works.addItem('{}{}{}'.format(d.dataComposer, WORK_STR_SEPARATOR, d.dataWork))

    @pyqtSlot()
    def on_btn_dirigents_remove_clicked(self):
        if len(self.lw_edit_dirigents.selectedItems()) > 0:
            self.lw_edit_dirigents.takeItem(self.lw_edit_dirigents.currentIndex().row())

    @pyqtSlot()
    def on_btn_soloists_remove_clicked(self):
        if len(self.lw_edit_soloists.selectedItems()) > 0:
            self.lw_edit_soloists.takeItem(self.lw_edit_soloists.currentIndex().row())

    @pyqtSlot()
    def on_btn_works_remove_clicked(self):
        if len(self.lw_edit_works.selectedItems()) > 0:
            self.lw_edit_works.takeItem(self.lw_edit_works.currentIndex().row())

    @pyqtSlot()
    def on_actionSprava_festivalov_triggered(self):
        d = DialogFestivalsSub(self)
        d.exec_()
        self.refresh_festivals()

    def refresh_festivals(self):
        # Add festivals to combobox
        self.cb_festival.clear()
        festivals = self.dbjobs.get_all_festivals()
        for festival in festivals:
            self.cb_festival.addItem(festival[1], festival[0])

# End of Mainformsub.py
