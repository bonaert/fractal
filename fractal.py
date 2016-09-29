import os

from PIL import Image

CONSTANT = 5+2*1j
DEPTH = 500

WIDTH = 800
HEIGHT = 600

ITERATIONS_FILE_NAME = "iterations.data"
PIXEL_COLORS_FILE_NAME = "pixel.data"

def evolution(val, constant=CONSTANT):
    return val**2 + constant

def is_inside_bounds(val):
    # Fast simple evaluation
    # return abs(val.real) < 2 and abs(val.imag) < 2

    # Slower, more precise version
    size_squared = (val.real ** 2 + val.imag ** 2)
    return size_squared < 4

def num_iterations_until_escape(constant):
    num = 0
    iterations = 0
    while is_inside_bounds(num) and iterations < DEPTH:
        num = evolution(num, constant)
        iterations += 1

    return iterations

    if iterations == DEPTH:
        return None
    else:
        return iterations

def get_colors(iterations):
    if iterations == DEPTH:
        return (255, 255, 255)
    else:
        return (0,0,0)
    percent = iterations / DEPTH
    color = 255 - int(255 * percent)
    return (color, color, 0)

def make_image(pixels_colors):
    im = smp.toimage(pixels_colors)
    im.save("fractal.png","PNG")
    os.system("xdg-open fractal.png")
    return im

def scale_x(x):
    # The Mandelbrot X scale is (-2.5, 1)
    return -2.5 + 3.5 * (x / WIDTH)

def scale_y(y):
    # The Mandelbrot Y scale is (-1, 1)
    return -1.0 +  2 * (y / HEIGHT)

def restore_from_file(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return None

def compute_iterations():
    iterations = []
    for x in range(WIDTH):
        print(x)
        scaled_x = scale_x(x)
        for y in range(HEIGHT):
            scaled_y = scale_y(y)
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
    colors_pixels = list(map(get_colors, iterations))
    print(colors_pixels)

    with open(ITERATIONS_FILE_NAME, "w") as f:
        f.write(str(iterations))

    with open(PIXEL_COLORS_FILE_NAME, "w") as f:
        f.write(str(colors_pixels))
    
    make_image(colors_pixels)

make_mandelbrot_image()

