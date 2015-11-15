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
        self.startDialog.newButton = Button((20, 100, 80, 20), "Create...", callback=self.newDocument_)
        self.startDialog.openText = TextBox((160, 60, 60, 30), "Existing")
        self.startDialog.openButton = Button((160, 100, 60, 20), "Open...", callback=self.openDocument_)
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

    def openNewDocumentDialog(self):
        u"""
        Opens the document canvas if it doesn't exist yet.
        """
        self.closeStartDialog()
        self.setDefaultDocumentValues()

        size = (400, 300)
        self.newDocumentDialog = w = Window(size, "New Document", minSize=size, maxSize=size)

        w.nameText = TextBox((20, 20, 180, 20), "Name")
        w.nameBox = EditText((200, 20, 180, 20), callback=self.newDocumentNameCallback)
        w.nameBox.set(self.documentValues['documentName'])

        w.sizeText = TextBox((20, 40, 180, 20), "Size")
        values = PaperSizes.getAllPaperSizes()
        w.sizeComboBox = ComboBox((200, 40, 180, 20), values, callback=self.newDocumentSizeCallback)
        w.sizeComboBox.set(self.defaultPaperSize)

        '''
        w.dimensionsText = TextBox((20, 220, 220, 30), u"Dimensions (w×h in ㎝)")
        w.dimensionBoxWidth = EditText((200, 220, 80, 30), callback=self.newDocumentWidthCallback)
        w.dimensionBoxWidth.set(self.documentValues['documentWidth'])
        w.dimensionsX = TextBox((285, 220, 10, 30), u"×")
        w.dimensionBoxHeight = EditText((300, 220, 80, 30), callback=self.newDocumentHeightCallback)
        w.dimensionBoxHeight.set(self.documentValues['documentHeight'])
        '''

        w.okayButton = Button((240, 560, 60, 20), "Okay", callback=self.newDocumentOkayCallback)
        w.okayButton.getNSButton().setEnabled_(False)
        w.cancelButton = Button((320, 560, 60, 20), "Cancel",
                callback=self.newDocumentCancelCallback)
        w.open()

    def openSaveDocumentDialog(self):
        if not self.saveDocumentDialog is None:
            return

        self.saveDocumentDialog = Window(self.saveDialogSize, "Save", minSize=self.saveDialogSize,
                                    maxSize=self.saveDialogSize)
        self.saveDocumentDialog.saveText = TextBox((60, 20, 280, 60),
                "Save changes to the document %s?" % self.currentDocument.name)

        self.saveDocumentDialog.dontButton = Button((60, 70, 100, 20), "Don't Save",
                callback=self.saveDocumentDontCallback)

        self.saveDocumentDialog.cancelButton = Button((260, 70, 60, 20), "Cancel",
                callback=self.saveDocumentCloseCallback)

        self.saveDocumentDialog.doButton = Button((320, 70, 60, 20), "Save",
            callback=self.saveDocumentDoCallback)
        self.saveDocumentDialog.open()

    def windowShouldCloseCallback(self, sender):
        if sender == self.addDestinationDialog:
            self.addDestinationDialog.close()
            self.addDestinationDialog = None
        else:
            window = self.getCurrentWindow()

            if sender == window:
                self.closeDocument_(sender)
