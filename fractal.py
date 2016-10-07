import os
import json

from PIL import Image

from time import time

ITERATIONS_FILE_NAME = "iterations.data"
PIXEL_COLORS_FILE_NAME = "pixel.data"
IMAGE_FILE_NAME = "fractal.png"

DEPTH = 80

# Pas moi
import colorsys

colors_max = DEPTH + 1


# Calculate a tolerable palette
def generate_palette():
    palette = [0] * colors_max
    for i in range(colors_max):
        f = 1 - abs((float(i) / colors_max - 1) ** 15)
        r, g, b = colorsys.hsv_to_rgb(.66 + f / 3, 1 - f / 2, f)
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))
    return palette


class ImageGenerator:
    def __init__(self):
        self.X_SCALE = (-2.2, 2.2)
        self.Y_SCALE = (- 2.2, 2.2)

        self.X_SIZE = self.X_SCALE[1] - self.X_SCALE[0]
        self.Y_SIZE = self.Y_SCALE[1] - self.Y_SCALE[0]

        self.DIM = 80
        self.WIDTH = 500  # int(self.DIM * self.X_SIZE)
        self.HEIGHT = 500  # int(self.DIM * self.Y_SIZE)

        self.PALETTE = generate_palette()

    def evolution(self, val, constant):
        return val ** 2 + constant

    def is_inside_bounds(self, val):
        return (val.real * val.real + val.imag * val.imag) <= 4

    def num_iterations_until_escape(self, constant):
        iterations = 0
        val = 0j
        while val.real * val.real + val.imag * val.imag <= 4 and iterations < DEPTH:
            val = val ** 2 + constant
            iterations += 1

        return iterations

    def make_image(self, pixels_colors):
        im = Image.new("RGB", (self.WIDTH, self.HEIGHT))
        im.putdata(pixels_colors)
        #im.save(IMAGE_FILE_NAME, "PNG")

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

    def compute_iterations2(self):
        iterations = []
        for y in range(self.HEIGHT):
            scaled_y = self.scale_y(y)
            for x in range(self.WIDTH):
                scaled_x = self.scale_x(x)
                constant = scaled_x + scaled_y * 1j
                num_iterations = self.num_iterations_until_escape(constant)
                iterations.append(num_iterations)
        return iterations

    def compute_iterations(self):
        os.system("./generate %f %f %f %f" % (self.X_SCALE[0], self.Y_SCALE[0], self.X_SCALE[1], self.Y_SCALE[1]))
        iterations = []
        with open("iterations.txt") as f:
            for line in f:
                line = line.strip().split()
                line = list(map(int, line))
                iterations.extend(line)

        return iterations

    def get_iterations(self, should_restore_from_file=True):
        return self.compute_iterations()

    def make_mandelbrot_image(self, restore_from_file=True):
        start = time()
        iterations = self.get_iterations(restore_from_file)
        end = time()
        print("It took %f seconds to generate the numbers" % (end - start))



        start = time()
        colors_pixels = [self.PALETTE[num] for num in iterations]
        end = time()
        print("It took %f seconds to get the colors" % (end - start))
    
        start = time()
        image = self.make_image(colors_pixels)
        end = time()
        print("It took %f seconds to generate the image" % (end - start))

        return image

    def zoom(self, factor=0.5):

        x_center = self.X_SCALE[0] + self.X_SIZE / 2
        y_center = self.Y_SCALE[0] + self.Y_SIZE / 2

        self.X_SIZE *= factor
        self.Y_SIZE *= factor
        
        self.X_SCALE = (x_center - self.X_SIZE / 2, x_center + self.X_SIZE / 2)
        self.Y_SCALE = (y_center - self.Y_SIZE / 2, y_center + self.Y_SIZE / 2)


    def move(self, factorX=1.0, factorY=1.0):
        x_adjust = self.X_SIZE * factorX
        self.X_SCALE = tuple((x + x_adjust for x in self.X_SCALE))

        y_adjust = self.Y_SIZE * factorY
        # The Y-axis in the opposite direction than the usual
        # Cartesian graph
        self.Y_SCALE = tuple((y - y_adjust for y in self.Y_SCALE))

    def move_right(self, factor=0.3):
        self.move(factorX=factor, factorY=0)

    def move_left(self, factor=0.3):
        self.move(factorX=-factor, factorY=0)

    def move_up(self, factor=0.3):
        self.move(factorX=0, factorY=factor)

    def move_down(self, factor=0.3):
        self.move(factorX=0, factorY=-factor)


if __name__ == '__main__':
    image_generator = ImageGenerator()
    image = image_generator.make_mandelbrot_image()
    os.system("xdg-open " + IMAGE_FILE_NAME)
