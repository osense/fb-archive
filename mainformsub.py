# -*- coding: utf-8 -*-

## This file is part of fb-archive.

## fb-archive is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.

## fb-archive is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with fb-archive.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from mainform import *
import dbjobs
import os
import sys
from dialogeditsub import DialogEditSub
from dialogaboutsub import DialogAboutSub
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
        self.resize(800, 650)
        self.show_all_concerts()
        self.frame_search.adjustSize()
        self.frame.adjustSize()
        # Variables
        self.now_edited_concert_id = None

    ### MAIN FUNCTIONS ##############################################################################################################################

    def prepare_gui(self):
        # Hide not needed widgets
        self.frame_edit.hide()
        self.frame_search.adjustSize()
        # Create auto completer
        self.completer = QCompleter()
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
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
                      self.tr('Festival'), self.tr('Skladatel, skladba'), self.tr('Sólisti'), self.tr('Dirigenti'), self.tr('Sbory'), self.tr('Poznámka'), ]
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
        # Clear search section
        self.btn_clear_widgets.click()
        self.btn_clear_criteria.click()
        self.refresh_festivals()

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
            self.completer_model.sort(0)

    def closeEvent(self, ce):
        """
        Close database
        """
        ce.accept()
        self.dbjobs.close()

    ### SEARCH FUNCTIONS ############################################################################################################################

    @pyqtSlot()
    def on_btn_search_clicked(self):
        search_parameters = {}
        # Add parameters to dict
        if self.check_date.isChecked():
            dt_from = self.edit_s_date_from.dateTime()
            search_parameters['date_from'] = datetime.datetime(dt_from.date().year(), dt_from.date().month(), dt_from.date().day(), 0, 0, 0)
            dt_to = self.edit_s_date_to.dateTime()
            search_parameters['date_to'] = datetime.datetime(dt_to.date().year(), dt_to.date().month(), dt_to.date().day(), 23, 59, 59)
        if self.check_name.isChecked():
            search_parameters['name'] = self.edit_s_name.text().rstrip()
        if self.check_state.isChecked():
            search_parameters['state'] = self.edit_s_state.text().rstrip()
        if self.check_city.isChecked():
            search_parameters['city'] = self.edit_s_city.text().rstrip()
        if self.check_hall.isChecked():
            search_parameters['hall'] = self.edit_s_hall.text().rstrip()
        if self.check_type.isChecked():
            search_parameters['type'] = self.edit_s_type.text().rstrip()
        if self.check_festival.isChecked():
            search_parameters['festival'] = self.cb_s_festival.itemData(self.cb_s_festival.currentIndex(), Qt.UserRole)
        if self.check_composer.isChecked():
            search_parameters['composer'] = self.edit_s_composer.text().rstrip()
        if self.check_work.isChecked():
            search_parameters['work'] = self.edit_s_work.text().rstrip()
        if self.check_soloist.isChecked():
            search_parameters['soloist'] = self.edit_s_soloist.text().rstrip()
        if self.check_dirigent.isChecked():
            search_parameters['dirigent'] = self.edit_s_dirigent.text().rstrip()
        if self.check_choir.isChecked():
            search_parameters['choir'] = self.edit_s_choir.text().rstrip()
        if self.check_note.isChecked():
            search_parameters['note'] = self.edit_s_note.text().rstrip()
        # Db function
        data = self.dbjobs.universal_search(search_parameters)
        # Show data in tableview
        self.show_selected_concerts(data)

    def show_all_concerts(self):
        """
        Shows all concerts from the database in tableview
        """
        data = self.dbjobs.get_all_concerts()
        self.show_selected_concerts(data)

    def show_selected_concerts(self, data):
        """
        Inserts selected concerts from db to tableview
        """
        self.concerts_model.beginResetModel()
        self.concerts_model.clear()
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
            # works
            works = self.dbjobs.get_works(concert_id)
            joined_works = []
            for work in works:
                joined_works.append(WORK_STR_SEPARATOR.join(work[1:]))
            works = ', '.join(joined_works)
            dirigents = ', '.join([i[1] for i in self.dbjobs.get_dirigents(concert_id)])
            choirs = ', '.join([i[1] for i in self.dbjobs.get_choirs(concert_id)])
            soloists = ', '.join([i[0] for i in self.dbjobs.get_soloists_for_concert(concert_id)])
            new_row = [date_from, date_to, name, state, city, hall, type, festival, works, soloists, dirigents, choirs, note, concert_id, festival_id]
            self.concerts_model.addRow(new_row)
        self.concerts_model.endResetModel()

    ### ADD and EDIT FUNCTIONS ######################################################################################################################

    @pyqtSlot()
    def on_btn_edit_cancel_clicked(self):
        self.frame_edit.hide()
        self.frame_search.show()
        self.clear_widgets()
        self.now_edited_concert_id = None

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
            index = self.sort_proxy_model.mapToSource(selected_indexes[0])
            self.clear_widgets()
            self.frame_search.hide()
            self.frame_edit.show()
            # Add festivals to combobox
            self.refresh_festivals()
            # Show / Hide unused buttons
            self.btn_edit_confirm.hide()
            self.btn_edit_save.show()
            # Load data to widgets
            self.now_edited_concert_id = self.concerts_model.get_item_data(index, COLUMN_CONCERT_ID)
            self.edit_name.setText(self.concerts_model.get_item_data(index, COLUMN_NAME))
            self.edit_date_from.setDateTime(self.concerts_model.get_item_data(index, COLUMN_DATE_FROM))
            self.edit_date_to.setDateTime(self.concerts_model.get_item_data(index, COLUMN_DATE_TO))
            self.edit_state.setText(self.concerts_model.get_item_data(index, COLUMN_STATE))
            self.edit_city.setText(self.concerts_model.get_item_data(index, COLUMN_CITY))
            self.edit_hall.setText(self.concerts_model.get_item_data(index, COLUMN_HALL))
            self.edit_type.setText(self.concerts_model.get_item_data(index, COLUMN_TYPE))
            self.cb_festival.setCurrentIndex(self.cb_festival.findData(self.concerts_model.get_item_data(index, COLUMN_FESTIVAL_ID)))
            self.edit_note.setText(self.concerts_model.get_item_data(index, COLUMN_NOTE))
            # choir
            choirs = self.dbjobs.get_choirs(self.now_edited_concert_id)
            for choir in choirs:
                item = QListWidgetItem()
                item.setText(choir[1])
                item.setData(Qt.UserRole, choir[0])
                self.lw_edit_choirs.addItem(item)
            # dirigents
            dirigents = self.dbjobs.get_dirigents(self.now_edited_concert_id)
            for dirigent in dirigents:
                item = QListWidgetItem()
                item.setText(dirigent[1])
                item.setData(Qt.UserRole, dirigent[0])
                self.lw_edit_dirigents.addItem(item)
            # soloists and works
            works = self.dbjobs.get_works(self.now_edited_concert_id)
            for work in works:
                work_item = QTreeWidgetItem()
                work_item.setText(0, '{}{}{}'.format(work[1], WORK_STR_SEPARATOR, work[2]))
                work_item.setData(0, Qt.UserRole, work[0])
                soloists = self.dbjobs.get_soloists_for_work(work[0])
                for soloist in soloists:
                    soloist_item = QTreeWidgetItem()
                    soloist_item.setText(0, soloist[1])
                    soloist_item.setData(0, Qt.UserRole, soloist[0])
                    work_item.addChild(soloist_item)
                self.tw_edit_works.invisibleRootItem().addChild(work_item)
            self.tw_edit_works.expandAll()
        else:
            QMessageBox.warning(self, self.tr('Varování'), self.tr('Nebyl vybrán žádný koncert.'))

    @pyqtSlot()
    def on_btn_edit_confirm_clicked(self):
        dt_from = self.edit_date_from.dateTime()
        date_from = datetime.datetime(dt_from.date().year(), dt_from.date().month(), dt_from.date().day(), 12, 0)
        dt_to = self.edit_date_to.dateTime()
        date_to = datetime.datetime(dt_to.date().year(), dt_to.date().month(), dt_to.date().day(), 12, 0)
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
            # Show message
            self.statusbar.showMessage(self.tr('Záznam byl úspěšne přidán.'), TIMEOUT_INFO)
            self.on_btn_edit_cancel_clicked()
            self.show_all_concerts()
        except:
            print(sys.exc_info())
            self.statusbar.showMessage(self.tr('Záznam se nepodařilo přidat!'), TIMEOUT_ERROR)

    @pyqtSlot()
    def on_btn_edit_save_clicked(self):
        """
        Update details for concert
        """
        try:
            dt_from = self.edit_date_from.dateTime()
            date_from = datetime.datetime(dt_from.date().year(), dt_from.date().month(), dt_from.date().day(), 12, 0)
            dt_to = self.edit_date_to.dateTime()
            date_to = datetime.datetime(dt_to.date().year(), dt_to.date().month(), dt_to.date().day(), 12, 0)
            name = self.edit_name.text().strip()
            state = self.edit_state.text().strip()
            city = self.edit_city.text().strip()
            hall = self.edit_hall.text().strip()
            type = self.edit_type.text().strip()
            festival_id = self.cb_festival.itemData(self.cb_festival.currentIndex(), Qt.UserRole)
            note = self.edit_note.toPlainText().strip() or None
            # DB part
            self.dbjobs.update_concert(self.now_edited_concert_id, name, festival_id, date_from, date_to, state, city, hall, type, note)
            # Dirigents - remove all dirigents for concert
            self.dbjobs.remove_dirigents_for_concert(self.now_edited_concert_id)
            # Dirigents - add all dirigents from widget
            for i in range(self.lw_edit_dirigents.count()):
                self.dbjobs.add_dirigent(self.now_edited_concert_id, self.lw_edit_dirigents.item(i).text())
            # Choirs - remove all choirs for concert
            self.dbjobs.remove_choirs_for_concert(self.now_edited_concert_id)
            # Choirs - add all choirs from widget
            for i in range(self.lw_edit_choirs.count()):
                self.dbjobs.add_choir(self.now_edited_concert_id, self.lw_edit_choirs.item(i).text())
            # Remove soloists and works for concert
            self.dbjobs.remove_soloists_for_concert(self.now_edited_concert_id)
            self.dbjobs.remove_works_for_concert(self.now_edited_concert_id)
            # Insert soloists and works into DB
            for i in range(self.tw_edit_works.invisibleRootItem().childCount()):
                item = self.tw_edit_works.invisibleRootItem().child(i)
                # Add work
                data = item.text(0).split(WORK_STR_SEPARATOR)
                work_id = self.dbjobs.add_work(self.now_edited_concert_id, data[0], data[1])
                # Add soloists
                for j in range(item.childCount()):
                    self.dbjobs.add_soloist(self.now_edited_concert_id, work_id, item.child(j).text(0))
            # Show info
            self.statusbar.showMessage(self.tr('Záznam byl úspěšne upraven.'), TIMEOUT_INFO)
            self.on_btn_edit_cancel_clicked()
            self.show_all_concerts()
        except:
            print(sys.exc_info())
            self.statusbar.showMessage(self.tr('Záznam se nepodařilo upravit!'), TIMEOUT_ERROR)

    @pyqtSlot()
    def on_btn_dirigents_add_clicked(self):
        # Stringlist for completion
        stringlist = []
        for i in range(self.lw_edit_dirigents.count()):
            stringlist.append(self.lw_edit_dirigents.item(i).text())
        # Dialog
        d = DialogEditSub(self, stringlist, dirigents=True, caption=self.tr('Zadejte jméno dirigenta'))
        if d.exec_() == QDialog.Accepted:
            item = QListWidgetItem()
            item.setText(d.dataDirigent)
            self.lw_edit_dirigents.addItem(item)
            self.lw_edit_dirigents.scrollToItem(item, QAbstractItemView.EnsureVisible)
            self.lw_edit_dirigents.selectionModel().setCurrentIndex(self.lw_edit_dirigents.indexFromItem(item), QItemSelectionModel.ClearAndSelect)
            self.lw_edit_dirigents.sortItems()

    @pyqtSlot()
    def on_btn_works_add_soloist_clicked(self):
        selected_items = self.tw_edit_works.selectedItems()
        if len(selected_items) > 0:
            # Stringlist for completion
            stringlist = []
            for i in range(self.tw_edit_works.invisibleRootItem().childCount()):
                item = self.tw_edit_works.invisibleRootItem().child(i)
                for j in range(item.childCount()):
                    stringlist.append(item.child(j).text(0))
            # Dialog
            d = DialogEditSub(self, stringlist, soloists=True, caption=self.tr('Zadejte jméno sólisty'))
            if d.exec_() == QDialog.Accepted:
                item = QTreeWidgetItem()
                item.setText(0, d.dataSoloist)
                parent = selected_items[0].parent()
                if parent != None:
                    parent.addChild(item)
                    parent.sortChildren(0, Qt.AscendingOrder)
                else:
                    selected_items[0].addChild(item)
                    selected_items[0].sortChildren(0, Qt.AscendingOrder)
                self.tw_edit_works.expandAll()
                self.tw_edit_works.scrollToItem(item, QAbstractItemView.EnsureVisible)
        else:
            QMessageBox.warning(self, self.tr('Varování'), self.tr('Nebyla označena žádná skladba.'))

    @pyqtSlot()
    def on_btn_works_add_clicked(self):
        # Stringlist for completion
        stringlist = []
        for i in range(self.tw_edit_works.invisibleRootItem().childCount()):
            item = self.tw_edit_works.invisibleRootItem().child(i)
            stringlist.append(item.text(0))
        # Dialog
        d = DialogEditSub(self, stringlist, works=True, caption=self.tr('Zadejte jméno skladatele a název díla'))
        if d.exec_() == QDialog.Accepted:
            item = QTreeWidgetItem()
            item.setText(0, '{}{}{}'.format(d.dataComposer, WORK_STR_SEPARATOR, d.dataWork))
            self.tw_edit_works.invisibleRootItem().addChild(item)
            self.tw_edit_works.expandAll()
            self.tw_edit_works.scrollToItem(item, QAbstractItemView.EnsureVisible)
            self.tw_edit_works.selectionModel().setCurrentIndex(self.tw_edit_works.indexFromItem(item), QItemSelectionModel.ClearAndSelect)
            self.tw_edit_works.sortItems(0, Qt.AscendingOrder)

    @pyqtSlot()
    def on_btn_choirs_add_clicked(self):
        # Stringlist for completion
        stringlist = []
        for i in range(self.lw_edit_choirs.count()):
            stringlist.append(self.lw_edit_choirs.item(i).text())
        # Dialog
        d = DialogEditSub(self, stringlist, choirs=True, caption=self.tr('Zadejte název sboru'))
        if d.exec_() == QDialog.Accepted:
            item = QListWidgetItem()
            item.setText(d.dataChoir)
            self.lw_edit_choirs.addItem(item)
            self.lw_edit_choirs.scrollToItem(item, QAbstractItemView.EnsureVisible)
            self.lw_edit_choirs.selectionModel().setCurrentIndex(self.lw_edit_choirs.indexFromItem(item), QItemSelectionModel.ClearAndSelect)
            self.lw_edit_choirs.sortItems()

    @pyqtSlot()
    def on_btn_choirs_remove_clicked(self):
        selected_items = self.lw_edit_choirs.selectedItems()
        if len(selected_items) > 0:
            self.lw_edit_choirs.takeItem(self.lw_edit_choirs.currentIndex().row())

    @pyqtSlot()
    def on_btn_dirigents_remove_clicked(self):
        selected_items = self.lw_edit_dirigents.selectedItems()
        if len(selected_items) > 0:
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
        self.cb_s_festival.clear()
        self.cb_festival.addItem(self.tr('<Žádný>'))
        self.cb_s_festival.addItem(self.tr('<Žádný>'))
        festivals = self.dbjobs.get_all_festivals()
        for festival in festivals:
            self.cb_festival.addItem(festival[1], festival[0])
            self.cb_s_festival.addItem(festival[1], festival[0])

    @pyqtSlot()
    def on_actionOdstranit_triggered(self):
        """
        Removes the concert from database
        """
        selected_indexes = self.tableView.selectedIndexes()
        if len(selected_indexes) > 0:
            index = self.sort_proxy_model.mapToSource(selected_indexes[0])
            self.on_btn_edit_cancel_clicked()
            mb = QMessageBox.question(self, self.tr('Upozornení'), self.tr('Opravdu chcete vybraný koncert smazat?'))
            if mb == QMessageBox.Yes:
                concert_id = self.concerts_model.get_item_data(index, COLUMN_CONCERT_ID)
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
                self.concerts_model.removeRow(index.row())
                self.statusbar.showMessage(self.tr('Záznam byl úspěšne odstraněn.'), TIMEOUT_INFO)
        else:
            QMessageBox.warning(self, self.tr('Varování'), self.tr('Nebyl vybrán žádný koncert.'))

    @pyqtSlot()
    def on_actionO_programe_triggered(self):
        d = DialogAboutSub(self)
        d.exec_()

    @pyqtSlot()
    def on_btn_clear_widgets_clicked(self):
        """
        Clears all search widgets
        """
        self.edit_s_date_from.setDateTime(datetime.datetime.today())
        self.edit_s_date_to.setDateTime(datetime.datetime.today())
        self.cb_s_festival.setCurrentIndex(self.cb_s_festival.findData(None))

    ### SEARCH EDITS BEHAVIOR #######################################################################################################################

    @pyqtSlot("QString")
    def on_edit_s_name_textEdited(self, text):
        self.check_name.setChecked(text != '')

    @pyqtSlot("QString")
    def on_edit_s_state_textEdited(self, text):
        self.check_state.setChecked(text != '')

    @pyqtSlot("QString")
    def on_edit_s_city_textEdited(self, text):
        self.check_city.setChecked(text != '')

    @pyqtSlot("QString")
    def on_edit_s_hall_textEdited(self, text):
        self.check_hall.setChecked(text != '')

    @pyqtSlot("QString")
    def on_edit_s_type_textEdited(self, text):
        self.check_type.setChecked(text != '')

    @pyqtSlot("QString")
    def on_edit_s_composer_textEdited(self, text):
        self.check_composer.setChecked(text != '')

    @pyqtSlot("QString")
    def on_edit_s_work_textEdited(self, text):
        self.check_work.setChecked(text != '')

    @pyqtSlot("QString")
    def on_edit_s_soloist_textEdited(self, text):
        self.check_soloist.setChecked(text != '')

    @pyqtSlot("QString")
    def on_edit_s_dirigent_textEdited(self, text):
        self.check_dirigent.setChecked(text != '')

    @pyqtSlot("QString")
    def on_edit_s_choir_textEdited(self, text):
        self.check_choir.setChecked(text != '')

    @pyqtSlot("QString")
    def on_edit_s_note_textEdited(self, text):
        self.check_note.setChecked(text != '')

    @pyqtSlot("QDate")
    def on_edit_s_date_from_dateChanged(self, date):
        self.check_date.setChecked(True)
        if self.edit_s_date_from.dateTime() > self.edit_s_date_to.dateTime():
            self.edit_s_date_to.setDateTime(self.edit_s_date_from.dateTime())

    @pyqtSlot("QDate")
    def on_edit_s_date_to_dateChanged(self, date):
        self.check_date.setChecked(True)
        if self.edit_s_date_to.dateTime() < self.edit_s_date_from.dateTime():
            self.edit_s_date_from.setDateTime(self.edit_s_date_to.dateTime())

    @pyqtSlot("QDate")
    def on_edit_date_from_dateChanged(self, date):
        if self.edit_date_from.dateTime() > self.edit_date_to.dateTime():
            self.edit_date_to.setDateTime(self.edit_date_from.dateTime())

    @pyqtSlot("QDate")
    def on_edit_date_to_dateChanged(self, date):
        if self.edit_date_to.dateTime() < self.edit_date_from.dateTime():
            self.edit_date_from.setDateTime(self.edit_date_to.dateTime())

    @pyqtSlot("int")
    def on_cb_s_festival_currentIndexChanged(self, index):
        self.check_festival.setChecked(index != 0)

# End of Mainformsub.py
