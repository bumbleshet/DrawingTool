
from tkinter import *
from tkinter import messagebox, filedialog, simpledialog
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
import pyscreenshot as ImageGrab
import imageProcessing



class SimpleDrawingApp(object):

    DEFAULT_COLOR = 'black'
    DEFAULT_ADD_PEN = 3
    DEFAULT_SIZE = 600

    def __init__(self):
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.title('Drawing App')
        messagebox.showinfo("Directions", "I want you to make a picture of a person. Make the very best picture that you can. Take your time and work very carefully. Try very hard and see what a good picture you can make.")
        self.root.bind('<Control-z>', self.undo) 
        self.root.bind('<Control-y>', self.redo) 
        self.dir_btn = Button(self.root, text='Directions', command=self.directions, width=12)
        self.dir_btn.grid(row=0, column=0, sticky="nsew")

        self.opn_img_btn = Button(self.root, text='Open Image', command=self.open_img, width=12)
        self.opn_img_btn.grid(row=0, column=1, sticky="nsew")

        self.pen_button = Button(self.root, text='Pen', command=self.use_pen, width=12)
        self.pen_button.grid(row=1, column=0, sticky="nsew")

        self.eraser_button = Button(self.root, text='Eraser', command=self.use_eraser, width=12)
        self.eraser_button.grid(row=1, column=1, sticky="nsew")

        Label(text="Pen/Eraser Size:", font=(None, 12)).grid(row=2, column=0, sticky="nsew")
        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=2, column=1, sticky="nsew")

        self.clear_all_button = Button(self.root, text='Erase All', command=self.clear_all, width=12)
        self.clear_all_button.grid(row=3, column=0, sticky="nsew")
        

        self.predict_button = Button(self.root, text='Predict', command=self.predict, width=12)
        self.predict_button.grid(row=3, column=1, sticky="nsew")
        self.stack = [] 
        self.temp_stack = [] 
        self.deleted_stack = []
        self.erase_all_bool = False
        # self.count = 0
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

    def open_img(self):
        self.root.fileName = filedialog.askopenfilename(filetypes =[("JPEG Images", "*.jpg"), ("PNG Images", "*.png")])
        self.loadImage = Image.open(self.root.fileName)    
        self.loadImage = self.loadImage.resize((600,600), Image.BICUBIC) 
        self.loadImage = ImageTk.PhotoImage(self.loadImage)
        self.c.create_image(0, 0, anchor="nw", image=self.loadImage)

    def directions(self):
        messagebox.showinfo("Directions", "I want you to make a picture of a person. Make the very best picture that you can. Take your time and work very carefully. Try very hard and see what a good picture you can make.")                             
        
    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def create_canvas(self):
        self.c = Canvas(self.root, bg='white', width=self.DEFAULT_SIZE, height=self.DEFAULT_SIZE)
        self.c.grid(row=0,rowspan=16, column=4, columnspan=6)
        self.setup()
        self.root.mainloop()

    def clear_all(self):
        
        self.erase_all_bool = True
        self.temp_image = self.getter(self.c)
        self.temp_image = ImageTk.PhotoImage(self.temp_image)
        self.create_canvas()
        self.stack = [] 
        self.temp_stack = [] 
        self.deleted_stack = []

    def predict(self):
        isAddPadding = True
        
        self.toProcessImg = self.getter(self.c)
        self.toProcessImg, isAddPadding = imageProcessing.rm_white_space(self.toProcessImg, Image)
        self.toProcessImg = self.toProcessImg.resize((150,150), Image.BICUBIC)
        # print(isAddPadding)
        if(isAddPadding):
            self.toProcessImg = imageProcessing.add_white_border(self.toProcessImg, Image)
            self.toProcessImg = self.toProcessImg.resize((150,150), Image.BICUBIC)
        # self.count=self.count+1
        # self.toProcessImg.save('predict'+str(self.count)+'.jpg')
        self.predicted_class = imageProcessing.predict_class(self.toProcessImg)
        years = simpledialog.askinteger("What's your age?", self.root)
        months = MyDialog(self.root, "How many months until your birthday?").result
        years = (years*12) + months
        print(years)
        if(years>156):
            years=156
        elif(years<12):
            messagebox.showinfo("Information","Age invalid, only 1-13")
        if(self.predicted_class==1):
            messagebox.showinfo("Information","I'm sorry, I can't recognize the drawing")
        elif(self.predicted_class==2):
            messagebox.showinfo("Information","IQ: " + str(int((((3*12)/years)*100))) + " or less")
        else:
            messagebox.showinfo("Information","IQ: " + str(int((((self.predicted_class*12)/years)*100))) + "-" + str(int(((((self.predicted_class*12)+9)/years)*100))))
        self.create_canvas()

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.erase_all_bool = False
        self.line_width = self.choose_size_button.get()+self.DEFAULT_ADD_PEN
        paint_color = 'white' if self.eraser_on else self.color
        attib = dict()

        if self.old_x and self.old_y:

            x = self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36, 
                               tags='temp_line')
            attib.update({'old_x': self.old_x, 'old_y': self.old_y, 
                               'event.x': event.x, 'event.y': event.y,
                               'line_width': self.line_width, 'paint_color': paint_color})
            self.stack.append(x)
            self.temp_stack.append(attib)
            
        self.old_x = event.x    
        self.old_y = event.y

    def getter(self, widget):
        x=self.root.winfo_rootx()+widget.winfo_x()
        y=self.root.winfo_rooty()+widget.winfo_y()
        x1=x+widget.winfo_width()
        y1=y+widget.winfo_height()
        return ImageGrab.grab().crop((x,y,x1,y1))

    def undo(self, event):
        if(self.erase_all_bool):
            self.c.create_image(0, 0, anchor="nw", image=self.temp_image) 
            self.erase_all_bool = False
        else:
            x = self.stack.pop()
            deleted_attib = self.temp_stack.pop()
            self.deleted_stack.append(deleted_attib)
            self.c.delete(x)  
    

    def redo(self, event):
        attib = dict()
        attib_deleted = self.deleted_stack.pop()
        x = self.c.create_line(attib_deleted['old_x'], attib_deleted['old_y'], attib_deleted['event.x'], attib_deleted['event.y'],
                            width=attib_deleted['line_width'], fill=attib_deleted['paint_color'],
                            capstyle=ROUND, smooth=TRUE, splinesteps=36, 
                            tags='temp_line')  
        attib.update({'old_x': attib_deleted['old_x'], 'old_y': attib_deleted['old_y'], 
                            'event.x': attib_deleted['event.x'], 'event.y': attib_deleted['event.y'],
                            'line_width': attib_deleted['line_width'], 'paint_color': attib_deleted['paint_color']})
        
        self.stack.append(x)
        self.temp_stack.append(attib)
        

    def reset(self, event):
        self.old_x, self.old_y = None, None

#customize varaible
class MyDialog(simpledialog.Dialog):
    def body(self, master):
        self.geometry("400x75")
        tk.Label(master).grid(row=0)

        self.e1 = tk.Entry(master)
        self.e1.grid(row=0)
        return self.e1
    
    def validate(self):
        try:
            first = self.e1.get()
            val = int(first)
            self.result = val
            return 1
        except ValueError:
            messagebox.showwarning(
                "Illegal value",
                "Not an integer. Please try again"
            )
            return 0

if __name__ == '__main__':
    SimpleDrawingApp()
