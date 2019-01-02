
from tkinter import *
from tkinter.colorchooser import askcolor

class SimpleDrawingApp(object):

    DEFAULT_PEN_SIZE = 10.0
    DEFAULT_COLOR = 'black'

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

        self.predict_button = Button(self.root, text='Predict', command='', width=15)
        self.predict_button.grid(row=0, column=4)

        self.create_canvas()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
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
        self.c = Canvas(self.root, bg='white', width=600, height=600)
        self.c.grid(row=1, columnspan=5)

        self.setup()
        self.root.mainloop()

    def clear_all(self):
        self.create_canvas()

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x

        self.old_y = event.y


    def reset(self, event):
        self.old_x, self.old_y = None, None



if __name__ == '__main__':
    SimpleDrawingApp()