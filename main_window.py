# main_window.py
# The Main Window of the flashcards app
# Displays the flashcards in the traditional form, but with both front
# and back visible
# STARTED: 10/14/11
# Version: 0.3
# In version 0.2, the new features are,
# Keeping track of statistics for individual cards
# Done through a new Flashcard class that is a subclass of tuple
# A new format for saving flashcard sets
# Uses front, back, correct, incorrect,\n and repeats to store sets
# NEW in version 0.3: The GUI will be converted to wxPython
# Will be put under version control with git

import wx
import pickle
import os
from card_set import FlashcardSet
from new_cards_window import NewCardsWin
from quiz_window import QuizWindow, QuizOptionsDialog
from edit_window import ViewCardsWindow
from import_cards import ImportCardsDialog

class MainWindow(wx.Frame):
    """The main control window of the Flashcard Application"""
    def __init__(self, master):
        super(MainWindow, self).__init__(master, -1, size=(500, 265))
        self.flashcards = FlashcardSet()
##        Here for testing purposes only
        self.flashcards.add("vencer", "to defeat")
        self.flashcards.add("conseguir", "to achieve")
        self.flashcards.add("fingir", "to pretend")
        self.flashcards.add("proteger", "to protect")
        self.flashcards.add("merecer", "to deserve")
        self.index = 0
        
        self.card_index = 1
        self.saved = False
        self.saved_changes = True
        
        self.SetTitle("Untitled")
        self.initUI()

    def initUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        the_font = wx.Font(36, family=wx.MODERN, style=wx.NORMAL, 
                           weight=wx.NORMAL, faceName='times')
        
        # Building the top of the window. 
        # This includes the front and back of the flashcard
        # This also includes the 'next' and 'previous' buttons
        self.card_front = wx.StaticText(self, label="No Flashcards")
        self.card_back  = wx.StaticText(self, label="to display")
        self.card_number = wx.StaticText(self, label="")
        
        self.card_front.SetFont(the_font)
        self.card_back.SetFont(the_font)
        
        next_back_frame = wx.BoxSizer(wx.HORIZONTAL)
        
        self.next_b = wx.Button(self, label="Next")
        self.prev_b = wx.Button(self, label="Prev") 
        next_back_frame.Add(self.prev_b, flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        next_back_frame.Add(self.next_b, flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        
        vbox.Add(self.card_front, flag=wx.ALIGN_CENTER|wx.ALL, border=10)
        vbox.Add(self.card_back, flag=wx.ALIGN_CENTER|wx.ALL, border=10)
        vbox.Add(self.card_number, flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        vbox.Add(next_back_frame, flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        
        b_size = (150, 22)
        buttons_box = wx.BoxSizer(wx.HORIZONTAL)
        self.new_b = wx.Button(self, label="New Cards", size=b_size)
        self.view_b = wx.Button(self, label="View Cards", size=b_size)
        self.quiz_b = wx.Button(self, label="Quiz", size=b_size)
        buttons_box.Add(self.new_b, flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        buttons_box.Add(self.view_b, flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        buttons_box.Add(self.quiz_b, flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        
        vbox.Add(buttons_box, flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        self.SetSizer(vbox)
        self.Show()
        
        # Building the menu
        menubar = wx.MenuBar()
        filemenu = wx.Menu()
        new = filemenu.Append(id=-1, text="New\tCtrl+N")
        open = filemenu.Append(id=-1, text="Open\tCtrl+O")
        save = filemenu.Append(id=-1, text="Save\tCtrl+S")
        save_as = filemenu.Append(id=-1, text="Save As...\tShift+Ctrl+S")
        quit = filemenu.Append(id=-1, text="Quit\tCtrl+Q")
        
        menubar.Append(filemenu, title="File")

        cardsmenu = wx.Menu()
        shuffle = cardsmenu.Append(id=-1, text="Shuffle Cards")
        view_all = cardsmenu.Append(id=-1, text="View Cards\tCtrl+V")
        find = cardsmenu.Append(id=-1, text="Find\tCtrl+F")
        load_cards = cardsmenu.Append(id=-1, text="Load from Quizlet")
        
        menubar.Append(cardsmenu, title="Cards")
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, handler=self.on_open, id=open.GetId())
        self.Bind(wx.EVT_MENU, handler=self.on_import, id=load_cards.GetId())
        
        self.Bind(wx.EVT_BUTTON, handler=self.show_next_card, 
                  id=self.next_b.GetId())
        self.Bind(wx.EVT_BUTTON, handler=self.show_prev_card,
                  id=self.prev_b.GetId())
        self.Bind(wx.EVT_BUTTON, handler=self.new_cards_window,
                  id=self.new_b.GetId())
        self.Bind(wx.EVT_BUTTON, handler=self.quiz,
                  id=self.quiz_b.GetId())
        self.Bind(wx.EVT_BUTTON, handler=self.edit_cards,
                  id=self.view_b.GetId())

        # Accelerator key binding
#        self.root.bind("<Command-o>", self.on_open)
#        self.root.bind("<Command-s>", self.on_save)
#        self.root.bind("<Command-q>", self.on_quit)
#        self.root.bind("<Command-f>", self.find_card_win)
#        self.root.bind("<Command-v>", self.view_all_cards)

    def shuffle_cards(self, event=None):
        self.flashcards.shuffle()
        self.index = 0

    def view_all_cards(self, event=None):
        """In a new window. Show both sides of every flashcard using labels"""
        win = Toplevel(self.root)
        self.data_view = MultiListbox(win, (("Front", 30), ("Back", 30), 
                                       ("Correct", 10), ("Incorrect", 10),
                                       ("Percent", 10)))
        self.data_view.pack()
        sort_b = Button(win, text="Sort by Percentage", 
                        command=self.sort_flashcards)
        sort_b.pack(side=BOTTOM, pady=10)
        for pair in self.flashcards:
            percent = "%.1f" % (100 * pair.percentage()) + "%"
            self.data_view.insert(END, (pair[0], pair[1], pair.correct,
                                    pair.incorrect, percent))
        
        self.data_view.labels[-1].bind("<ButtonRelease-1>", self.sort_flashcards)
        self.data_view.labels[-1].bind("<Button-1>", self.sort_button_pushed)
        #self.flashcards.sort_by_percentage()
        #print self.flashcards 
    
    def sort_button_pushed(self, event=None):
        """Called when the sort column 'Percentage' is pressed"""
        self.data_view.labels[-1] ['relief'] = SUNKEN
    
    def sort_flashcards(self, event=None):
        """Sort the flashcards by percentage in the view_all_cards screen"""
        self.data_view.labels[-1] ['relief'] = RAISED
        cards_copy = FlashcardSet()
        cards_copy.cards = self.flashcards.cards[:]
        cards_copy.sort_by_percentage()
        self.data_view.delete(0, END)
        for card in cards_copy:
            percent = "%.1f" % (100 * card.percentage()) + "%"
            self.data_view.insert(END, (card[0], card[1], card.correct,
                                         card.incorrect, percent))

    def show_next_card(self, event=None):
        """Method called to display the next flashcard in the set"""
        if len(self.flashcards) == 0:
            return
        
        front = self.flashcards[self.index] [0]
        back  = self.flashcards[self.index] [1]
        self.card_front.SetLabel(front)
        self.card_back.SetLabel(back)
        self.card_front.SetSize(self.card_front.GetBestSize())
        self.card_back.SetSize(self.card_back.GetBestSize())
        self.card_front.Wrap(self.GetSize() [0])
        self.card_back.Wrap(self.GetSize() [0])
        
        self.index += 1
        if self.index == len(self.flashcards):
            self.index = 0
        if self.card_index == len(self.flashcards):
            self.card_index = 1
        else:
            self.card_index += 1
        self.update_card_count()
        if self.GetSize() [1] < self.card_back.GetSize() [1]:
            print 'here'
        self.SetSize((-1, self.GetBestSize() [1]))
        self.SendSizeEvent()
        self.Layout()

    def show_prev_card(self, event=None):
        front = self.flashcards[self.index] [0]
        back  = self.flashcards[self.index] [1]
        self.card_front.SetLabel(front)
        self.card_back.SetLabel(back)
        self.index -= 1
        if self.index == 0:
            self.index = len(self.flashcards) - 1
        if self.card_index == 1:
            self.card_index = len(self.flashcards)
        else:
            self.card_index -= 1
        self.update_card_count()
        self.Layout()
    
    def find_card_win(self, event=None):
        self.find_win = Toplevel(self.root)
        top_frame = Frame(self.find_win)
        self.find_win.title("Find Card")
        
        label = Label(top_frame, text="Search: ")
        self.user_search = Entry(top_frame)
        label.pack(side=LEFT, pady=5, padx=5)
        self.user_search.pack(side=LEFT, pady=5)
        self.user_search.focus_set()
        self.find_b = Button(top_frame, text="Find", width=5, command=self.find)
        self.find_b.pack(pady=5)
        top_frame.pack()
        
        self.result_label = Label(self.find_win, text="Results: ", 
                                  font=('default', '14'))
        self.result_label.pack(pady=5)
        self.user_search.bind("<Return>", self.find)
    
    def find(self, event=None):
        query = self.user_search.get().strip()
        card_found = False
        for i in range(len(self.flashcards)):
            card = self.flashcards[i]
            if (query in card[0]) or (query in card[1]):
                card_found = True
                break
        if card_found:
            self.index = i
            self.show_next_card()
            self.result_label['text'] = "%s %s" % (card[0], card[1])
        else:
            self.result_label['text'] = "No Matches Found"
    
    def update_card_count(self):
        """Update the text of the counter for the card number. i.e. 5 / 26, or 10 / 21"""
        self.card_number.SetLabel("%d / %d" % (self.card_index, len(self.flashcards)))

    def new_cards_window(self, event):
        win = NewCardsWin(self, self.flashcards)
        self.save_changes = False
        old_title = self.GetTitle()
        if old_title[0] != "*":
            self.SetTitle("*%s" % (old_title))
    
    def quiz(self, event):
        """Display the quiz window. Start the actual flashcard quiz"""
        quiz_options = QuizOptionsDialog(self, self.flashcards)
        if quiz_options.ShowModal() == wx.ID_OK:
            cards_for_quiz = FlashcardSet()
            cards_for_quiz.cards = self.flashcards.cards[:]
            number_cards = quiz_options.get_num_cards()
            cards_for_quiz.sort_by_percentage()
            cards_for_quiz.cards = cards_for_quiz.cards[:number_cards]
            #print cards_for_quiz
            quizwin = QuizWindow(self, cards_for_quiz)

    def edit_cards(self, event):
        editwin = ViewCardsWindow(self, self.flashcards)
#        self.save_changes = False
#        old_title = self.root.title()
#        if old_title[0] != "*":
#            self.root.title("*%s" % (old_title))

    def on_import(self, event):
        """Shows a dialog for importing flashcard sets from Quizlet"""
        import_d = ImportCardsDialog(self, title="Import Cards")
        if import_d.ShowModal() == wx.ID_OK:
            self.flashcards = import_d.get_flashcards()
    
    def on_open(self, event=None):
        """Show the dialog to open a file to load saved flashcards"""
        open_window = wx.FileDialog(self, style=wx.FD_OPEN)
        if open_window.ShowModal() == wx.ID_OK:
            filename = open_window.GetFilename()
            dir = open_window.GetDirectory()
            pathname = os.path.join(dir, filename)
            try:
                self.flashcards = FlashcardSet.load_set(pathname)
                self.SetTitle(filename)
            except IOError:
                print "Unable to read file"
            self.saved = filename
            self.show_next_card()
            self.card_index = 1
            self.update_card_count()

    def on_save(self, event=None):
        """Save the current flashcard set to a file"""
        if not self.saved:
            save_dialog = wx.FileDialog(self, style=wx.FD_SAVE)
            if save_dialog.ShowModal() == wx.ID_OK:
                filename = save_dialog.GetFilename()
                dir = save_dialog.GetDirectory()
                save_name = os.path.join(dir, filename)
                self.flashcards.save(save_name)
                self.saved = save_name
                real_name = save_name.split("/") [-1]
                self.SetTitle("%s" % (real_name))
        else:
            self.flashcards.save(self.saved)
            real_name = self.saved.split("/") [-1]
            self.SetTitle("%s" % (real_name))
        self.saved_changes = True

    def on_quit(self, event=None):
        self.Destroy()
        
app = wx.App()
f = MainWindow(None)
app.MainLoop()