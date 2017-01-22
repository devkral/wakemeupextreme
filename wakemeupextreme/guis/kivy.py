import kivy
kivy.require('1.9.1')
import gc

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button


def create_lfunc(num, func):
    def ff(*args):
        func(num)
    return ff


class MainWidget(FloatLayout):
    alarm_stop = None
    correctanswer = None
    alarmactive = False
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for y in range(0, 2):
            for x in range(0, 5):
                self.add_widget(Button(text=str(y*5+x), on_press=create_lfunc(str(y*5+x),self.enter_num), pos_hint={"x": x*0.15, 'y': 0.3*(1-y)}, size_hint=(0.15, 0.3)))
    def enter_num(self, num):
        self.ids["calculationinput"].text += str(num)
        
    def alarm_start(self, question, correct_answer):
        self.correctanswer = correct_answer
        self.ids["calculationinput"].text = ""
        self.ids["calculationshow"].text = question
        self.ids["calculationinput"].focus = True
        App.get_running_app().root_window.show()
        App.get_running_app().root_window.raise_window()

    def enter_calc(self, *ll):
        if not self.alarmactive:
            return
        if self.question_answer.get() == self.correctanswer:
            self.ids["calculationinput"].text = ""
            self.ids["calculationshow"].text = "no question"
            self.alarm_stop()
        else:
            self.ids["calculationinput"].text = ""


class KivyApp(App):
    pass
def Gui(alarm_stop):
    # hack for stopping coredumps
    gc.set_debug(gc.DEBUG_SAVEALL)
    MainWidget.alarm_stop = alarm_stop
    return KivyApp()


