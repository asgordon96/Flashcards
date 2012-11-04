# This is for importing flashcards from quizlet
# STARTED: January 8, 2012
# BY: Aaron Gordon
# Using urllib2 and the export features of quizlet can import cards
# The user enters the url of the flashcards form quizlet and the cards are loaded
import urllib2
import wx
from card_set import FlashcardSet, Flashcard

def get_cards_export(url):
    """Gets the quizlet tab separated export text from the url"""
    parts = url.split('/')
    new_url = "/".join(parts[:len(parts) - 2]) + "/export/"
    page = urllib2.urlopen(new_url)
    content = page.read()
    start_index = content.find("textarea")
    for char in content[start_index:]:
        if char == '>':
            break
        start_index += 1
    start_index += 1
    
    end_index = content.find("</textarea>")
    cards = content[start_index:end_index]
    split_cards = [line.split('\t') for line in cards.split('\n')]
    for line in split_cards:
        print line
    
    flashcards = FlashcardSet()
    for front, back in split_cards:
        flashcards.add(front, back)
    return flashcards

class ImportCardsDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(ImportCardsDialog, self).__init__(parent, title=title,
              style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        
        self.cards = None
        self.SetSize((500, 150))
        self.SetMinSize((500, 150))
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        message = "Import cards from Quizlet. Copy and paste the url below"
        heading = wx.StaticText(self, label=message)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        text_label = wx.StaticText(self, label="Quizlet Url:")
        self.url_text = wx.TextCtrl(self, size=(200, -1))
        hbox.Add(text_label, wx.ALL, border=10)
        hbox.Add(self.url_text, wx.ALL|wx.EXPAND, border=10)
        
        buttons_box = wx.BoxSizer(wx.HORIZONTAL)
        import_b = wx.Button(self, label="Import")
        cancel_b = wx.Button(self, label="Cancel")
        buttons_box.Add(import_b, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        buttons_box.Add(cancel_b, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        
        vbox.Add(heading, flag=wx.ALL|wx.ALIGN_CENTER, border=10)
        vbox.Add(hbox, flag=wx.ALL, border=10)
        vbox.Add(buttons_box, flag=wx.ALL|wx.ALIGN_CENTER, border=10)
        
        import_b.Bind(wx.EVT_BUTTON, handler=self.on_import)
        cancel_b.Bind(wx.EVT_BUTTON, handler=self.on_cancel)
        
        self.SetSizer(vbox)
    
    def on_import(self, event):
        """Imports the flashcards set at the specified url"""
        try:
            self.cards = get_cards_export(self.url_text.GetValue())
#            print self.cards
            self.EndModal(wx.ID_OK)
        except urllib2.HTTPError:
            d = wx.MessageDialog(self, message="URL not found", caption="Error",
                                 style=wx.OK)
            d.ShowModal()
    
    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)
    
    def get_flashcards(self):
        return self.cards

if __name__ == "__main__":
    app = wx.App()
    f = wx.Frame(None)
    f.Show()
    import_d = ImportCardsDialog(f, title="Import Cards")
    import_d.Show()
    app.MainLoop()
        
        