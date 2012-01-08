#! /usr/bin/env python
# edit_window.py
# Go to this window when editing the flashcards
# STARTED: November 2, 2011

import wx
from card_set import FlashcardSet, Flashcard

class EditDialog(wx.Dialog):
    """A dialog window to change or delete a single flashcard"""
    def __init__(self, master, title, card):
        super(EditDialog, self).__init__(master, title=title, size=(300, 150),
              style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.edited_card = None
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        grid = wx.FlexGridSizer(rows=2, cols=2, vgap=10, hgap=10)
        
        front_label = wx.StaticText(self, label="Front:")
        back_label = wx.StaticText(self, label="Back:")
        self.front_entry = wx.TextCtrl(self, size=(150, -1))
        self.back_entry = wx.TextCtrl(self, size=(150, -1))
        
        self.front_entry.SetValue(card[0])
        self.back_entry.SetValue(card[1])
        
        buttons_box = wx.BoxSizer(wx.HORIZONTAL)
        finish_b = wx.Button(self, label="Finish")
        cancel_b = wx.Button(self, label="Cancel")
        delete_b = wx.Button(self, label="Delete")
        buttons_box.Add(finish_b, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        buttons_box.Add(delete_b, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        buttons_box.Add(cancel_b, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        
        grid.AddMany([(front_label), (self.front_entry), 
                      (back_label), (self.back_entry)])
        
        vbox.Add(grid, flag=wx.ALL, border=10)
        vbox.Add(buttons_box, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        
        finish_b.Bind(wx.EVT_BUTTON, handler=self.on_finish)
        cancel_b.Bind(wx.EVT_BUTTON, handler=self.on_cancel)
        delete_b.Bind(wx.EVT_BUTTON, handler=self.on_delete)
        
        self.SetSizer(vbox)

    def on_finish(self, event):
        self.edited_card = Flashcard(self.front_entry.GetValue(), 
                                self.back_entry.GetValue())
        self.EndModal(wx.ID_OK)
    
    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)
    
    def on_delete(self, event):
        self.EndModal(wx.ID_DELETE)
        
        
class ViewCardsWindow:
    """The window for editing the flashcards"""
    def __init__(self, master, flashcards):
        self.win = wx.Dialog(master, title="View Cards",
                             style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.cards = flashcards
        self.initUI()

    def initUI(self):
        """Draw the User Interface for the window"""
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.listbox = wx.ListCtrl(self.win, 
                        style=wx.LC_REPORT|wx.BORDER_SUNKEN|wx.LC_SINGLE_SEL)
        self.listbox.InsertColumn(0, "Front")
        self.listbox.InsertColumn(1, "Back")
        self.listbox.InsertColumn(2, "Correct")
        self.listbox.InsertColumn(3, "Incorrect")
        self.listbox.InsertColumn(4, "Percentage")
        
        index = 0
        self.data_d = {}
        for card in self.cards:
            self.listbox.InsertStringItem(index, card[0])
            self.listbox.SetStringItem(index, 1, card[1])
            self.listbox.SetStringItem(index, 2, str(card.correct))
            self.listbox.SetStringItem(index, 3, str(card.incorrect))
            self.listbox.SetStringItem(index, 4, "%.1f%%" % (card.percentage()))
            self.listbox.SetItemData(index, id(card))
            self.data_d[id(card)] = card
            index += 1
        
        self.listbox.SetColumnWidth(col=0, width=wx.LIST_AUTOSIZE)
        self.listbox.SetColumnWidth(col=1, width=wx.LIST_AUTOSIZE)
        for i in range(2, 5):
            self.listbox.SetColumnWidth(col=i, width=wx.LIST_AUTOSIZE_USEHEADER)
        
        self.listbox.Bind(wx.EVT_LIST_ITEM_ACTIVATED, handler=self.edit_cards)
        
        vbox.Add(self.listbox, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        self.win.SetSizer(vbox)
        self.win.Show()

    def edit_cards(self, event):
        """Called when a listCtrl item in double-clicked. Displays a dialog
        for editing and deleting cards"""
        index = event.m_itemIndex
        the_card = self.data_d[self.listbox.GetItemData(index)]
        edit_win = EditDialog(self.win, title="Edit Cards", card=the_card)
        show_id = edit_win.ShowModal()
        if show_id == wx.ID_OK:
            new_card = edit_win.edited_card
            card_index = self.cards.cards.index(the_card)
            del self.cards[card_index]
            self.cards.cards.insert(card_index, new_card)
            
            self.listbox.DeleteItem(index)
            self.listbox.InsertStringItem(index, new_card[0])
            self.listbox.SetStringItem(index, 1, new_card[1])
            self.listbox.SetStringItem(index, 2, '0')
            self.listbox.SetStringItem(index, 3, '0')
            self.listbox.SetStringItem(index, 4, '0.0%')
            print self.cards
            
        elif show_id == wx.ID_DELETE:
            del_message = "Are you sure you want to delete this card?"
            confirm_delete = wx.MessageDialog(self.win, message=del_message,
                                              caption="Delete Card?",
                                              style=wx.YES_NO|wx.YES_DEFAULT)
            if confirm_delete.ShowModal() == wx.ID_YES:
                card_i = self.cards.cards.index(the_card)
                del self.cards[card_i]
                self.listbox.DeleteItem(index)
                print self.cards

if __name__ == "__main__":
    app = wx.App()
    f = wx.Frame(None)
    f.Show()
    test_cards = FlashcardSet()
    test_cards.add("Hello", "World")
    test_cards.add("Python", "Tkinter")
    test_cards.add("Flashcards", "App")
    test_cards.add("The Zen", "Of Python") 
    view_win = ViewCardsWindow(f, test_cards)
    app.MainLoop()

        
        
