#!/usr/bin/env python
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
from dialogedit import Ui_DialogEdit
from constants import *


class DialogEditSub(QDialog, Ui_DialogEdit):
    """
    Dialog to add new group
    """
    def __init__(self, parent, view_stringlist=None, dirigents=False, works=False, soloists=False, festivals=False, choirs=False, caption=''):
        super(QDialog, self).__init__()
        self.parent = parent
        self.view_stringlist = view_stringlist
        self.setupUi(self)
        self.setWindowTitle(caption)
        # Variables
        self.dataComposer = ''
        self.dataDirigent = ''
        self.dataSoloist = ''
        self.dataWork = ''
        self.dataFestival = ''
        self.dataChoir = ''
        # Set type of dialog
        self.typeDirigents = dirigents
        self.typeWorks = works
        self.typeSoloists = soloists
        self.typeFestivals = festivals
        self.typeChoirs = choirs
        # Show/hide widgets
        self.frame_dirigent.setVisible(dirigents)
        self.frame_works.setVisible(works)
        self.frame_soloists.setVisible(soloists)
        self.frame_festivals.setVisible(festivals)
        self.frame_choirs.setVisible(choirs)
        # Clear text edits
        self.edit_soloist.clear()
        self.edit_dirigent.clear()
        self.edit_composer.clear()
        self.edit_work.clear()
        self.edit_choir.clear()
        self.adjustSize()
        # Create auto completer
        self.completer = QCompleter()
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer_model = QStringListModel()
        self.completer.setModel(self.completer_model)
        # Completion database functions connected with particular widgets
        self.completion_dict = {self.edit_composer: {'db_func': self.parent.dbjobs.get_completion_for_composer},
                                self.edit_work: {'db_func': self.parent.dbjobs.get_completion_for_work},
                                self.edit_dirigent: {'db_func': self.parent.dbjobs.get_completion_for_dirigent},
                                self.edit_soloist: {'db_func': self.parent.dbjobs.get_completion_for_soloist},
                                self.edit_festival: {'db_func': self.parent.dbjobs.get_completion_for_festival},
                                self.edit_choir: {'db_func': self.parent.dbjobs.get_completion_for_choir}, }
        # Set auto completer for widgets
        self.edit_composer.setCompleter(self.completer)
        self.edit_work.setCompleter(self.completer)
        self.edit_dirigent.setCompleter(self.completer)
        self.edit_soloist.setCompleter(self.completer)
        self.edit_festival.setCompleter(self.completer)
        self.edit_choir.setCompleter(self.completer)
        # Connect widgets to completer function
        self.edit_composer.textEdited.connect(self.getCompleterData)
        self.edit_work.textEdited.connect(self.getCompleterData)
        self.edit_dirigent.textEdited.connect(self.getCompleterData)
        self.edit_soloist.textEdited.connect(self.getCompleterData)
        self.edit_festival.textEdited.connect(self.getCompleterData)
        self.edit_choir.textEdited.connect(self.getCompleterData)

    def getCompleterData(self, text):
        """
        Shows expressions for completion due to edit type
        """
        lineedit = self.sender()
        stringlist = []
        # Add strings from database
        data = self.completion_dict[lineedit]['db_func'](text)
        if data != None:
            for item in data:
                stringlist += item
            if len(stringlist) == 7:
                stringlist[6] = '...'
        # Add string already added to parent view object
        if self.view_stringlist != None:
            if self.typeWorks:
                newlist = []
                column = 0 if lineedit == self.edit_composer else 1
                for record in self.view_stringlist:
                    newlist.append(record.split(WORK_STR_SEPARATOR)[column])
                stringlist += newlist
            else:
                stringlist += self.view_stringlist
        # Remove duplicates
        stringlist = list(set(stringlist))
        # Set string list for completter
        self.completer_model.setStringList(stringlist)
        self.completer_model.sort(0)

    def accept(self):
        # Handle input data
        if self.typeDirigents:
            self.dataDirigent = self.edit_dirigent.text().strip()
        elif self.typeSoloists:
            self.dataSoloist = self.edit_soloist.text().strip()
        elif self.typeWorks:
            self.dataComposer = self.edit_composer.text().strip()
            self.dataWork = self.edit_work.text().strip()
        elif self.typeFestivals:
            self.dataFestival = self.edit_festival.text().strip()
        elif self.typeChoirs:
            self.dataChoir = self.edit_choir.text().strip()
        # Check input data
        if (len(self.dataDirigent) != 0) or (len(self.dataSoloist) != 0) or ((len(self.dataComposer) != 0) and (len(self.dataWork) != 0)) or (len(self.dataFestival) != 0) or (len(self.dataChoir) != 0):
            QDialog.accept(self)
        else:
            QMessageBox.warning(self, self.tr('Varování'), self.tr('Nesprávně vyplněné údaje.'))

# End of dialogeditsub.py
