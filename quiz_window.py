#! usr/bin/env python
# quiz_window.py
# The quiz window for the flashcard app. It is a question and answer quiz for
# the user of the flashcards
# STARTED: October 22 2011
from Tkinter import *
from accent_entry import AccentEntry

class QuizWindow:
    """The window where you take a quiz on the flashcards"""
    def __init__(self, master, cards):
        self.cards = cards
        self.cards.shuffle()
        self.question_index = 0
        self.root = master
        self.correct = 0
        self.incorrect = 0
        self.remaining = len(self.cards)
        self.initUI()
        
    def initUI(self):
        myfont = ("default", "14")
        self.window = Toplevel(self.root)
        self.window.title("Quiz")
        left_pane = Frame(self.window)
        right_pane = Frame(self.window)
        self.num_correct = Label(left_pane, text="Correct: 0", font=myfont)
        self.num_incorrect = Label(left_pane, text="Incorrect: 0", font=myfont)
        self.num_remaining = Label(left_pane, font=myfont,
                               text="Remaining: %d" % (len(self.cards)))
        self.num_correct.pack(pady=2)
        self.num_incorrect.pack(pady=2)
        self.num_remaining.pack(pady=2)

        mid_frame = Frame(right_pane)

        self.question_label = Label(right_pane, text=self.cards[0] [0], font=myfont)
        self.answer_box = AccentEntry(mid_frame, font="default")
        self.answer_button = Button(mid_frame, text="Answer", command=self.on_answer)
        self.result = Label(right_pane, text="", font=myfont)
        self.result2 = Label(right_pane, text="", font=myfont)
        self.next = Label(right_pane, text="", font=myfont)
        self.answer_box.bind("<Return>", self.on_answer)
        self.next.bind("<Return>", self.next_q)

        self.answer_box.pack(side=LEFT, padx=5)
        self.answer_button.pack(side=LEFT)
        self.question_label.pack(pady=5)
        mid_frame.pack(pady=5)
        self.result.pack(pady=3)
        self.result2.pack(pady=3)
        self.next.pack(pady=3)

        left_pane.pack(side=LEFT, padx=5)
        right_pane.pack(side=LEFT, padx=5)

    def on_answer(self, evnet=None):
        """Called when the user submits an answer. Checks its correctness and returns feedback"""
        #print "in self.on_answer"
        the_card = self.cards[self.question_index] 
        the_answer = the_card[1].lower()
        user_answer = self.answer_box.get().strip().lower()
        print repr(user_answer)
        print repr(the_answer)
        if the_answer == user_answer:
            self.correct += 1
            the_card.correct += 1
            self.result['text'] = "Correct!"
        else:
            self.result['text'] = "Sorry. Incorrect"
            self.result2['text'] = "Answer: %s" % (the_answer)
            self.incorrect += 1
            the_card.incorrect += 1
        self.remaining -=1
        self.update_scores()
        self.answer_button['command'] = self.nothing
        self.answer_box['state'] = DISABLED
        self.next['text'] = "Press <Return> to continue"
        self.next.focus_set()

    def next_q(self, event=None):
        """Called to go to the next question. The card index is incremened"""
        myfont = ("default", "14")     
        self.question_index += 1
        if self.question_index == len(self.cards):
            self.dialog = Toplevel(self.window)
            self.dialog.title("Again?")
            c = self.correct
            total = self.correct + self.incorrect
            label = Label(self.dialog, text="You got %d out of %s questions right" % (c, total),
                          font=myfont)                     
            label.pack(pady=5, padx=5)
            percentage = (self.correct / float(self.correct + self.incorrect)) * 100
            percent_label = Label(self.dialog, text="Percentage: %d" % (percentage) + "%", font=myfont)
            percent_label.pack(padx=5)
            q = Label(self.dialog, text="Would you like to take the quiz again?", font=myfont)
            q.pack(pady=5, padx=5)

            bot_frame = Frame(self.dialog)
            yes = Button(bot_frame, text="Yes", width=5, default='active', command=self.restart_quiz)
            no = Button(bot_frame, text="No", width=5, command=self.window.destroy)
            yes.pack(side=RIGHT, padx=5, pady=5)
            no.pack(side=RIGHT, padx=5, pady=5)
            bot_frame.pack()
            
        else:
            self.question_label['text'] = self.cards[self.question_index] [0]
            self.result['text'] = ""
            self.result2['text'] = ""
            self.next['text'] = ""
            self.answer_button['command'] = self.on_answer
            self.answer_box['state'] = NORMAL
            self.answer_box.delete(0, END)
            self.answer_box.focus_set()

    def nothing(self):
        pass

    def update_scores(self):
        self.num_correct['text'] = "Correct: %s" % (self.correct)
        self.num_incorrect['text'] = "Incorrect: %s" % (self.incorrect)
        self.num_remaining['text'] = "Remaining: %s" % (self.remaining)

    def restart_quiz(self):
        self.cards.shuffle()
        self.dialog.destroy()
        self.question_index = 0
        self.question_label['text'] = self.cards[0] [0]
        self.next['text'] = ""
        self.answer_button['command'] = self.on_answer
        self.answer_box['state'] = NORMAL
        self.answer_box.delete(0, END)
        self.answer_box.focus_set()
        self.correct = 0
        self.incorrect = 0
        self.remaining = len(self.cards)
        self.update_scores()
        self.result['text'] = ""
        self.result2['text'] = ""

if __name__ == "__main__":
    root = Tk()
    app = QuizWindow(root, [("volver", "vuelto"), ("morir", "muerto"),
                            ("ver", "visto"),  ("escribir", "escrito")])
    root.mainloop()

        
