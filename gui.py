
from tkinter import *
from PIL import ImageTk
from fractal import make_mandelbrot_image

def make_tkinter_image(pil_image):
    return ImageTk.PhotoImage(pil_image)

class App:

    def __init__(self, master):
        pil_image = make_mandelbrot_image(restore_from_file=True)
        image = make_tkinter_image(pil_image)
#        canvas.create_image(image.width(), image.height(),image=image)
        label = Label(master, image=image)
        label.image = image
        label.pack()

    def say_hi(self):
        print("hi there, everyone!")

root = Tk()
app = App(root)
root.mainloop()
