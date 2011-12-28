# new_cards_window.py
# STARTED: 10/14/11
# A dialog window for creating new flashcards
# Used by main_window.py
# NEW: converting the GUI to wxPython

import wx

class NewCardsWin:
    """The dialog window for making new flashcards"""
    def __init__(self, master, cards):
        self.win = wx.Dialog(master, title="Add Cards", size=(250, 150),
                             style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.cards = cards
        self.initUI()

    def initUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        fgs = wx.FlexGridSizer(rows=2, cols=2, vgap=10, hgap=10)
        
        size = (150, 22)
        self.front_entry = wx.TextCtrl(self.win, size=size)
        self.back_entry = wx.TextCtrl(self.win, size=size, 
                                      style=wx.TE_PROCESS_ENTER)

        front_label = wx.StaticText(self.win, label="Front:")
        back_label = wx.StaticText(self.win, label="Back:")
        
        fgs.Add(front_label)
        fgs.Add(self.front_entry)
        fgs.Add(back_label)
        fgs.Add(self.back_entry)
        vbox.Add(fgs, flag=wx.ALL, border=10)
        
        buttons_frame = wx.BoxSizer(wx.HORIZONTAL)
        add_b = wx.Button(self.win, label="Add")
        finish_b = wx.Button(self.win, label="Finish")
        buttons_frame.Add(add_b, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        buttons_frame.Add(finish_b, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        vbox.Add(buttons_frame, flag=wx.ALIGN_CENTER)
        self.win.SetSizer(vbox)
        
        add_b.Bind(wx.EVT_BUTTON, handler=self.add_new_card)
        finish_b.Bind(wx.EVT_BUTTON, handler=self.finish_call)
        self.back_entry.Bind(wx.EVT_TEXT_ENTER, handler=self.add_new_card)
        self.win.Show()

    def add_new_card(self, event=None):
        front_side = self.front_entry.GetValue()
        back_side = self.back_entry.GetValue()
        self.cards.add(front_side, back_side)
        self.front_entry.SetValue("")
        self.back_entry.SetValue("")
        self.front_entry.SetFocus()

    def finish_call(self, event=None):
        if self.front_entry.GetValue() and self.back_entry.GetValue():
            self.add_new_card()
        self.win.Destroy()

if __name__ == "__main__":
    app = wx.App()
    f = wx.Frame(None)
    f.Show()
    w = NewCardsWin(f, None)
    app.MainLoop()
        
