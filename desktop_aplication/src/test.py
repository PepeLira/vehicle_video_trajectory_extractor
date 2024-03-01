import cv2
import kivy
from kivy.app import App
from kivy.uix.image import Image

# an example code using kinvy and opencv to create a desktop application, just open a image with cv2 and show it with kinvy

class MyApp(App):
    def build(self):
        # Load the image using OpenCV
        image = cv2.imread('/home/pepe/Documents/vehicle_video_trajectory_extractor/desktop_aplication/src/a.jpg')

        # Create a Kivy Image widget
        img_widget = Image()

        # Convert the OpenCV image to a Kivy texture
        texture = kivy.graphics.texture.Texture.create(size=(image.shape[1], image.shape[0]))
        texture.blit_buffer(image.tobytes(), colorfmt='bgr', bufferfmt='ubyte')

        # Set the texture as the source for the Image widget
        img_widget.texture = texture

        # Return the Image widget as the root widget of the application
        return img_widget

if __name__ == '__main__':
    MyApp().run()