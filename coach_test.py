import kivy
import subprocess
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

class FitnessApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Title Layout with purple background
        title_layout = BoxLayout(size_hint=(1, 0.1))
        with title_layout.canvas.before:
            Color(0.5, 0, 0.5, 1)  # purple background color
            self.rect = Rectangle(size=title_layout.size, pos=title_layout.pos)
        layout.add_widget(title_layout)

        # Title Label
        self.title_label = Label(text='')
        title_layout.add_widget(self.title_label)

        # Body Layout with white background
        body_layout = GridLayout(cols=1, spacing=10, padding=10)
        with body_layout.canvas.before:
            Color(1, 1, 1, 1)  # white background
            self.rect = Rectangle(size=body_layout.size, pos=body_layout.pos)
        layout.add_widget(body_layout)

        # Button 1: Workout Tutorial and Pose Detection with purple background
        button1 = Button(text='Workout Tutorial and Pose Detection', size_hint=(1, 0.3),
                         background_color=(0.5, 0, 0.5, 1))
        button1.bind(on_press=self.workout_tutorial)
        body_layout.add_widget(button1)

        # Button 2: Chatbot with purple background
        button2 = Button(text='Chatbot', size_hint=(1, 0.3), background_color=(0.5, 0, 0.5, 1))
        button2.bind(on_press=self.open_chatbot)
        body_layout.add_widget(button2)

        # Button 3: Exit with purple background
        button3 = Button(text='Exit', size_hint=(1, 0.3), background_color=(0.5, 0, 0.5, 1))
        button3.bind(on_press=self.exit_app)
        body_layout.add_widget(button3)

        # Start auto typing animation
        Clock.schedule_once(self.autotype, 1)

        return layout

    def autotype(self, dt):
        self.autotype_text = "Hi! I'm your coach and I'll assist you in your fitness journey."
        self.index = 0
        Clock.schedule_interval(self.type_character, 0.1)

    def type_character(self, dt):
        if self.index < len(self.autotype_text):
            self.title_label.text += self.autotype_text[self.index]
            self.index += 1
        else:
            Clock.unschedule(self.type_character)

    def workout_tutorial(self, instance):
        # Define the action for the first button here
        print("Opening Workout Tutorial and Pose Detection")

    def open_chatbot(self, instance):
        # Define the action for the second button here
        print("Opening Chatbot")
        subprocess.Popen(["python", "chatbot.py"])

    def exit_app(self, instance):
        # Define the action for the third button here
        print("Exiting Fitness Application")
        App.get_running_app().stop()

if __name__ == '__main__':
    FitnessApp().run()
