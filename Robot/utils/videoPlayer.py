import os
import time
from PIL import Image, ImageDraw, ImageFont
import ST7735 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import os
import threading

# Constants
WIDTH = 128
HEIGHT = 160
SPEED_HZ = 16000000

# Raspberry Pi configuration.
DC = 24
RST = 25
SPI_PORT = 0
SPI_DEVICE = 0

class Animate():

    def __init__(self):
        self.disp = TFT.ST7735(
            DC,
            rst=RST,
            spi=SPI.SpiDev(
                SPI_PORT,
                SPI_DEVICE,
                max_speed_hz=SPEED_HZ)
        )

        self.disp.begin()
        print("display initialized")
        self.animation_thread = None
        self.animation_stop_event = threading.Event()


    def convert_rgb_to_bgr(self, image):
        r, g, b = image.split()
        return Image.merge("RGB", (b, g, r))

    # Function to load and display an image
    def display_image(self, image_path):
        try:
            # Open the image file
            image = Image.open(image_path)

            # Ensure image is in RGB mode
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Resize image to fit display, maintaining aspect ratio
            image.thumbnail((WIDTH, HEIGHT), Image.LANCZOS)

            # Create a blank image with the size of the display
            display_image = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
            # Calculate position to center the image
            x_pos = (WIDTH - image.width) // 2
            y_pos = (HEIGHT - image.height) // 2

            # Paste the resized image onto the display image
            display_image.paste(image, (x_pos, y_pos))

            # Rotate image to fit the display orientation
            display_image = display_image.rotate(90)

            display_image = self.convert_rgb_to_bgr(display_image)

            # Clear the display
            self.disp.clear((0, 0, 0))

            # Display the image on the screen
            self.disp.display(display_image)

        except Exception as e:
            print(f"Error displaying image {image_path}: {e}")

    def play_animation(self, animation_folder):
        print("Playing animation:", animation_folder)
        if self.animation_thread and self.animation_thread.is_alive():
            self.animation_stop_event.set()  # Set stop event to terminate current animation thread
            self.animation_thread.join()

        # Start a new animation thread
        self.animation_stop_event.clear()
        self.animation_thread = threading.Thread(target=self._animation_worker, args=(animation_folder,))
        self.animation_thread.start()

    def display_text(self, text, font_path=None, font_size=20):
        if self.animation_thread and self.animation_thread.is_alive():
            self.animation_stop_event.set()  # Set stop event to terminate current animation thread
            self.animation_thread.join()

        # Start a new animation thread
        self.animation_stop_event.clear()
        self.animation_thread = threading.Thread(target=self._text_worker, args=(text, font_path, font_size))
        self.animation_thread.start()
        
        # Main loop to display images in sequence
    def _animation_worker(self, image_folder:str):
        print("playing animation", image_folder)
        frame_number = 1
        animation_path = os.path.join(os.path.dirname(__file__), '..','..', 'Animation', image_folder)
        while not self.animation_stop_event.is_set():
            image_path = os.path.join(animation_path, f'{image_folder} ({frame_number}).jpg')
            if os.path.exists(image_path):
                self.display_image(image_path)
                frame_number += 1
            else:
                if image_folder == "Neutral Static" or image_folder == "Start":
                    frame_number = 1  # Reset to first frame if the last frame is reached
                else:
                    break

    def _text_worker(self, text, font_path=None, font_size=20):
        try:
            # Create a blank image for the text
            image = Image.new('RGB', (HEIGHT, WIDTH), (0, 0, 0))  # Note the swapped dimensions
            draw = ImageDraw.Draw(image)

            # Use a truetype font if specified, else use a default bitmap font
            if font_path:
                font = ImageFont.truetype(font_path, font_size)
            else:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)

            # Calculate text size and position to center it
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # Calculate position to center the text
            text_x = (HEIGHT - text_width) // 2
            text_y = (WIDTH - text_height) // 2

            # Draw the text
            draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))

            # Rotate the image to fit the display orientation
            rotated_image = image.rotate(90, expand=True)

            # Display the image
            self.disp.display(rotated_image)

        except Exception as e:
            print(f"Error displaying text: {e}")
