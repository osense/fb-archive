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
from constants import *

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
        self.frame.adjustSize()

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
                                self.edit_type: {'db_func': self.dbjobs.get_completion_for_type},
                                self.edit_name: {'db_func': self.dbjobs.get_completion_for_name}, }
        # Set auto completer for widgets
        self.edit_state.setCompleter(self.completer)
        self.edit_hall.setCompleter(self.completer)
        self.edit_city.setCompleter(self.completer)
        self.edit_type.setCompleter(self.completer)
        self.edit_name.setCompleter(self.completer)
        # Connect widgets to completer function
        self.edit_state.textEdited.connect(self.getCompleterData)
        self.edit_hall.textEdited.connect(self.getCompleterData)
        self.edit_city.textEdited.connect(self.getCompleterData)
        self.edit_type.textEdited.connect(self.getCompleterData)
        self.edit_name.textEdited.connect(self.getCompleterData)
        # Main table with concerts
        headerdata = [self.tr('Datum od'), self.tr('Datum do'), self.tr("Název"), self.tr('Stát'), self.tr('Město'), self.tr('Sál'), self.tr('Typ koncertu'), \
                      self.tr('Festival'), self.tr('Skladatel, skladba'), self.tr('Solisti'), self.tr('Dirigenti'), self.tr('Sbory'), self.tr('Poznámka'), ]
        self.concerts_model = ConcertsTableModel(self, headerdata)
        # Proxy model is set here for sorting
        self.sort_proxy_model = QSortFilterProxyModel()
        self.sort_proxy_model.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.sort_proxy_model.setSourceModel(self.concerts_model)
        self.tableView.setModel(self.sort_proxy_model)
        # Set column size for main table
        self.tableView.horizontalHeader().setSectionResizeMode(COLUMN_DATE_FROM, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(COLUMN_DATE_TO, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(COLUMN_NAME, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(COLUMN_STATE, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(COLUMN_CITY, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(COLUMN_HALL, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(COLUMN_TYPE, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(COLUMN_FESTIVAL, QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setSectionResizeMode(COLUMN_WORKS, QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(COLUMN_SOLOISTS, QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(COLUMN_DIRIGENTS, QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(COLUMN_CHOIRS, QHeaderView.Stretch)

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
            date_from = row[1]
            date_to = row[2]
            name = row[3]
            state = row[4]
            city = row[5]
            hall = row[6]
            type = row[7]
            note = row[8]
            festival = row[9]
            festival_id = row[10]
            works = self.dbjobs.get_works(concert_id)
            joined_works = []
            for work in works:
                joined_works.append(WORK_STR_SEPARATOR.join(work[1:]))
            works = ', '.join(joined_works)
            dirigents = ', '.join([i for sub in self.dbjobs.get_dirigents(concert_id) for i in sub])
            choirs = ', '.join([i for sub in self.dbjobs.get_choirs(concert_id) for i in sub])
            soloists = ', '.join([i for sub in self.dbjobs.get_soloists_for_concert(concert_id) for i in sub])
            new_row = [date_from, date_to, name, state, city, hall, type, festival, works, soloists, dirigents, choirs, note, concert_id, festival_id]
            self.concerts_model.addRow(new_row)
        self.concerts_model.endResetModel()

    ### ADD and EDIT FUNCTIONS ######################################################################################################################

    @pyqtSlot()
    def on_btn_edit_cancel_clicked(self):
        self.frame_edit.hide()
        self.frame_search.show()
        self.clear_widgets()

    def clear_widgets(self):
        """
        Clears widgets
        """
        self.edit_city.clear()
        self.edit_date_from.clear()
        self.edit_date_to.clear()
        self.edit_hall.clear()
        self.edit_note.clear()
        self.edit_state.clear()
        self.edit_name.clear()
        self.edit_type.clear()
        self.cb_festival.setCurrentIndex(0)
        self.lw_edit_dirigents.clear()
        self.lw_edit_choirs.clear()
        self.tw_edit_works.clear()

    @pyqtSlot()
    def on_actionPridat_triggered(self):
        self.clear_widgets()
        self.frame_search.hide()
        self.frame_edit.show()
        # Add festivals to combobox
        self.refresh_festivals()
        # Show / Hide unused buttons
        self.btn_edit_confirm.show()
        self.btn_edit_save.hide()
        # Set current datetime
        self.edit_date_from.setDateTime(datetime.datetime.today())
        self.edit_date_to.setDateTime(datetime.datetime.today())

    @pyqtSlot("QModelIndex")
    def on_tableView_doubleClicked(self, index):
        self.on_actionUpravit_triggered()

    @pyqtSlot()
    def on_actionUpravit_triggered(self):
        selected_indexes = self.tableView.selectedIndexes()
        if len(selected_indexes) > 0:
            self.clear_widgets()
            self.frame_search.hide()
            self.frame_edit.show()
            # Add festivals to combobox
            self.refresh_festivals()
            # Show / Hide unused buttons
            self.btn_edit_confirm.hide()
            self.btn_edit_save.show()
            # Load data to widgets
            self.now_edited_concert_id = self.concerts_model.get_item_data(selected_indexes[0], COLUMN_CONCERT_ID)
            self.edit_name.setText(self.concerts_model.get_item_data(selected_indexes[0], COLUMN_NAME))
            self.edit_date_from.setDateTime(self.concerts_model.get_item_data(selected_indexes[0], COLUMN_DATE_FROM))
            self.edit_date_to.setDateTime(self.concerts_model.get_item_data(selected_indexes[0], COLUMN_DATE_TO))
            self.edit_state.setText(self.concerts_model.get_item_data(selected_indexes[0], COLUMN_STATE))
            self.edit_city.setText(self.concerts_model.get_item_data(selected_indexes[0], COLUMN_CITY))
            self.edit_hall.setText(self.concerts_model.get_item_data(selected_indexes[0], COLUMN_HALL))
            self.edit_type.setText(self.concerts_model.get_item_data(selected_indexes[0], COLUMN_TYPE))
            self.cb_festival.setCurrentIndex(self.cb_festival.findData(self.concerts_model.get_item_data(selected_indexes[0], COLUMN_FESTIVAL_ID)))
            self.edit_note.setText(self.concerts_model.get_item_data(selected_indexes[0], COLUMN_NOTE))
            # choir
            if len(self.concerts_model.get_item_data(selected_indexes[0], COLUMN_CHOIRS)) != 0:
                self.lw_edit_choirs.addItems(self.concerts_model.get_item_data(selected_indexes[0], COLUMN_CHOIRS).split(', '))
            # dirigents
            if len(self.concerts_model.get_item_data(selected_indexes[0], COLUMN_DIRIGENTS)) != 0:
                self.lw_edit_dirigents.addItems(self.concerts_model.get_item_data(selected_indexes[0], COLUMN_DIRIGENTS).split(', '))
            # soloists and works
            works = self.dbjobs.get_works(self.now_edited_concert_id)
            for work in works:
                work_item = QTreeWidgetItem()
                work_item.setText(0, '{}{}{}'.format(work[1], WORK_STR_SEPARATOR, work[2]))
                soloists = self.dbjobs.get_soloists_for_work(work[0])
                for soloist in soloists:
                    soloist_item = QTreeWidgetItem()
                    soloist_item.setText(0, soloist[0])
                    work_item.addChild(soloist_item)
                self.tw_edit_works.invisibleRootItem().addChild(work_item)
            self.tw_edit_works.expandAll()
        else:
            QMessageBox.warning(self, self.tr('Varování'), self.tr('Nebyl vybrán žádnej koncert.'))

    @pyqtSlot()
    def on_btn_edit_confirm_clicked(self):
        dt_from = self.edit_date_from.dateTime()
        date_from = datetime.datetime(dt_from.date().year(), dt_from.date().month(), dt_from.date().day(), dt_from.time().hour(), dt_from.time().minute())
        dt_to = self.edit_date_to.dateTime()
        date_to = datetime.datetime(dt_to.date().year(), dt_to.date().month(), dt_to.date().day(), dt_to.time().hour(), dt_to.time().minute())
        name = self.edit_name.text().strip()
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
            concert_id = self.dbjobs.add_concert(name, festival_id, date_from, date_to, state, city, hall, type, note)
            # Insert choirs into DB
            for i in range(self.lw_edit_choirs.count()):
                self.dbjobs.add_choir(concert_id, self.lw_edit_choirs.item(i).text())
            # Insert dirigents into DB
            for i in range(self.lw_edit_dirigents.count()):
                self.dbjobs.add_dirigent(concert_id, self.lw_edit_dirigents.item(i).text())
            # Insert soloists and works into DB
            for i in range(self.tw_edit_works.invisibleRootItem().childCount()):
                item = self.tw_edit_works.invisibleRootItem().child(i)
                # Add work
                data = item.text(0).split(WORK_STR_SEPARATOR)
                work_id = self.dbjobs.add_work(concert_id, data[0], data[1])
                # Add soloists
                for j in range(item.childCount()):
                    self.dbjobs.add_soloist(concert_id, work_id, item.child(j).text(0))

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
    def on_btn_works_add_soloist_clicked(self):
        selected_items = self.tw_edit_works.selectedItems()
        if len(selected_items) > 0:
            d = DialogEditSub(self, soloists=True, caption=self.tr('Zadejte jméno sólistu'))
            if d.exec_() == QDialog.Accepted:
                item = QTreeWidgetItem()
                item.setText(0, d.dataSoloist)
                parent = selected_items[0].parent()
                if parent != None:
                    parent.addChild(item)
                else:
                    selected_items[0].addChild(item)
                self.tw_edit_works.expandAll()
        else:
            QMessageBox.warning(self, self.tr('Varování'), self.tr('Nebyla označena žádna skladba.'))

    @pyqtSlot()
    def on_btn_works_add_clicked(self):
        d = DialogEditSub(self, works=True, caption=self.tr('Zadejte jméno skladatele a název díla'))
        if d.exec_() == QDialog.Accepted:
            item = QTreeWidgetItem()
            item.setText(0, '{}{}{}'.format(d.dataComposer, WORK_STR_SEPARATOR, d.dataWork))
            self.tw_edit_works.invisibleRootItem().addChild(item)
            self.tw_edit_works.expandAll()

    @pyqtSlot()
    def on_btn_choirs_add_clicked(self):
        d = DialogEditSub(self, choirs=True, caption=self.tr('Zadejte název sboru'))
        if d.exec_() == QDialog.Accepted:
            self.lw_edit_choirs.addItem(d.dataChoir)

    @pyqtSlot()
    def on_btn_choirs_remove_clicked(self):
        if len(self.lw_edit_choirs.selectedItems()) > 0:
            self.lw_edit_choirs.takeItem(self.lw_edit_choirs.currentIndex().row())

    @pyqtSlot()
    def on_btn_dirigents_remove_clicked(self):
        if len(self.lw_edit_dirigents.selectedItems()) > 0:
            self.lw_edit_dirigents.takeItem(self.lw_edit_dirigents.currentIndex().row())

    @pyqtSlot()
    def on_btn_works_remove_clicked(self):
        selected_items = self.tw_edit_works.selectedItems()
        if len(selected_items) > 0:
            parent = selected_items[0].parent()
            if parent != None:
                parent.removeChild(selected_items[0])
            else:
                self.tw_edit_works.takeTopLevelItem(self.tw_edit_works.indexFromItem(selected_items[0]).row())

    @pyqtSlot()
    def on_actionSprava_festivalov_triggered(self):
        d = DialogFestivalsSub(self)
        d.exec_()
        self.refresh_festivals()

    def refresh_festivals(self):
        # Add festivals to combobox
        self.cb_festival.clear()
        self.cb_festival.addItem(self.tr('<Nepoužívat>'))
        festivals = self.dbjobs.get_all_festivals()
        for festival in festivals:
            self.cb_festival.addItem(festival[1], festival[0])

    @pyqtSlot()
    def on_actionOdstranit_triggered(self):
        """
        Removes the concert from database
        """
        selected_indexes = self.tableView.selectedIndexes()
        if len(selected_indexes) > 0:
            self.on_btn_edit_cancel_clicked()
            mb = QMessageBox.question(self, self.tr('Upozornení'), self.tr('Opravdu chcete vybraný koncert smazat?'))
            if mb == QMessageBox.Yes:
                concert_id = self.concerts_model.get_item_data(selected_indexes[0], COLUMN_CONCERT_ID)
                # Remove concert from database
                self.dbjobs.remove_concert(concert_id)
                # Remove dirigents assigned to this concert
                self.dbjobs.remove_dirigents_for_concert(concert_id)
                # Remove choirs assigned to this concert
                self.dbjobs.remove_choirs_for_concert(concert_id)
                # Remove works assigned to this concert
                self.dbjobs.remove_works_for_concert(concert_id)
                # Remove soloists assigned to this concert
                self.dbjobs.remove_soloists_for_concert(concert_id)
                self.concerts_model.removeRow(selected_indexes[0].row())
                self.statusbar.showMessage(self.tr('Záznam byl úspěšne odstráněn.'), TIMEOUT_INFO)
        else:
            QMessageBox.warning(self, self.tr('Varování'), self.tr('Nebyl vybrán žádnej koncert.'))

# End of Mainformsub.py
