from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.properties import ObjectProperty
import datetime
from kivy.metrics import dp

from kivy.storage.jsonstore import JsonStore

from kivy.core.audio import SoundLoader


class MainScreenWidget(BoxLayout):
    pass


class LeftGrid(GridLayout):

    store = JsonStore('todo.json')

    # store.put('todos', todos_list_key = [['Meditate',False]])

    # todos_list = [['Meditate',False]]
    todos_list = store.get('todos')['todos_list_key']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_text_input()
        self.init_todos()


    def init_text_input(self):

        def on_enter(instance):
            if instance.text != '' and len(self.todos_list) <=13:
                i , j  = instance.text, False
                self.todos_list.append([i,j])
                # self.store.put('todos', todos_list_key = self.todos_list_copy.append([i,j])) 
                # print(self.store.get('todos')['todos_list_key'])
                Clock.schedule_once(update)
                instance.text = ''

        def update(dt):
            if len(self.todos_list) >1 :
                self.clear_widgets(self.children[:-3])
            self.init_todos()
        
        l = Label(text='TODO' , size_hint=[0.15,1])
        self.add_widget(l)
        text_input = TextInput(text = '', multiline = False, text_validate_unfocus=False, font_size=20)
        text_input.bind(on_text_validate=on_enter)
        self.add_widget(text_input)
        def callback(instance):
            on_enter(text_input)
        add_button = Button(text='ADD', size_hint=[0.15,1])
        add_button.bind(on_press=callback)
        self.add_widget(add_button)

    def init_todos(self):
        for item, is_done in self.todos_list:
            def done_todo(instance):
                done_button_index = self.children.index(instance)
                self.todos_list[len(self.todos_list)- 1 -int((done_button_index-2)/3)][1] = True
                lab = self.children[done_button_index-1]
                lab.markup = True
                lab.text = '[s]'+ lab.text+'[/s]'
                lab.color = [0,1,0]
                instance.background_normal = ''
                instance.background_color = [0,1,1]
                instance.disabled = True
                
            done_button = Button(text ='Done', size_hint=[0.15,1])
            done_button.bind(on_press=done_todo)
            self.add_widget(done_button)
            if is_done:
                text = '[s]'+ item + '[/s]'
                markup = True
            else:
                text = item
                markup = False
            l=Label(text=text, markup = markup, color= [0, 1, 0] if is_done else [1,1,1], font_size = dp(20))
            self.add_widget(l)
            def delete_todo(instance):
                delete_button_index = self.children.index(instance)
                self.todos_list.pop(len(self.todos_list)- 1 -int(delete_button_index/3))
                self.clear_widgets(self.children[delete_button_index: delete_button_index+3])

            delete_button = Button(text ='Delete', size_hint=[0.15,1])
            delete_button.bind(on_press=delete_todo)
            self.add_widget(delete_button)

class RightGrid(GridLayout):

    focus_lab = ObjectProperty()
    focus_but = ObjectProperty()
    focus_sli = ObjectProperty()
    break_lab = ObjectProperty()
    break_but = ObjectProperty()
    break_sli = ObjectProperty()
    music_but = ObjectProperty()
    focus_count = 0
    break_count = 0

    sound_bell_alert = None
    sound_study_music = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_audio()

    def init_audio(self):
        self.sound_bell_alert = SoundLoader.load('audio/happy-bell-alert.wav')
        self.sound_study_music = SoundLoader.load('audio/Cantata.wav')

        self.sound_bell_alert.volume = 1
        self.sound_study_music.volume = 0.15
        self.sound_study_music.loop = True

    def convert_time(self, t):
        return str(datetime.timedelta(seconds = t))

    def init_focus_count(self):
        self.focus_count = int(self.focus_sli.value)*60
    
    def start_focus(self):
        if self.focus_but.state == 'down':
            self.sound_bell_alert.play()
        self.init_focus_count()
        def update1(dt):
            if self.focus_count >0 and self.focus_but.state == 'down':
                self.focus_count = int(self.focus_count - 1)
                self.focus_lab.text = self.convert_time(self.focus_count)

            elif self.focus_but.state == 'normal':
                Clock.unschedule(focus_clock)
                self.focus_lab.text = self.convert_time(0)
                # print('i stopped')
                self.sound_bell_alert.play()
            elif self.focus_count <= 0:
                self.focus_but.state = 'normal'
                self.sound_bell_alert.play()

        focus_clock=Clock.schedule_interval(update1, 1)

    def init_break_count(self):
        self.break_count = int(self.break_sli.value)*60
    
    def start_break(self):
        if self.break_but.state == 'down':
            self.sound_bell_alert.play()
        if self.focus_but.state == 'normal':
            self.init_break_count()
            def update2(dt):
                if self.break_count >0 and self.break_but.state == 'down':
                    self.break_count = int(self.break_count -1)
                    self.break_lab.text = self.convert_time(self.break_count)

                elif self.break_but.state == 'normal':
                    Clock.unschedule(break_clock)
                    self.break_lab.text = self.convert_time(0)
                    # print('i stopped')
                    self.sound_bell_alert.play()

                elif self.break_count <= 0:
                    self.break_but.state = 'normal'
                    self.sound_bell_alert.play()
            break_clock=Clock.schedule_interval(update2, 1)
    
    def start_music(self):
        if self.music_but.state == 'down':
            self.sound_study_music.play()
        elif self.music_but.state == 'normal':
            self.sound_study_music.stop()


class FocusApp(App):
    pass

if __name__ == "__main__":
    FocusApp().run()
    LeftGrid.store.put('todos', todos_list_key = LeftGrid.todos_list)


    
    


