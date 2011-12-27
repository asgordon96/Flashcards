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

from Tkinter import *
import tkFileDialog
from multi_listbox import MultiListbox
import pickle
from card_set import FlashcardSet
from new_cards_window import NewCardsWin
from quiz_window import QuizWindow
from edit_window import EditWindow

class MainWindow:
    """The main control window of the Flashcard Application"""
    def __init__(self, master):
        self.flashcards = FlashcardSet()
##        Here for testing purposes only
##        self.flashcards.add("vencer", "to defeat")
##        self.flashcards.add("conseguir", "to achieve")
##        self.flashcards.add("fingir", "to pretend")
##        self.flashcards.add("proteger", "to protect")
##        self.flashcards.add("merecer", "to deserve")
        self.index = 0
        
        self.card_index = 1
        self.saved = False
        self.saved_changes = True
        
        self.root = master
        self.root.title("Untitled")
        self.initUI()

    def initUI(self):
        top_frame = Frame(self.root)
        bot_frame = Frame(self.root)
        the_font = ("Default", "36")
        
        # Building the top of the window. 
        # This includes the front and back of the flashcard
        # This also includes the 'next' and 'previous' buttons
        self.card_front = Label(top_frame, text="No flashcards", font=the_font)
        self.card_back  = Label(top_frame, text="to display", font=the_font)
        self.card_number = Label(top_frame, text="")
        next_back_frame = Frame(top_frame)
        self.next_b     = Button(next_back_frame, text="Next", width=7,
                                 command=self.show_next_card)
        self.prev_b = Button(next_back_frame, text="Previous", width=7,
                             command=self.show_prev_card)
        
        self.card_front.pack(pady=5)
        self.card_back.pack(pady=5)
        self.card_number.pack(pady=5)
        
        self.prev_b.pack(side=LEFT)
        self.next_b.pack(side=LEFT)
        next_back_frame.pack(pady=5)

        self.new_b = Button(bot_frame, text = "New Cards", width=15,
                            command=self.new_cards_window)
        
        self.delete_b = Button(bot_frame, text= "Edit Cards", width=15, 
                               command=self.edit_cards)
        
        self.quiz_b = Button(bot_frame, text = "Quiz", width=15, 
                             command=self.quiz_begin)

        self.new_b.pack(side=RIGHT, pady=5, padx=5)
        self.delete_b.pack(side=RIGHT, pady=5, padx=5)
        self.quiz_b.pack(side=RIGHT, pady=5, padx=5)

        top_frame.pack()
        bot_frame.pack(pady=10)

        # Building the menu
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", accelerator="Command+N")
        filemenu.add_command(label="Open", accelerator="Command+O", command=self.on_open)
        filemenu.add_command(label="Save", accelerator="Command+S", command=self.on_save)
        filemenu.add_command(label="Quit", accelerator="Command+Q", command=self.on_quit)
        menubar.add_cascade(label="File", menu=filemenu)

        cardsmenu = Menu(menubar, tearoff=0)
        cardsmenu.add_command(label="Shuffle Cards", command=self.shuffle_cards)
        cardsmenu.add_command(label="View All", command=self.view_all_cards,
                              accelerator="Command+V")
        cardsmenu.add_command(label="Find", accelerator="Command+F", command=self.find_card_win)
        menubar.add_cascade(label="Cards", menu=cardsmenu)

        self.root.config(menu=menubar)

        # Accelerator key binding
        self.root.bind("<Command-o>", self.on_open)
        self.root.bind("<Command-s>", self.on_save)
        self.root.bind("<Command-q>", self.on_quit)
        self.root.bind("<Command-f>", self.find_card_win)
        self.root.bind("<Command-v>", self.view_all_cards)

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

    def show_next_card(self):
        """Method called to display the next flashcard in the set"""
        if len(self.flashcards) == 0:
            return
        
        front = self.flashcards[self.index] [0]
        back  = self.flashcards[self.index] [1]
        self.card_front['text'] = front
        self.card_back['text'] = back
        self.index += 1
        if self.index == len(self.flashcards):
            self.index = 0
        if self.card_index == len(self.flashcards):
            self.card_index = 1
        else:
            self.card_index += 1
        self.update_card_count()

    def show_prev_card(self):
        front = self.flashcards[self.index] [0]
        back  = self.flashcards[self.index] [1]
        self.card_front['text'] = front
        self.card_back['text'] = back
        self.index -= 1
        if self.index == 0:
            self.index = len(self.flashcards) - 1
        if self.card_index == 1:
            self.card_index = len(self.flashcards)
        else:
            self.card_index -= 1
        self.update_card_count()
    
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
        self.card_number['text'] = "%d / %d" % (self.card_index, len(self.flashcards))

    def new_cards_window(self):
        win = NewCardsWin(self.root, self.flashcards)
        self.save_changes = False
        old_title = self.root.title()
        if old_title[0] != "*":
            self.root.title("*%s" % (old_title))
        

    def quiz_begin(self):
        """Shows a window asking to quiz on all cards, or only
           difficult ones"""
        self.quiz_start = Toplevel(self.root)
        mid_pane = Frame(self.quiz_start)
        self.text_var = StringVar()
        self.text_var.set("all")
        self.num_cards_var = StringVar()
        n_cards_options = [str(item) for item in range(1, len(self.flashcards) + 1)]
        all_cards = Radiobutton(self.quiz_start, text="All Cards", value="all", 
                                variable=self.text_var)
        diff_cards = Radiobutton(mid_pane, text="Difficult Cards", 
                                 value="diff", variable=self.text_var)
        num_cards = OptionMenu(mid_pane, self.num_cards_var, *n_cards_options)
        num_cards.config(state='disabled')
        self.num_cards_var.set('1')
        enable = lambda x=num_cards: x.config(state='normal')
        disable = lambda x=num_cards: x.config(state='disabled')
        diff_cards['command'] = enable
        all_cards['command'] = disable
        start_quiz_b = Button(self.quiz_start, text="Start Quiz!",
                              command=self.quiz)
        all_cards.pack(padx=5, pady=5, anchor=W)
        diff_cards.pack(padx=5, pady=5, anchor=W, side=LEFT)
        num_cards.pack(padx=5, pady=5, side=LEFT)
        mid_pane.pack()
        start_quiz_b.pack(pady=5)
        
    
    def quiz(self):
        """Display the quiz window. Start the actual flashcard quiz"""
        cards_for_quiz = FlashcardSet()
        cards_for_quiz.cards = self.flashcards.cards[:]
        if self.text_var.get() == "diff":
            number_cards = int(self.num_cards_var.get())
            cards_for_quiz.sort_by_percentage()
            cards_for_quiz.cards = cards_for_quiz.cards[:number_cards]
            #print cards_for_quiz
        
        self.quiz_start.destroy()
        quizwin = QuizWindow(self.root, cards_for_quiz)

    def edit_cards(self):
        editwin = EditWindow(self.root, self.flashcards)
        self.save_changes = False
        old_title = self.root.title()
        if old_title[0] != "*":
            self.root.title("*%s" % (old_title))

    def on_open(self, event=None):
        """Show the dialog to open a file to load saved flashcards"""
        open_window = tkFileDialog.Open(self.root, filetypes=[("Flashcard Set", "*.fld"),
                                                              ("All Files", "*")])
        filename = open_window.show()
        try:
            self.flashcards = FlashcardSet.load_set(filename)
            file_last = filename.split("/") [-1]
            self.root.title("%s" % (file_last))
        except IOError:
            print "Unable to read file"
        self.saved = filename
        self.show_next_card()
        self.card_index = 1
        self.update_card_count()

    def on_save(self, event=None):
        """Save the current flashcard set to a file"""
        if not self.saved:
            save_dialog = tkFileDialog.SaveAs(self.root)
            save_name = save_dialog.show()
            self.flashcards.save(save_name)
            self.saved = save_name
            real_name = save_name.split("/") [-1]
            self.root.title("%s" % (real_name))
        else:
            self.flashcards.save(self.saved)
            real_name = self.saved.split("/") [-1]
            self.root.title("%s" % (real_name))
        self.saved_changes = True

    def on_quit(self, event=None):
        self.root.destroy()
        
        
root = Tk()
app = MainWindow(root)
root.mainloop()
