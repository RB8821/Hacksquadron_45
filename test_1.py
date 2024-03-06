from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle

# Basic UI of the App 
class ColoredLabel(Label):
    def __init__(self, **kwargs):
        super(ColoredLabel, self).__init__(**kwargs)
        with self.canvas.before:
            Color(148/255, 0, 211/255, 1)  # Purple color
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class HomeScreen(Screen):
    pass

class ExerciseScreen(Screen):
    pass

class PushUpCounterScreen(Screen):
    def __init__(self, **kwargs):
        super(PushUpCounterScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20)  # Adjust spacing here
        label = Label(text="Push UP Counter", font_size=30, color=(1, 1, 1, 1))  # Set label color to white
        label.background_color = (0.5, 0, 1, 1)  # Set label background color to purple
        image = Image(source="Push-up.png")
        start_button = Button(text="Start Push up Counter", background_color=(0.5, 0, 1, 1))  # Set button background color to purple
        exit_button = Button(text="Exit", background_color=(0.5, 0, 1, 1))  # Set button background color to purple
        start_button.bind(on_press=self.start_push_up_counter)
        exit_button.bind(on_press=self.exit_app)
        layout.add_widget(label)
        layout.add_widget(image)
        layout.add_widget(start_button)
        layout.add_widget(exit_button)
        self.add_widget(layout)

    def start_push_up_counter(self, instance):
        self.manager.current = 'home'

    def exit_app(self, instance):
        App.get_running_app().stop()

class ClickableImageApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        # Home Screen
        home_screen = HomeScreen(name='home')
        root_layout = BoxLayout(orientation='vertical')

        # Upper Part
        upper_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        
        notification_button = Button(background_normal='notification.png', background_down='notification_clicked.png', size_hint=(0.15, 1))
        upper_layout.add_widget(notification_button)

        label = ColoredLabel(text="Fitness App", size_hint=(0.7, 1), font_size=28, bold=True, italic=True)
        upper_layout.add_widget(label)

        profile_button = Button(background_normal='profile.png', background_down='profile_clicked.png', size_hint=(0.15, 1))
        upper_layout.add_widget(profile_button)

        root_layout.add_widget(upper_layout)

        # Middle Part
        middle_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.6))
        middle_layout.background_color = (1, 1, 1, 1)

        exercise_button = Button(text="Exercise rep counter", size_hint=(0.8, 1), background_color=(1, 1, 1, 1), border=(1, 1, 1, 1),background_normal='workout.png', background_down='workout_clicked.png')
        exercise_button.bind(on_release=self.show_push_up_counter_screen)
        middle_layout.add_widget(exercise_button)

        root_layout.add_widget(middle_layout)

        # Lower Part
        lower_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        lower_layout.background_color = (148/255, 0, 211/255, 1)

        coach_button = Button(background_normal='coach.png', background_down='coach_clicked.png', size_hint=(0.33, 1))
        lower_layout.add_widget(coach_button)

        todo_button = Button(background_normal='todo.png', background_down='todo_clicked.png', size_hint=(0.33, 1))
        lower_layout.add_widget(todo_button)

        planner_button = Button(background_normal='planner.png', background_down='planner_clicked.png', size_hint=(0.33, 1))
        lower_layout.add_widget(planner_button)

        root_layout.add_widget(lower_layout)

        home_screen.add_widget(root_layout)
        self.screen_manager.add_widget(home_screen)

        # Exercise Screen
        exercise_screen = ExerciseScreen(name='exercise')
        exercise_layout = BoxLayout(orientation='vertical')

        exercise_image = Image(source='workout.png')
        exercise_layout.add_widget(exercise_image)

        push_up_button = Button(text='Push up counter', background_color=(148/255, 0, 211/255, 1))
        push_up_button.bind(on_release=self.show_push_up_counter_screen)
        exercise_layout.add_widget(push_up_button)

        pull_up_button = Button(text='Pull up counter', background_color=(148/255, 0, 211/255, 1))
        pull_up_button.bind(on_release=self.go_back_home)
        exercise_layout.add_widget(pull_up_button)

        bicep_curl_button = Button(text='Bicep Curl Counter', background_color=(148/255, 0, 211/255, 1))
        bicep_curl_button.bind(on_release=self.go_back_home)
        exercise_layout.add_widget(bicep_curl_button)

        exit_button = Button(text='Exit', background_color=(148/255, 0, 211/255, 1))
        exit_button.bind(on_release=self.go_back_home)
        exercise_layout.add_widget(exit_button)

        exercise_screen.add_widget(exercise_layout)
        self.screen_manager.add_widget(exercise_screen)
        return self.screen_manager

    def show_push_up_counter_screen(self, instance):
        push_up_counter_screen = PushUpCounterScreen(name='push_up_counter')
        self.screen_manager.add_widget(push_up_counter_screen)
        self.screen_manager.current = 'push_up_counter'

    def go_back_home(self, instance):
        self.screen_manager.current = 'home'

if __name__ == '__main__':
    ClickableImageApp().run()


