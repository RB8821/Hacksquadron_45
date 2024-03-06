import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import random

class FitnessChatbot(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fitness_responses = {
            "workout": ["Exercise is important for maintaining good health.", 
                        "What type of workout are you interested in?"],
            "diet": ["Eating a balanced diet is essential for overall health.",
                     "Are you looking for information on a specific diet?"],
            "weight loss": ["Weight loss is often achieved through a combination of diet and exercise.",
                            "Have you considered consulting a nutritionist or personal trainer?"],
            "muscle building": ["Strength training exercises can help build muscle mass.",
                                "Are you interested in bodyweight exercises or weightlifting?"],
            # Add more responses as needed
        }
        self.conversation_history = []

    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Conversation history scroll view
        self.conversation_scroll = ScrollView()
        self.conversation_layout = BoxLayout(orientation='vertical')
        self.conversation_scroll.add_widget(self.conversation_layout)
        layout.add_widget(self.conversation_scroll)

        # User input text input
        self.user_input = TextInput(hint_text='Type your message here...')
        self.user_input.bind(on_text_validate=self.send_message)
        layout.add_widget(self.user_input)

        return layout

    def send_message(self, instance):
        user_message = self.user_input.text
        self.user_input.text = ''
        self.add_message('User', user_message)

        response = self.get_response(user_message)
        self.add_message('FitnessChatbot', response)

    def add_message(self, sender, message):
        label = Label(text=f'{sender}: {message}')
        self.conversation_layout.add_widget(label)
        self.conversation_scroll.scroll_to(label)

    def get_response(self, user_message):
        for query, answers in self.fitness_responses.items():
            if query in user_message:
                return random.choice(answers)
        return "I'm sorry, I didn't understand that."

if __name__ == "__main__":
    FitnessChatbot().run()
