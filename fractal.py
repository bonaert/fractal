import os
import json

from PIL import Image


ITERATIONS_FILE_NAME = "iterations.data"
PIXEL_COLORS_FILE_NAME = "pixel.data"
IMAGE_FILE_NAME = "fractal.png"


DEPTH = 70



# Pas moi
import colorsys
colors_max = DEPTH + 1
# Calculate a tolerable palette
def generate_palette():
    palette = [0] * colors_max
    for i in range(colors_max):
        f = 1-abs((float(i)/colors_max-1)**15)
        r, g, b = colorsys.hsv_to_rgb(.66+f/3, 1-f/2, f)
        palette[i] = (int(r*255), int(g*255), int(b*255))
    return palette




class ImageGenerator:
    def __init__(self):
        self.X_SCALE = (-2.2, 2.2)
        self.Y_SCALE = (- 2.2, 2.2)

        self.X_SIZE = self.X_SCALE[1] - self.X_SCALE[0]
        self.Y_SIZE = self.Y_SCALE[1] - self.Y_SCALE[0]

        self.DIM = 100
        self.WIDTH = int(self.DIM * self.X_SIZE)
        self.HEIGHT = int(self.DIM * self.Y_SIZE)


        self.PALETTE = generate_palette()

    def evolution(self, val, constant):
        return val**2 + constant

    def is_inside_bounds(self, val):
        # Fast simple evaluation
        # return abs(val.real) < 2 and abs(val.imag) < 2

        # Slower, more precise version
        return abs(val) <= 2

    def num_iterations_until_escape(self, constant):
        num = 0+0*1j
        iterations = 0
        while self.is_inside_bounds(num) and iterations < DEPTH:
            num = self.evolution(num, constant)
            iterations += 1

        return iterations

    def get_colors(self, iterations):
        num = iterations
        return self.PALETTE[num]

    def make_image(self, pixels_colors):
        im = Image.new("RGB", (self.WIDTH, self.HEIGHT))
        im.putdata(pixels_colors)
        im.save(IMAGE_FILE_NAME,"PNG")

        return im

    def scale_x(self, x):
        # The Mandelbrot X scale is (-2.5, 1)
        return self.X_SCALE[0] + self.X_SIZE * (x / self.WIDTH)

    def scale_y(self, y):
        # The Mandelbrot Y scale is (-1, 1)
        return self.Y_SCALE[0] + self.Y_SIZE * (y / self.HEIGHT)


    def restore_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return None

    def compute_iterations(self):
        iterations = []
        for y in range(self.HEIGHT):
            print(y)
            scaled_y = self.scale_y(y)
            for x in range(self.WIDTH):
                scaled_x = self.scale_x(x)
                constant = scaled_x + scaled_y*1j
                num_iterations = self.num_iterations_until_escape(constant)
                iterations.append(num_iterations)
        return iterations

    def get_iterations(self, should_restore_from_file=True):
        data = None
        if should_restore_from_file:
            data = self.restore_from_file(ITERATIONS_FILE_NAME)

        if data is None:
            data = self.compute_iterations()

        return data

    def make_mandelbrot_image(self, restore_from_file=True):
        iterations = self.get_iterations(restore_from_file)
        print("Got iterations")
        colors_pixels = list(map(self.get_colors, iterations))
        print("Got pixel colors")

        with open(ITERATIONS_FILE_NAME, "w") as f:
            f.write(str(iterations))

        with open(PIXEL_COLORS_FILE_NAME, "w") as f:
            f.write(str(colors_pixels))
        
        print("Saved data")
        
        return self.make_image(colors_pixels)

    def zoom(self, factor = 0.5):
        self.X_SCALE = (factor * self.X_SCALE[0], factor * self.X_SCALE[1])
        self.Y_SCALE = (factor * self.Y_SCALE[0], factor * self.Y_SCALE[1])

        self.X_SIZE *= factor
        self.Y_SIZE *= factor

    def move_right(self, factor=0.3):
        x_adjust = self.X_SIZE * factor

        self.X_SCALE = tuple((x + x_adjust for x in self.X_SCALE))

    def move_left(self, factor=0.3):
        x_adjust = self.X_SIZE * factor

        self.X_SCALE = tuple((x - x_adjust for x in self.X_SCALE))
if __name__ == '__main__':
    image_generator = ImageGenerator()
    image = image_generator.make_mandelbrot_image()
    os.system("xdg-open " + IMAGE_FILE_NAME)
