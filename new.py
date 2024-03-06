from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
import cv2
import mediapipe as md

md_drawing = md.solutions.drawing_utils
md_pose = md.solutions.pose

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
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
        self.manager.current = 'counter'

    def exit_app(self, instance):
        App.get_running_app().stop()

class PushUpCounterScreen(Screen):
    def __init__(self, **kwargs):
        super(PushUpCounterScreen, self).__init__(**kwargs)
        self.count = 0
        self.position = None
        self.cap = cv2.VideoCapture(0)
        self.pose = md_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        layout = BoxLayout(orientation='vertical', spacing=20)  # Adjust spacing here
        start_button = Button(text='Start', background_color=(0.5, 0, 1, 1))  # Set button background color to purple
        stop_button = Button(text='Stop', background_color=(0.5, 0, 1, 1))  # Set button background color to purple
        reset_button = Button(text='Reset', background_color=(0.5, 0, 1, 1))  # Set button background color to purple
        back_button = Button(text='Back', background_color=(0.5, 0, 1, 1))  # Set button background color to purple

        layout.add_widget(start_button)
        layout.add_widget(stop_button)
        layout.add_widget(reset_button)
        layout.add_widget(back_button)

        start_button.bind(on_press=self.start_counter)
        stop_button.bind(on_press=self.stop_counter)
        reset_button.bind(on_press=self.reset_counter)
        back_button.bind(on_press=self.back_to_home)

        self.add_widget(layout)

    def start_counter(self, instance):
        Clock.schedule_interval(self.update_frame, 1 / 30.)

    def update_frame(self, dt):
        success, image = self.cap.read()
        if not success:
            print("Empty Camera")
            return
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        result = self.pose.process(image)
        imlist = []
        if result.pose_landmarks:
            md_drawing.draw_landmarks(
                image, result.pose_landmarks, md_pose.POSE_CONNECTIONS)
            for id, im in enumerate(result.pose_landmarks.landmark):
                h, w, _ = image.shape
                X, Y = int(im.x * w), int(im.y * h)
                imlist.append([id, X, Y])
        if len(imlist) != 0:
            if imlist[12][2] >= imlist[14][2] and imlist[11][2] >= imlist[13][2]:
                self.position = "down"
            if imlist[12][2] <= imlist[14][2] and imlist[11][2] <= imlist[13][2] and self.position == "down":
                self.position = 'up'
                self.count += 1
                print(self.count)

        cv2.imshow("Push-up Counter", cv2.flip(image, 1))
        key = cv2.waitKey(30)
        if key == ord('q'):
            self.stop_counter(None)

    def stop_counter(self, instance):
        Clock.unschedule(self.update_frame)

    def reset_counter(self, instance):
        self.count = 0

    def back_to_home(self, instance):
        self.stop_counter(None)
        self.cap.release()
        cv2.destroyAllWindows()
        self.manager.current = 'home'

    def show_push_up_screen(self):
        self.manager.current = 'push_up_counter'

class PushUpCounterApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical')
        sm = ScreenManager()
        home_screen = HomeScreen(name='home')
        counter_screen = PushUpCounterScreen(name='counter')
        push_up_screen = Screen(name='push_up_counter')
        sm.add_widget(home_screen)
        sm.add_widget(counter_screen)
        sm.add_widget(push_up_screen)
        self.root.add_widget(sm)
        return self.root

if __name__ == '__main__':
    PushUpCounterApp().run()
