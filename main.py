from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
import os
from kivy.core.window import Window
from kivy.config import Config

class Root(BoxLayout):
    nextImage1 = ObjectProperty(None)
    nextImage2 = ObjectProperty(None)
    nextImage3 = ObjectProperty(None)
    nextImage4 = ObjectProperty(None)
    nextImage5 = ObjectProperty(None)
    prevImage = ObjectProperty(None)
    currentImage = ObjectProperty(None)
    currentFilename = ObjectProperty(None)
    currentMove = ObjectProperty(None)
    textUp = ObjectProperty(None)
    textLeft = ObjectProperty(None)
    textRight = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.maximize()
        self.index = 1
        self.states = ("FR", "GV", "TS", "WAIT")
        self.state = self.states[3]
        self.directory = ''
        self.files = []
        self.lastMove = ['', '', '']

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            pass
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def _on_keyboard_up(self, keyboard, keycode):
        new_state = ''
        if self.state == self.states[3]:
            pass
        if 'backspace' in keycode:
            #roll back current
            pass
        if 'left' in keycode:
            if self.state == self.states[0]:
                new_state = 1
                self.files[self.index]["move0"] = 'F'
            if self.state == self.states[1]:
                new_state = 2
                self.files[self.index]["move1"] = 'G'
            if self.state == self.states[2]:
                new_state = 0
                self.files[self.index]["move2"] = 'T'
                self.finish_classification()
        if 'right' in keycode:
            if self.state == self.states[0]:
                new_state = 1
                self.files[self.index]["move0"] = 'R'
            if self.state == self.states[1]:
                new_state = 2
                self.files[self.index]["move1"] = 'V'
            if self.state == self.states[2]:
                new_state = 0
                self.files[self.index]["move2"] = 'S'
                self.finish_classification()
        if ('up' in keycode) and (self.state != self.states[3]):
            new_state = 0
            self.files[self.index]["move0"] = self.lastMove[0]
            self.files[self.index]["move1"] = self.lastMove[1]
            self.files[self.index]["move2"] = self.lastMove[2]
            self.finish_classification()
            
        if not self.state == self.states[3]:
            self.currentMove.text = f'{self.files[self.index]["move0"]} {self.files[self.index]["move1"]} {self.files[self.index]["move2"]}'   
            if self.index >= len(self.files):
                new_state = 3
            if new_state != '':
                self.change_state(new_state)

    def finish_classification(self):
        self.lastMove[0] = self.files[self.index]["move0"]
        self.lastMove[1] = self.files[self.index]["move1"]
        self.lastMove[2] = self.files[self.index]["move2"]
        self.textUp.text = f'{self.lastMove[0]} {self.lastMove[1]} {self.lastMove[2]}'

        self.index += 1
        self.show_images()

    def change_state(self, index):
        if index == 0:
            self.textLeft.text = 'F'
            self.textRight.text = 'R'
        if index == 1:
            self.textLeft.text = 'G'
            self.textRight.text = 'V'
        if index == 2:
            self.textLeft.text = 'T'
            self.textRight.text = 'S'
        if index == 3:
            self.textLeft.text = ''
            self.textRight.text = ''
            self.textUp.text = ''
        self.state = self.states[index]

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load Folder", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, directory):
        self.files = []
        self.directory = directory
        extensions = ['png', 'jpg', 'jpeg', 'gif']
        for file in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, file)):
                continue
            if not file.split('.')[1] in extensions:
                continue
            entry = {'filename': file, 'move0': '-', 'move1': '-', 'move2': '-'}
            self.files.append(entry)
            self.change_state(0)
        self.dismiss_popup()
        self.show_images()

    def get_next_index(self):
        for i in range(len(self.files)):
            if self.files[i]["move0"] == '-':
                self.index = i
                return False
        return True

    def show_images(self):
        finished = self.get_next_index()
        
        if finished:
            self.prevImage.opacity = 0
            self.currentImage.opacity = 0
            self.nextImage1.opacity = 1
            self.nextImage2.opacity = 1
            self.nextImage3.opacity = 1
            self.nextImage4.opacity = 1
            self.nextImage5.opacity = 1
            self.change_state(3)
            pass
                
        if self.index > 0:
            self.prevImage.source = os.path.join(self.directory, self.files[self.index -1]["filename"])
            self.prevImage.opacity = 1

        if self.index < len(self.files):
            self.currentImage.source = os.path.join(self.directory, self.files[self.index]["filename"])
            self.currentImage.opacity = 1
            self.currentFilename.text = self.files[self.index]["filename"]
        else:
            self.currentImage.opacity = 0    
        if self.index + 1 < len(self.files):
            self.nextImage1.source = os.path.join(self.directory, self.files[self.index+1]["filename"])
            self.nextImage1.opacity = 1
        else:
            self.nextImage1.opacity = 0

        if self.index + 2 < len(self.files):
            self.nextImage2.source = os.path.join(self.directory, self.files[self.index+2]["filename"])
            self.nextImage2.opacity = 1
        else:
            self.nextImage2.opacity = 0

        if self.index + 3 < len(self.files):
            self.nextImage3.source = os.path.join(self.directory, self.files[self.index+3]["filename"])
            self.nextImage3.opacity = 1
        else:
            self.nextImage3.opacity = 0

        if self.index + 4 < len(self.files):
            self.nextImage4.source = os.path.join(self.directory, self.files[self.index+4]["filename"])
            self.nextImage4.opacity = 1
        else:
            self.nextImage4.opacity = 0

        if self.index + 5 < len(self.files):
            self.nextImage5.source = os.path.join(self.directory, self.files[self.index+5]["filename"])
            self.nextImage5.opacity = 1
        else:
            self.nextImage5.opacity = 0

    def show_history(self):
        content = History(cancel_action=self.cancel_action, confirm_movement=self.confirm_movement ,cancel=self.dismiss_popup)
        #if self.state != self.states[3]:
        if True:
            for file in self.files:
                grid = content.children[0].children[2].children[0] 
                image = Image(source=os.path.join(self.directory, file["filename"]), allow_stretch=True, size_hint=(1, 10))
                
                grid.add_widget(image)

                bl1 = BoxLayout(orientation='vertical', size_hint=(1/20, 1))
                label = Label(text=file["move0"], size_hint=(1, None), height=30)
                bl1.add_widget(Widget())
                bl1.add_widget(label)
                bl1.add_widget(Widget())
                grid.add_widget(bl1)
                

                bl2 = BoxLayout(orientation='vertical', size_hint=(1/20, 1))
                label = Label(text=file["move1"], size_hint=(1, None), height=30)
                bl2.add_widget(Widget())
                bl2.add_widget(label)
                bl2.add_widget(Widget())
                grid.add_widget(bl2)
                
                bl2 = BoxLayout(orientation='vertical', size_hint=(1/20, 1))
                label = Label(text=file["move2"], size_hint=(1, None), height=30)
                bl2.add_widget(Widget())
                bl2.add_widget(label)
                bl2.add_widget(Widget())
                grid.add_widget(bl2)

                bl = BoxLayout(orientation='vertical')
                bl.add_widget(Widget())
                button = UndoButton(text='Undo', size_hint = (1/5, None), size=(0, 30), on_release=self.cancel_action, filename=file["filename"])
                bl.add_widget(button)
                bl.add_widget(Widget())
                grid.add_widget(bl)
                
                #content.children[0].children[1].children[0].add_widget(bl)
                
            #widget = Widget()
            #content.children[0].children[1].children[0].add_widget(widget)     

        self._popup = Popup(title="History", content=content, size_hint=(None, 0.9), size=("600dp", 0))
        self._popup.open()

    def confirm_movement(self):
        for i in range(len(self.files)):
            file = self.files[i]
            if file["move0"] != '-':
                directory = self.directory
                self.move_file(file["filename"], file["move0"])
                self.move_file(file["filename"], file["move1"])
                self.move_file(file["filename"], file["move2"])
                self.move_file(file["filename"], "backup")
                os.system(f'rm {os.path.join(self.directory, file["filename"])}')
        self.dismiss_popup()
        self.load(self.directory)

    def move_file(self, filename, classification):
        if not os.path.isdir(os.path.join(self.directory, classification)):
            os.system(f'mkdir {os.path.join(self.directory, classification)}')
        os.system(f'cp {os.path.join(self.directory, filename)} {os.path.join(self.directory, classification, filename)}')

    def cancel_action(self, button):
        for i in range(len(self.files)):
            if self.files[i]["filename"] == button.filename:
                self.files[i]["move0"] = "-"
                self.files[i]["move1"] = "-"
                self.files[i]["move2"] = "-"
        self.dismiss_popup()
        self.show_history()
        self.show_images()
        
    def show_settings(self):
        pass

    def dismiss_popup(self):
        self._popup.dismiss()
    
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    def is_dir(self, directory, filename):
        return os.path.isdir(os.path.join(directory, filename))

class History(FloatLayout):
    cancel = ObjectProperty(None)
    confirm_movement = ObjectProperty(None)
    cancel_action = ObjectProperty(None)

class UndoButton(Button):
    filename = ObjectProperty(None)

class PictureMoverApp(App):
    def build(self):
        return Root()

if __name__ == "__main__":
    
    PictureMoverApp().run()
