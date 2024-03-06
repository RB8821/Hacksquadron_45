import cv2
import mediapipe as mp
import math
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class PushupCounterApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)  # Set window background color to white

        self.count = 0
        self.position = None
        self.threshold_angle = 90  # Threshold angle for counting a push-up (less than 90 degrees)
        self.cap = cv2.VideoCapture(0)
        self.running = False

        layout = FloatLayout()

        self.pushup_count_label = Button(text="Pull-ups: 0", background_color=(0.2, 0.2, 0.6, 1), color=(1, 1, 1, 1))
        self.angle_label = Button(text="Angle: 0.00 degrees", background_color=(0.2, 0.2, 0.6, 1), color=(1, 1, 1, 1))
        self.start_button = Button(text="Start", background_color=(0.6, 0.2, 0.6, 1), color=(1, 1, 1, 1))
        self.stop_button = Button(text="Stop", background_color=(0.6, 0.2, 0.6, 1), color=(1, 1, 1, 1))
        self.back_button = Button(text="Back", background_color=(0.6, 0.2, 0.6, 1), color=(1, 1, 1, 1))

        self.pushup_count_label.size_hint = (0.8, 0.1)
        self.angle_label.size_hint = (0.8, 0.1)
        self.start_button.size_hint = (0.4, 0.1)
        self.stop_button.size_hint = (0.4, 0.1)
        self.back_button.size_hint = (0.4, 0.1)

        self.pushup_count_label.pos_hint = {'center_x': 0.5, 'top': 0.9}
        self.angle_label.pos_hint = {'center_x': 0.5, 'top': 0.8}
        self.start_button.pos_hint = {'center_x': 0.25, 'y': 0.6}
        self.stop_button.pos_hint = {'center_x': 0.75, 'y': 0.6}
        self.back_button.pos_hint = {'center_x': 0.5, 'y': 0.2}

        self.start_button.bind(on_press=self.start_counter)
        self.stop_button.bind(on_press=self.stop_counter)
        self.back_button.bind(on_press=self.stop_app)

        layout.add_widget(self.pushup_count_label)
        layout.add_widget(self.angle_label)
        layout.add_widget(self.start_button)
        layout.add_widget(self.stop_button)
        layout.add_widget(self.back_button)

        Clock.schedule_interval(self.update, 1.0/30.0)  # Update UI at 30fps

        return layout

    def start_counter(self, instance):
        self.running = True

    def stop_counter(self, instance):
        self.running = False

    def stop_app(self, instance):
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()
        App.get_running_app().stop()

    def update(self, dt):
        if self.running:
            success, image = self.cap.read()
            if not success:
                print("Empty camera ")
                return

            with mp_pose.Pose(
                    min_detection_confidence=0.7,
                    min_tracking_confidence=0.7) as pose:

                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                result = pose.process(image)

                if result.pose_landmarks:
                    mp_drawing.draw_landmarks(
                        image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    landmarks = result.pose_landmarks.landmark
                    if landmarks[12].visibility > 0 and landmarks[14].visibility > 0:  # Check visibility of shoulder and elbow landmarks
                        # Calculate the angle between shoulder, elbow, and wrist
                        angle = math.degrees(math.atan2(landmarks[14].y - landmarks[12].y, landmarks[14].x - landmarks[12].x) -
                                            math.atan2(landmarks[16].y - landmarks[14].y, landmarks[16].x - landmarks[14].x))
                        angle = angle + 360 if angle < 0 else angle
                        if angle > 180:
                            angle = 360 - angle

                        if angle < self.threshold_angle and self.position != "down":
                            self.position = "down"  # Mark the start of the down phase
                        elif angle > self.threshold_angle and self.position == "down":
                            self.position = "up"  # Mark the start of the up phase, count as a push-up
                            self.count += 1
                            self.pushup_count_label.text = f"Push-ups: {self.count}"
                            print("Push-up count:", self.count)

                        self.angle_label.text = f"Angle: {angle:.2f} degrees"

                cv2.imshow("Push-up counter", image)

        key = cv2.waitKey(1)
        if key == ord('q'):
            self.stop_app(None)

if __name__ == '__main__':
    PushupCounterApp().run()
