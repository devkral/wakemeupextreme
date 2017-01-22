import tkinter

def create_lfunc(num, func):
    def ff():
        func(num)
    return ff

class Gui(tkinter.Frame):
    questionl = None
    question_answer = None
    question_entry = None
    alarm_stop = None
    correctanswer = None
    alarmactive = False
    
    def __init__(self, alarm_stop):
        super().__init__(None, borderwidth=5)
        self.alarm_stop = alarm_stop
        self.pack()
        self.master.attributes('-zoomed', True)
        self["width"] = self.master.winfo_screenwidth()
        self["height"] = self.master.winfo_screenheight()
        # fullscreen
        #self.master.overrideredirect(1)
        #self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        self.questionl = tkinter.StringVar(self, value="no question")
        self.question_answer = tkinter.StringVar(self)
        tkinter.Label(self, textvariable=self.questionl).place(relx=0, rely=0, relwidth=1.0, relheight=0.2, anchor=tkinter.NW)
        self.question_entry = tkinter.Entry(self,justify="right", textvariable=self.question_answer)
        self.question_entry.place(relx=0, rely=0.2, relwidth=0.8, relheight=0.2, anchor=tkinter.NW)
        self.question_entry.bind('<Key-Return>', self.enter_calc)
        tkinter.Button(self, text="x", command=self.enter_calc).place(relx=0.8, rely=0.2, relwidth=0.2, relheight=0.2, anchor=tkinter.NW)
        for y in range(0, 2):
            for x in range(0, 5):
                tkinter.Button(self, text=str(y*5+x), command=create_lfunc(str(y*5+x),self.enter_num)).place(relx=x*0.15, rely=0.4+0.3*y, relwidth=0.15, relheight=0.3, anchor=tkinter.NW)
        tkinter.Button(self, text="back", command=self.backspace).place(relx=0.8, rely=0.4, relwidth=0.20, relheight=0.6, anchor=tkinter.NW)
    
    def enter_num(self, num):
        self.question_answer.set(self.question_answer.get()+num)
        self.pack()
    def backspace(self):
        self.question_answer.set(self.question_answer.get()[:-1])
        self.pack()

    def alarm_start(self, question, correct_answer):
        self.correctanswer = correct_answer
        self.tkraise()
        self.question_answer.set("")
        self.questionl.set(question)
        self.question_entry.focus()
    
    def enter_calc(self, *ll):
        if not self.alarmactive:
            return
        if self.question_answer.get() == self.correctanswer:
            self.question_answer.set("")
            self.questionl.set("no question")
            self.alarm_stop()
        else:
            self.question_answer.set("")
    def run(self):
        self.mainloop()
