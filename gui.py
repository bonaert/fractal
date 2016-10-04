import tkinter

from tkinter import *
from PIL import ImageTk
from fractal import ImageGenerator

def make_tkinter_image(pil_image):
    return ImageTk.PhotoImage(pil_image)

class App:

    def __init__(self, master):
        self.generator = ImageGenerator()
        self.image = self.make_image(restore=False)

        self.label = Label(master, image=self.image)
        self.label.image = self.image
        self.label.pack()
        
        
        self.button = tkinter.Button(master, text="Zoom", command=self.zoom)
        self.button.pack()

        self.button2 = tkinter.Button(master, text="Zoom Out", command=self.zoomout)
        self.button2.pack()


        self.button3 = tkinter.Button(master, text="Right", command=self.moveright)
        self.button3.pack()

        self.button4 = tkinter.Button(master, text="Left", command=self.moveleft)
        self.button4.pack()

        self.button5 = tkinter.Button(master, text="Up", command=self.moveup)
        self.button5.pack()

        self.button6 = tkinter.Button(master, text="Down", command=self.movedown)
        self.button6.pack()

    def make_image(self, restore=False):
        pil_image = self.generator.make_mandelbrot_image(restore_from_file=restore)
        image = make_tkinter_image(pil_image)
        return image

    def zoom(self, factor=0.5):
        print("Zoom")
        self.generator.zoom(factor)
        self.put_image()

    def put_image(self):
        self.image = self.make_image()
        self.label.configure(image=self.image)
    
    def zoomout(self):
        self.zoom(2)

    def moveleft(self):
        self.generator.move_left()
        self.put_image()

    def moveright(self):
        self.generator.move_right()
        self.put_image()

    def moveup(self):
        self.generator.move_up()
        self.put_image()

    def movedown(self):
        self.generator.move_down()
        self.put_image()
        

root = Tk()
app = App(root)
root.mainloop()
