from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image

class ClickableImageApp(App):
    def build(self):
        # Create a Button with an Image as its background
        button = Button(background_normal='new.png', background_down='image_clicked.png')
        button.bind(on_press=self.on_button_click)
        return button

    def on_button_click(self, instance):
        print("Image clicked!")

if __name__ == '__main__':
    ClickableImageApp().run()