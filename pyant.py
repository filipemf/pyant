# Components imports
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox

from tkinter import colorchooser
from tkinter import filedialog

#Pillow imports
import PIL 
from PIL import Image, ImageDraw, ImageGrab, ImageTk

class pyant:
    def __init__(self, master):
        self.master = master

        self.brushColor = 'black'
        self.bgColor = 'white'

        self.initial_x = None
        self.initial_y = None

        self.brushWidth = 5
        self.brushType = StringVar()
        self.brushType.set("round")

        self.drawComponents()
        
        self.canvas.bind('<B1-Motion>',self.paint)
        self.canvas.bind('<ButtonRelease-1>',self.resetxy)
      
    def drawComponents(self):
        self.canvas = Canvas(self.master,width=500,height=400,bg=self.bgColor)
        self.canvas.pack(fill=BOTH,expand=True)
        
        brush_options_frame = Frame(self.master)
        brush_options_frame.pack(padx=20)

        # Brush size
        brush_size_frame = LabelFrame(brush_options_frame, text="Tamanho do pincel")
        brush_size_frame.grid(row=0, column=0)

        # Brush Slider
        self.slider = ttk.Scale(brush_size_frame, from_=1, to=100,command=self.changeBrushWidth, orient=VERTICAL, value=10)
        self.slider.pack(pady=10, padx=10)

        # Brush slider Label
        slider_label = Label(brush_size_frame, text=self.brushWidth)
        slider_label.pack()

        # Brush
        brush_type_frame = LabelFrame(brush_options_frame, text="Tipo de pincel", height=10)
        brush_type_frame.grid(row=0, column=1, padx=50)

        # Radio buttons for Brush Type
        brush_type_radio1 = Radiobutton(brush_type_frame, text="Lápis", variable=self.brushType, value="round")
        brush_type_radio2 = Radiobutton(brush_type_frame, text="Slash", variable=self.brushType, value="butt")
        brush_type_radio3 = Radiobutton(brush_type_frame, text="Diamond", variable=self.brushType, value="projecting")
        brush_type_radio4 = Radiobutton(brush_type_frame, text="Borracha", variable=self.brushType, value="eraser")


        brush_type_radio1.pack()
        brush_type_radio4.pack()
        brush_type_radio2.pack()
        brush_type_radio3.pack()


        # Change Colors
        change_colors_frame = LabelFrame(brush_options_frame, text="Opções de Cores")
        change_colors_frame.grid(row=0, column=3)

        # Change Brush Color Button 
        brush_color_button = Button(change_colors_frame, text="Cor do pincel", command=self.changeBrushColor)
        brush_color_button.pack(pady=10, padx=10)

        # Change canvas background color
        canvas_color_button = Button(change_colors_frame, text="Cor do Canvas", command=self.changeBackgroundColor)
        canvas_color_button.pack(pady=10, padx=10)

        # Program Options Frame
        options_frame = LabelFrame(brush_options_frame, text="Opções do programa")
        options_frame.grid(row=0, column=4, padx=50)

        clearCanvas_button = Button(options_frame, text="Limpar Canvas", command=self.clearCanvas)
        clearCanvas_button.pack()

        # Save image
        save_image_button = Button(options_frame, text="Salvar em PNG", command=self.saveImageAsPNG)
        save_image_button.pack()  

    def paint(self, event):

        if self.brushType.get()=="round":
            if self.initial_x and self.initial_y:
                self.canvas.create_line(self.initial_x,self.initial_y, event.x, event.y, width=self.brushWidth, fill=self.brushColor, capstyle=self.brushType.get(), smooth=True)
        elif self.brushType.get()=="butt":
            if self.initial_x and self.initial_y:
                x1 = event.x - 1
                y1 = event.y - 1

                # End point
                x2 = event.x + 1
                y2 = event.y + 1

                self.canvas.create_line(x1, y1, x2, y2, width=self.brushWidth, fill=self.brushColor, capstyle=self.brushType.get(), smooth=True)
        
        elif self.brushType.get()=="eraser":
            if self.initial_x and self.initial_y:
                self.canvas.create_line(self.initial_x,self.initial_y, event.x, event.y, width=self.brushWidth, fill=self.bgColor, capstyle=ROUND, smooth=True)
        else:
            x1 = event.x - 1
            y1 = event.y - 1

            # End point
            x2 = event.x + 1
            y2 = event.y + 1

            self.canvas.create_line(x1, y1, x2, y2, width=self.brushWidth, fill=self.brushColor, capstyle=self.brushType.get(), smooth=True)


        self.initial_x = event.x
        self.initial_y = event.y

    def resetxy(self, event):
        self.initial_x = None
        self.initial_y = None      

    def changeBrushWidth(self, event):
        self.brushWidth = event
        self.my_slider = "self.brushWidth"

    def saveImageAsPNG(self):
        file = filedialog.asksaveasfilename(filetypes=[('Portable Network Graphics','*.png')])
        if file:
            x = self.master.winfo_rootx() + self.c.winfo_x()
            y = self.master.winfo_rooty() + self.c.winfo_y()
            x1 = x + self.c.winfo_width()
            y1 = y + self.c.winfo_height()

            PIL.ImageGrab.grab().crop((x,y,x1,y1)).save(file + '.png')            
        
    def clearCanvas(self):
        self.canvas.delete(ALL)
        self.canvas.config(bg="white")

    def changeBrushColor(self):
        self.brushColor = colorchooser.askcolor(color=self.brushColor)[1]

    def changeBackgroundColor(self):
        self.bgColor=colorchooser.askcolor(color=self.bgColor)[1]
        self.canvas['bg'] = self.bgColor


if __name__ == '__main__':
    root = Tk()
    pyant(root)
    root.title('Pyant')

    root.mainloop()
