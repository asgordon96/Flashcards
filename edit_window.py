#! usr/bin/env python
# edit_window.py
# Go to this window when editing the flashcards
# STARTED: November 2, 2011

import wx
from card_set import FlashcardSet

class EditWindow:
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
            
#        right_panel = Frame(self.win)
#        top_frame = Frame(right_panel)
#        bot_frame = Frame(right_panel)

#        self.change_b = Button(bot_frame, text="Change")
#        self.delete_b = Button(bot_frame, text="Delete")
#        self.change_b.pack(side=RIGHT, anchor=E)
#        self.delete_b.pack(side=RIGHT, anchor=E)
        
#        label_frame = Frame(top_frame)
#        front = Label(label_frame, text="Front: ")
#        back = Label(label_frame, text="Back: ")
        
#        entry_frame = Frame(top_frame)
#        self.entry1 = AccentEntry(entry_frame)
#        self.entry2 = AccentEntry(entry_frame)

#        front.pack(pady=7, anchor=W)
#        back.pack(pady=7, anchor=W)
#        self.entry1.pack(pady=5)
#        self.entry2.pack(pady=5)
#        entry_frame.pack(side=RIGHT)
#        label_frame.pack(side=RIGHT)
#        top_frame.pack(pady=5)
#        bot_frame.pack()
#        self.listbox.pack(side=LEFT, pady=3, padx=5)
#        right_panel.pack(side=LEFT, padx=5)

#        self.listbox.lists[0].bind("<ButtonRelease-1>", self.update_text)
#        self.listbox.lists[1].bind("<ButtonRelease-1>", self.update_text)
#        self.change_b['command'] = self.change_card
#        self.delete_b['command'] = self.delete_card

    def edit_cards(self, event):
        """Called when a listCtrl item in double-clicked. Displays a dialog
        for editing and deleting cards"""
        index = event.m_itemIndex
        the_card = self.data_d[self.listbox.GetItemData(index)]
        print the_card
        
    def update_text(self, event):
        """Called when a listbox item in selected. So the text in the entry 
        boxes is updated"""
        self.cur_index = int(self.listbox.curselection() [0])
        #selected = self.listbox.get(self.cur_index)
        #selected = selected.split()
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        cur_card = self.cards[self.cur_index]
        self.entry1.insert(0, cur_card[0])
        self.entry2.insert(0, cur_card[1])

    def change_card(self):
        """Called when the user presses the 'change' button.
           Changes the flashcards"""
        new_front = self.entry1.get()
        new_back = self.entry2.get()
        self.cards.replace(self.cur_index, new_front, new_back)
        self.listbox.delete(self.cur_index)
        self.listbox.insert(self.cur_index, (new_front, new_back))
        #print self.cards

    def delete_card(self):
        """Called to delete a flashcard. Check if the user really wants to with a
           message box"""
        del_cards = tkMessageBox.askokcancel(title="Delete Cards", parent=self.win,
                                 message="Are you sure you want to delete this flashcard?")
        if del_cards:
            del self.cards[self.cur_index] 
            self.listbox.delete(self.cur_index)
            #print self.cards
        

if __name__ == "__main__":
    app = wx.App()
    f = wx.Frame(None)
    f.Show()
    test_cards = FlashcardSet()
    test_cards.add("Hello", "World")
    test_cards.add("Python", "Tkinter")
    test_cards.add("Flashcards", "App")
    test_cards.add("The Zen", "Of Python") 
    view_win = EditWindow(f, test_cards)
    app.MainLoop()

        
        
