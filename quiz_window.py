#! usr/bin/env python
# quiz_window.py
# The quiz window for the flashcard app. It is a question and answer quiz for
# the user of the flashcards
# STARTED: October 22 2011
import wx

class QuizOptionsDialog(wx.Dialog):
    """Dialog asking if the user wants to be quizzed on all cards or
    only the most difficult ones"""
    def __init__(self, master, card_set):
        super(QuizOptionsDialog, self).__init__(master)
        self.SetTitle("Quiz Options")
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        grid = wx.FlexGridSizer(rows=2, cols=2, vgap=10, hgap=10)
        
        self.all_r = wx.RadioButton(self, label="All Cards", style=wx.RB_GROUP)
        self.some_r = wx.RadioButton(self, label="Most Difficult")
        self.all_r.SetValue(True)
        choices = map(str, range(1, len(card_set)))
        self.num_cards = wx.ComboBox(self, choices=choices, style=wx.CB_READONLY)
        
        grid.AddMany([(self.all_r, 0, wx.ALIGN_CENTER_VERTICAL), 
                      (wx.StaticText(self, label="")),
                      (self.some_r, 0, wx.ALIGN_CENTER_VERTICAL), (self.num_cards)])
        
        vbox.Add(grid, flag=wx.ALL, border=10)
        self.SetSizer(vbox)
        self.Show()
        
class QuizAgainDialog(wx.Dialog):
    """Dialog shown showing results of the quiz and asking if the user
    wants to take the quiz again"""
    def __init__(self, master, correct, total):
        super(QuizAgainDialog, self).__init__(master, size=(300, 150))
        self.SetTitle("Again?")
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        result_string = "You got %d out of %d questions correct" % (correct, total)
        percent_string = "Percentage: %d%%" % (round(float(correct) / total * 100))
        again_label = "Take the quiz again?"
        result_label = wx.StaticText(self, label=result_string)
        percent_label = wx.StaticText(self, label=percent_string)
        again_label = wx.StaticText(self, label=again_label)
        
        buttons_box = wx.BoxSizer(wx.HORIZONTAL)
        yes_button = wx.Button(self, label="Yes")
        no_button = wx.Button(self, label="No")
        yes_button.SetDefault()
        buttons_box.Add(yes_button, flag=wx.ALL, border=3)
        buttons_box.Add(no_button, flag=wx.ALL, border=3)
                
        vbox.Add(result_label, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        vbox.Add(percent_label, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        vbox.Add(again_label, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        vbox.Add(buttons_box, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        
        yes_button.Bind(wx.EVT_BUTTON, handler=self.on_yes)
        no_button.Bind(wx.EVT_BUTTON, handler=self.on_no)
        
        self.SetSizer(vbox)
    
    def on_yes(self, event):
        self.EndModal(wx.ID_YES)
    
    def on_no(self, event):
        self.EndModal(wx.ID_NO)
        
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
        self.window = wx.Dialog(self.root, size=(400, 200),
                                style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.window.SetTitle("Quiz")
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_pane = wx.BoxSizer(wx.VERTICAL)
        self.right_pane = wx.BoxSizer(wx.VERTICAL)
        
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
        self.right_pane.Add(self.question_label, flag=wx.ALL|wx.ALIGN_CENTER,
                       border=5)
        
        self.answer_box = wx.TextCtrl(self.window, style=wx.TE_PROCESS_ENTER,
                                      size=(175,22))
        self.answer_button = wx.Button(self.window, label="Answer")
        
        mid_frame.Add(self.answer_box, flag=wx.ALL, border=5)
        mid_frame.Add(self.answer_button, flag=wx.ALL, border=5)
        self.right_pane.Add(mid_frame, flag=wx.ALL, border=5)
        
        self.result = wx.StaticText(self.window, label="")
        self.result2 = wx.StaticText(self.window, label="")
        self.result.SetFont(myfont)
        self.result2.SetFont(myfont)

        self.right_pane.Add(self.result, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        self.right_pane.Add(self.result2, flag=wx.ALL|wx.ALIGN_CENTER, border=5)
        
        self.answer_button.Bind(wx.EVT_BUTTON, handler=self.on_answer)
        self.answer_box.Bind(wx.EVT_TEXT_ENTER, handler=self.on_answer)
        
        sizer.Add(left_pane)
        sizer.Add(self.right_pane)
        self.window.SetSizer(sizer)
        self.window.Show()

    def on_answer(self, evnet):
        """Called when the user submits an answer. Checks its correctness and returns feedback"""
        the_card = self.cards[self.question_index] 
        the_answer = the_card[1].lower()
        user_answer = self.answer_box.GetValue().strip().lower()
        if the_answer == user_answer:
            self.correct += 1
            #the_card.correct += 1
            self.result.SetLabel("Correct!")
            self.result2.SetLabel("")
        else:
            self.result.SetLabel("Sorry. Incorrect")
            self.result2.SetLabel("Answer: %s" % (the_answer))
            self.incorrect += 1
            #the_card.incorrect += 1
        self.remaining -=1
        self.update_scores()
        self.answer_box.Disable()
        self.next = wx.Button(self.window, label="Next")
        self.right_pane.Add(self.next, flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        self.next.SetDefault()
        self.next.Bind(wx.EVT_BUTTON, handler=self.next_q)
        self.window.Layout()

    def next_q(self, event=None):
        """Called to go to the next question. The card index is incremened"""   
        self.question_index += 1
        if self.question_index == len(self.cards):
            c = self.correct
            total = self.correct + self.incorrect
            again_dialog = QuizAgainDialog(self.window, self.correct, total)
            if again_dialog.ShowModal() == wx.ID_YES:
                self.restart_quiz()
            else:
                self.window.Destroy()
            
        else:
            self.question_label.SetLabel(self.cards[self.question_index] [0])
            self.result.SetLabel("")
            self.result2.SetLabel("")
            self.next.SetLabel("")
            self.answer_box.Enable()
            self.answer_box.SetValue("")
            self.answer_box.SetFocus()
            self.next.Destroy()

    def nothing(self):
        pass

    def update_scores(self):
        self.num_correct.SetLabel("Correct: %s" % (self.correct))
        self.num_incorrect.SetLabel("Incorrect: %s" % (self.incorrect))
        self.num_remaining.SetLabel("Remaining: %s" % (self.remaining))

    def restart_quiz(self):
        #self.cards.shuffle()
        self.question_index = 0
        self.question_label.SetLabel(self.cards[0] [0])
        self.answer_box.Enable()
        self.answer_box.SetValue("")
        self.answer_box.SetFocus()
        self.correct = 0
        self.incorrect = 0
        self.remaining = len(self.cards)
        self.update_scores()
        self.result.SetLabel("")
        self.result2.SetLabel("")
        self.next.Destroy()

if __name__ == "__main__":
    app = wx.App()
    f = wx.Frame(None)
    f.Show()
    win = QuizWindow(f, [("volver", "vuelto"), ("morir", "muerto"),
                            ("ver", "visto"),  ("escribir", "escrito")])
    d = QuizOptionsDialog(f, range(10))
    app.MainLoop()

        
