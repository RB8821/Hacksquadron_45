import cv2
import mediapipe as mp
import numpy as np
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class PoseEstimationApp(App):
    def __init__(self, **kwargs):
        super(PoseEstimationApp, self).__init__(**kwargs)
        self.counter = 0
        self.stage = None
        self.cap = cv2.VideoCapture(0)
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        Clock.schedule_interval(self.update, 1.0/30.0)

    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Label for counter
        self.label = Label(text="0", color=(1, 1, 1, 1), size_hint=(1, 0.5), font_size='40sp', halign='center', valign='middle')
        layout.add_widget(self.label)

        # Buttons
        start_button = Button(text='Start', size_hint=(1, 0.1), background_color=(0.5, 0, 0.5, 1))
        start_button.bind(on_press=self.start_counter)
        layout.add_widget(start_button)

        stop_button = Button(text='Stop', size_hint=(1, 0.1), background_color=(0.5, 0, 0.5, 1))
        stop_button.bind(on_press=self.stop_counter)
        layout.add_widget(stop_button)

        restart_button = Button(text='Restart', size_hint=(1, 0.1), background_color=(0.5, 0, 0.5, 1))
        restart_button.bind(on_press=self.restart_counter)
        layout.add_widget(restart_button)

        exit_button = Button(text='Exit', size_hint=(1, 0.1), background_color=(0.5, 0, 0.5, 1))
        exit_button.bind(on_press=self.exit_app)
        layout.add_widget(exit_button)

        return layout

    def update(self, dt):
        ret, frame = self.cap.read()
        
        if not ret:
            return

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            angle = self.calculate_angle(shoulder, elbow, wrist)
            
            cv2.putText(image, str(angle), tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
            if angle > 160:
                self.stage = "down"
            if angle < 30 and self.stage == 'down':
                self.stage = "up"
                self.counter += 1
                self.label.text = str(self.counter)
                
        except Exception as e:
            print("Exception:", e)

        cv2.imshow('Mediapipe Feed', image)

    def calculate_angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

    def start_counter(self, instance):
        self.counter = 0
        self.stage = None
        self.label.text = "0"

    def stop_counter(self, instance):
        pass

    def restart_counter(self, instance):
        self.start_counter(instance)

    def exit_app(self, instance):
        self.cap.release()
        cv2.destroyAllWindows()
        App.get_running_app().stop()

if __name__ == '__main__':
    PoseEstimationApp().run()
