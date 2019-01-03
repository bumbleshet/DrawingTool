
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageDraw
import imageProcessing



class SimpleDrawingApp(object):

    DEFAULT_COLOR = 'black'
    DEFAULT_ADD_PEN = 3
    DEFAULT_SIZE = 600

    def __init__(self):
        self.root = Tk()

        self.pen_button = Button(self.root, text='Pen', command=self.use_pen, width=8)
        self.pen_button.grid(row=0, column=0)

        self.eraser_button = Button(self.root, text='Eraser', command=self.use_eraser, width=8)
        self.eraser_button.grid(row=0, column=1)

        self.clear_all_button = Button(self.root, text='Clear All', command=self.clear_all, width=8)
        self.clear_all_button.grid(row=0, column=2)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=3)

        self.predict_button = Button(self.root, text='Predict', command=self.predict, width=15)
        self.predict_button.grid(row=0, column=4)

        self.create_canvas()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()+self.DEFAULT_ADD_PEN
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def create_canvas(self):
        self.c = Canvas(self.root, bg='white', width=self.DEFAULT_SIZE, height=self.DEFAULT_SIZE)
        self.c.grid(row=1, columnspan=5)

        self.toProcessImg = Image.new("RGB", (self.DEFAULT_SIZE, self.DEFAULT_SIZE), color='white')
        self.draw = ImageDraw.Draw(self.toProcessImg)

        self.setup()
        self.root.mainloop()

    def clear_all(self):
        self.create_canvas()

    def predict(self):

        self.toProcessImg = imageProcessing.rm_white_space(self.toProcessImg, Image)
        # basewidth = 150
        # wpercent = (basewidth/float( self.toProcessImg.size[0]))
        # hsize = int((float( cropped.size[1])*float(wpercent)))
        self.toProcessImg = self.toProcessImg.resize((150,150), Image.BICUBIC)
        
        predicted_class = imageProcessing.predict_class(self.toProcessImg)
        messagebox.showinfo("Information","Mental Age: " + predicted_class)
        self.create_canvas()

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()+self.DEFAULT_ADD_PEN
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
            
            self.draw.line([(self.old_x, self.old_y), (event.x, event.y)],
                            width=self.line_width, fill=paint_color)
        self.old_x = event.x

        self.old_y = event.y


    def reset(self, event):
        self.old_x, self.old_y = None, None



if __name__ == '__main__':
    SimpleDrawingApp()