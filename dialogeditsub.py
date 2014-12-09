#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from dialogedit import Ui_DialogEdit


class DialogEditSub(QDialog, Ui_DialogEdit):
    """
    Dialog to add new group
    """
    def __init__(self, parent, dirigents=False, works=False, soloists=False, festivals=False, choirs=False, caption=''):
        super(QDialog, self).__init__()
        self.parent = parent
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
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
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
        data = self.completion_dict[lineedit]['db_func'](text)
        stringlist = []
        if data != None:
            for item in data:
                stringlist += item
            if len(stringlist) == 7:
                stringlist[6] = '...'
            self.completer_model.setStringList(stringlist)

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
