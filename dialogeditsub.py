#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from dialogedit import Ui_DialogEdit


class DialogEditSub(QDialog, Ui_DialogEdit):
    """
    Dialog to add new group
    """
    def __init__(self, dirigents=False, works=False, soloists=False, caption=''):
        super(QDialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(caption)
        # Variables
        self.dataComposer = ''
        self.dataDirigent = ''
        self.dataSoloist = ''
        self.dataWork = ''
        # Set type of dialog
        self.typeDirigents = dirigents
        self.typeWorks = works
        self.typeSoloists = soloists
        # Show/hide widgets
        self.frame_dirigent.setVisible(dirigents)
        self.frame_works.setVisible(works)
        self.frame_soloists.setVisible(soloists)
        # Clear text edits
        self.edit_soloist.clear()
        self.edit_dirigent.clear()
        self.edit_composer.clear()
        self.edit_work.clear()
        self.adjustSize()

    def accept(self):
        # Handle input data
        if self.typeDirigents:
            self.dataDirigent = self.edit_dirigent.text().strip()
        elif self.typeSoloists:
            self.dataSoloist = self.edit_soloist.text().strip()
        elif self.typeWorks:
            self.dataComposer = self.edit_composer.text().strip()
            self.dataWork = self.edit_work.text().strip()
        # Check input data
        if (len(self.dataDirigent) != 0) or (len(self.dataSoloist) != 0) or ((len(self.dataComposer) != 0) and (len(self.dataWork) != 0)):
            QDialog.accept(self)
        else:
            QMessageBox.warning(self, self.tr('Varování'), self.tr('Nesprávne vyplnené údaje.'))

# End of dialogeditsub.py