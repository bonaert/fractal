import os
import json

from PIL import Image
DEPTH = 100

X_SCALE = (-2.2, 2.2)
Y_SCALE = (- 2.2, 2.2)

X_SIZE = X_SCALE[1] - X_SCALE[0]
Y_SIZE = Y_SCALE[1] - Y_SCALE[0]

DIM = 200
WIDTH = int(DIM * X_SIZE)
HEIGHT = int(DIM * Y_SIZE)


ITERATIONS_FILE_NAME = "iterations.data"
PIXEL_COLORS_FILE_NAME = "pixel.data"

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


PALETTE = generate_palette()

def evolution(val, constant):
    return val**2 + constant

def is_inside_bounds(val):
    # Fast simple evaluation
    # return abs(val.real) < 2 and abs(val.imag) < 2

    # Slower, more precise version
    return abs(val) <= 2

def num_iterations_until_escape(constant):
    num = 0+0*1j
    iterations = 0
    while is_inside_bounds(num) and iterations < DEPTH:
        num = evolution(num, constant)
        iterations += 1

    return iterations

def get_colors(iterations):
    num = iterations
    return PALETTE[num]

def make_image(pixels_colors):
    im = Image.new("RGB", (WIDTH, HEIGHT))
    im.putdata(pixels_colors)
    im.save("fractal.png","PNG")
    os.system("xdg-open fractal.png")
    return im

def scale_x(x):
    # The Mandelbrot X scale is (-2.5, 1)
    return X_SCALE[0] + X_SIZE * (x / WIDTH)

def scale_y(y):
    # The Mandelbrot Y scale is (-1, 1)
    return Y_SCALE[0] + Y_SIZE * (y / HEIGHT)


def restore_from_file(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return None

def compute_iterations():
    iterations = []
    for y in range(HEIGHT):
        print(y)
        scaled_y = scale_y(y)
        for x in range(WIDTH):
            scaled_x = scale_x(x)
            constant = scaled_x + scaled_y*1j
            num_iterations = num_iterations_until_escape(constant)
            iterations.append(num_iterations)
    return iterations

def get_iterations():
    data = restore_from_file(ITERATIONS_FILE_NAME)
    if data is None:
        data = compute_iterations()

    return data

def make_mandelbrot_image():
    iterations = get_iterations()
    print("Got iterations")
    colors_pixels = list(map(get_colors, iterations))
    print("Got pixel colors")

    with open(ITERATIONS_FILE_NAME, "w") as f:
        f.write(str(iterations))

    with open(PIXEL_COLORS_FILE_NAME, "w") as f:
        f.write(str(colors_pixels))
    
    print("Saved data")
    
    make_image(colors_pixels)

make_mandelbrot_image()

