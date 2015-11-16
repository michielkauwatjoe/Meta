# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    Wayfinding appication.
#    Copyright (c) 2014+ www.michielkauwatjoe.com
#
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    dialogs.py
#

from vanilla import Window, TextBox, Button, EditText, ComboBox
from AppKit import NSOKButton, NSOpenPanel

from meta.papersizes import PaperSizes

class Dialogs(object):
    u"""
    New dialog creation, for dialog closing see Callbacks class.
    """

    # Start.

    def openStartWindow(self):
        u"""
        Offers a 'New' and 'Open...' button.
        """
        self.startDialog = Window(self.dialogSize, "Welcome", minSize=self.dialogSize, maxSize=self.dialogSize)
        self.startDialog.newText = TextBox((20, 60, 60, 30), "New")
        self.startDialog.newButton = Button((20, 100, 80, 20), "Create...", callback=self.new_)
        self.startDialog.openText = TextBox((160, 60, 60, 30), "Existing")
        self.startDialog.openButton = Button((160, 100, 60, 20), "Open...", callback=self.open_)
        self.startDialog.open()

    def closeStartDialog(self):
        u"""
        Closes and clears start dialog.
        """
        if not self.startDialog is None:
            self.startDialog.close()
            self.startDialog = None

    # Document.

    def openOpenDocumentDialog(self):
        u"""
        Open document dialog.
        """
        self.closeStartDialog()

        panel = NSOpenPanel.openPanel()
        panel.setCanChooseDirectories_(False)
        panel.setCanChooseFiles_(True)
        panel.setAllowsMultipleSelection_(False)
        panel.setAllowedFileTypes_(['wf'])

        if panel.runModal() == NSOKButton:
            added, document = self.model.openDocument(panel.filenames()[0])
            self.initDocument(added, document)

    def openNewDialog(self):
        u"""
        Opens the document canvas if it doesn't exist yet.
        """
        self.closeStartDialog()
        self.setDefaultDocumentValues()

        size = (400, 300)
        self.newDialog = w = Window(size, "New Document", minSize=size, maxSize=size)

        w.nameText = TextBox((20, 20, 180, 20), "Name")
        w.nameBox = EditText((200, 20, 180, 20), callback=self.newNameCallback)
        w.nameBox.set(self.documentValues['documentName'])

        w.sizeText = TextBox((20, 40, 180, 20), "Size")
        values = PaperSizes.getAllPaperSizes()
        w.sizeComboBox = ComboBox((200, 40, 180, 20), values, callback=self.newSizeCallback)
        w.sizeComboBox.set(self.defaultPaperSize)

        w.whText = TextBox((20, 60, 220, 20), u"w×h in ㎜")

        width, height = PaperSizes.getSize(self.defaultPaperSize, 'mm')

        w.width = EditText((200, 60, 80, 20), callback=self.newWidthCallback)
        w.width.set(width)

        w.x = TextBox((285, 60, 10, 20), u"×")
        w.dimensionBoxHeight = EditText((300, 60, 80, 20), callback=self.newHeightCallback)
        w.dimensionBoxHeight.set(height)

        w.okayButton = Button((240, 260, 60, 20), "Okay", callback=self.newOkayCallback)
        #w.okayButton.getNSButton().setEnabled_(False)
        w.cancelButton = Button((320, 260, 60, 20), "Cancel",
                callback=self.newCancelCallback)
        w.open()

    def closeOpenDialog(self):
        if not self.openDialog is None:
            self.openDialog.close()
            self.openDialog = None

    # Save dialog.

    def openSaveDialog(self):
        if not self.saveDialog is None:
            return

        self.saveDialog = Window(self.saveDialogSize, "Save", minSize=self.saveDialogSize,
                                    maxSize=self.saveDialogSize)
        self.saveDialog.saveText = TextBox((60, 20, 280, 60),
                "Save changes to the document %s?" % self.currentDocument.name)

        self.saveDialog.dontButton = Button((60, 70, 100, 20), "Don't Save",
                callback=self.saveDontCallback)

        self.saveDialog.cancelButton = Button((260, 70, 60, 20), "Cancel",
                callback=self.saveCloseCallback)

        self.saveDialog.doButton = Button((320, 70, 60, 20), "Save",
            callback=self.saveDoCallback)
        self.saveDialog.open()

    def closeSaveDialog(self):
        self.saveDocumentDialog.close()
        self.saveDocumentDialog = None

    # Close.

    def windowShouldCloseCallback(self, sender):
        window = self.getCurrentWindow()

        if sender == window:
            self.closeDocument_(sender)
