from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import os

class RoyaltonApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # 1. Logo
        self.layout.add_widget(Image(source='logo.png', size_hint_y=None, height=200))
        
        # 2. Search Bar
        self.search_input = TextInput(hint_text='Search Student Name...', size_hint_y=None, height=50, multiline=False)
        self.search_input.bind(text=self.update_suggestions)
        self.layout.add_widget(self.search_input)
        
        # 3. Suggestion Area (Scrollable)
        self.scroll = ScrollView()
        self.suggestion_box = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.suggestion_box.bind(minimum_height=self.suggestion_box.setter('height'))
        self.scroll.add_widget(self.suggestion_box)
        self.layout.add_widget(self.scroll)
        
        # 4. Status Label
        self.status = Label(text="Ready", color=(0, 1, 0, 1))
        self.layout.add_widget(self.status)
        
        return self.layout

    def update_suggestions(self, instance, value):
        self.suggestion_box.clear_widgets()
        if value:
            if os.path.exists('student_qrs'):
                for file in os.listdir('student_qrs'):
                    if value.lower() in file.lower():
                        name = file.replace('_', ' ').replace('.png', '')
                        btn = Button(text=name, size_hint_y=None, height=50)
                        btn.bind(on_release=lambda x: self.process_scan(x.text))
                        self.suggestion_box.add_widget(btn)

    def process_scan(self, student_name):
        self.status.text = f"Logged: {student_name}"
        # Here we would add the database saving logic
        print(f"Student {student_name} clocked in!")

if __name__ == '__main__':
    RoyaltonApp().run()