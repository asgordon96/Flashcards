#! usr/bin/env python
# quiz_window.py
# The quiz window for the flashcard app. It is a question and answer quiz for
# the user of the flashcards
# STARTED: October 22 2011
import wx

class QuizWindow:
    """The window where you take a quiz on the flashcards"""
    def __init__(self, master, cards):
        self.cards = cards
        #self.cards.shuffle()
        self.question_index = 0
        self.root = master
        self.correct = 0
        self.incorrect = 0
        self.remaining = len(self.cards)
        self.initUI()
        
    def initUI(self):
        myfont = wx.Font(14, family=wx.MODERN, style=wx.NORMAL, weight=wx.NORMAL,
                         face='lucida grande')
        self.window = wx.Dialog(self.root, 
                                style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.window.SetTitle("Quiz")
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_pane = wx.BoxSizer(wx.VERTICAL)
        right_pane = wx.BoxSizer(wx.VERTICAL)
        
        self.num_correct = wx.StaticText(self.window, label="Correct: 0")
        self.num_correct.SetFont(myfont)
        self.num_incorrect = wx.StaticText(self.window, label="Incorrect: 0")
        self.num_incorrect.SetFont(myfont)
        self.num_remaining = wx.StaticText(self.window, label="Remaining: %d" %
                                           self.remaining)
        self.num_remaining.SetFont(myfont)
        
        left_pane.Add((-1, 20))
        left_pane.Add(self.num_correct, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        left_pane.Add(self.num_incorrect, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        left_pane.Add(self.num_remaining, flag=wx.ALL|wx.ALIGN_CENTER, border=5)

        mid_frame = wx.BoxSizer(wx.HORIZONTAL)

        self.question_label = wx.StaticText(self.window, 
                                            label=self.cards[0] [0])
        self.question_label.SetFont(myfont)
        right_pane.Add(self.question_label, flag=wx.ALL|wx.ALIGN_CENTER,
                       border=5)
        
        self.answer_box = wx.TextCtrl(self.window, style=wx.TE_PROCESS_ENTER,
                                      size=(175,22))
        self.answer_button = wx.Button(self.window, label="Answer")
        
        mid_frame.Add(self.answer_box, flag=wx.ALL, border=5)
        mid_frame.Add(self.answer_button, flag=wx.ALL, border=5)
        right_pane.Add(mid_frame, flag=wx.ALL, border=5)
        
        self.result = wx.StaticText(self.window, label="Test")
        self.result2 = wx.StaticText(self.window, label="Run")
        self.next = wx.StaticText(self.window, label="<Return>")
        self.result.SetFont(myfont)
        self.result2.SetFont(myfont)
        self.next.SetFont(myfont) 
        
        right_pane.Add(self.result, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        right_pane.Add(self.result2, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        right_pane.Add(self.next, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        
        sizer.Add(left_pane)
        sizer.Add(right_pane)
        self.window.SetSizer(sizer)
        self.window.Show()

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
    app = wx.App()
    f = wx.Frame(None)
    f.Show()
    win = QuizWindow(f, [("volver", "vuelto"), ("morir", "muerto"),
                            ("ver", "visto"),  ("escribir", "escrito")])
    app.MainLoop()

        
