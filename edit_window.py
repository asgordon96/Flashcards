#! usr/bin/env python
# edit_window.py
# Go to this window when editing the flashcards
# STARTED: November 2, 2011
from Tkinter import *
import tkMessageBox
from card_set import FlashcardSet
from accent_entry import AccentEntry
from multi_listbox import MultiListbox

class EditWindow:
    """The window for editing the flashcards"""
    def __init__(self, master, flashcards):
        self.win = Toplevel(master)
        self.win.title("Edit Flashcards")
        self.cards = flashcards
        self.createUI()

    def createUI(self):
        """Draw the User Interface for the window"""
        self.listbox = MultiListbox(self.win, (("Front", 30), ("Back", 30)))
        for card in self.cards:
            self.listbox.insert(END, (card[0], card[1]))
        right_panel = Frame(self.win)
        top_frame = Frame(right_panel)
        bot_frame = Frame(right_panel)

        self.change_b = Button(bot_frame, text="Change")
        self.delete_b = Button(bot_frame, text="Delete")
        self.change_b.pack(side=RIGHT, anchor=E)
        self.delete_b.pack(side=RIGHT, anchor=E)
        
        label_frame = Frame(top_frame)
        front = Label(label_frame, text="Front: ")
        back = Label(label_frame, text="Back: ")
        
        entry_frame = Frame(top_frame)
        self.entry1 = AccentEntry(entry_frame)
        self.entry2 = AccentEntry(entry_frame)

        front.pack(pady=7, anchor=W)
        back.pack(pady=7, anchor=W)
        self.entry1.pack(pady=5)
        self.entry2.pack(pady=5)
        entry_frame.pack(side=RIGHT)
        label_frame.pack(side=RIGHT)
        top_frame.pack(pady=5)
        bot_frame.pack()
        self.listbox.pack(side=LEFT, pady=3, padx=5)
        right_panel.pack(side=LEFT, padx=5)

        self.listbox.lists[0].bind("<ButtonRelease-1>", self.update_text)
        self.listbox.lists[1].bind("<ButtonRelease-1>", self.update_text)
        self.change_b['command'] = self.change_card
        self.delete_b['command'] = self.delete_card

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
    root = Tk()
    test_cards = FlashcardSet()
    test_cards.add("Hello", "World")
    test_cards.add("Python", "Tkinter")
    test_cards.add("Flashcards", "App")
    test_cards.add("The Zen", "Of Python") 
    win = EditWindow(root, test_cards)
    root.mainloop()
        
        
