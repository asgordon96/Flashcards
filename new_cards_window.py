# new_cards_window.py
# STARTED: 10/14/11
# A dialog window for creating new flashcards
# Used by main_window.py
# NEW: converting the GUI to wxPython

import wx

class NewCardsWin:
    """The dialog window for making new flashcards"""
    def __init__(self, master, cards):
        self.win = Toplevel(master)
        self.win.title("Add Flashcards")
        self.cards = cards
        self.initUI()

    def initUI(self):
        top_frame = Frame(self.win)
        bot_frame = Frame(self.win)
        left = Frame(top_frame)
        right = Frame(top_frame)

        self.front_side = StringVar()
        self.back_side = StringVar()
        self.front_entry = AccentEntry(right, textvariable=self.front_side,
                                 font="default")
        self.back_entry = AccentEntry(right, textvariable=self.back_side,
                                font="default")
        self.front_entry.pack(pady=5, padx=10)
        self.back_entry.pack(pady=5, padx=10)
        right.pack(side=RIGHT)

        front_label = Label(left, text="Front:", font="default")
        back_label = Label(left, text="Back:", font="default")
        front_label.pack(pady=5)
        back_label.pack(pady=5)
        left.pack(side=RIGHT)
        top_frame.pack(pady=5)

        add_b = Button(bot_frame, text="Add", width=6,
                       command=self.add_new_card)
        finish_b = Button(bot_frame, text="Finish", width=6,
                          command=self.finish_call)
        finish_b.pack(side=RIGHT, padx=5)
        add_b.pack(side=RIGHT, padx=5)
        bot_frame.pack(pady=5)
        self.front_entry.bind("<Return>", self.add_new_card)
        self.back_entry.bind("<Return>", self.add_new_card)

    def add_new_card(self, event=None):
        front_side = self.front_side.get()
        back_side = self.back_side.get()
        self.cards.add(front_side, back_side)
        self.front_side.set("")
        self.back_side.set("")
        self.front_entry.focus_set()

    def finish_call(self):
        if self.front_side.get() and self.back_side.get():
            self.add_new_card()
        self.win.destroy()

if __name__ == "__main__":
    root = Tk()
    win = NewCardsWin(root, None)
    root.mainloop()

        
