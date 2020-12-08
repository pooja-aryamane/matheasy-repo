#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
os.chdir('/Users/poojaaryamane/Desktop/PythonWD')


# In[2]:


import requests
import xml.etree.ElementTree as ET
from PIL import Image
from io import BytesIO


# In[3]:


import keras
import cv2
import numpy as np
from tkinter import *
import PIL
from PIL import Image, ImageDraw, ImageTk
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
#keras.backend.image_data_format('th')
K.common.set_image_dim_ordering('th')
from keras.models import model_from_json

json_file = open('model_final.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model_final.h5")

from tkinter import filedialog
from tkinter import *
from tkinter.colorchooser import *
import pyscreenshot as ImageGrab
from PIL import Image




# In[4]:


import tkinter
from PIL import ImageTk, Image

class ScrollableImage(tkinter.Canvas):
    def __init__(self, master=None, **kw):
        self.image = kw.pop('image', None)
        super(ScrollableImage, self).__init__(master=master, **kw)
        self['highlightthickness'] = 0
        self.propagate(0)  # wont let the scrollbars rule the size of Canvas
        self.create_image(0,0, anchor='nw', image=self.image)
        # Vertical and Horizontal scrollbars
        self.v_scroll = tkinter.Scrollbar(self, orient='vertical', width=6)
        self.h_scroll = tkinter.Scrollbar(self, orient='horizontal', width=6)
        self.v_scroll.pack(side='right', fill='y')
        self.h_scroll.pack(side='bottom', fill='x')
        # Set the scrollbars to the canvas
        self.config(xscrollcommand=self.h_scroll.set, 
                yscrollcommand=self.v_scroll.set)
        # Set canvas view to the scrollbars
        self.v_scroll.config(command=self.yview)
        self.h_scroll.config(command=self.xview)
        # Assign the region to be scrolled 
        self.config(scrollregion=self.bbox('all'))

        self.focus_set()
        self.bind_class(self, "<MouseWheel>", self.mouse_scroll)

    def mouse_scroll(self, evt):
        if evt.state == 0 :
            self.yview_scroll(-1*(evt.delta), 'units') # For MacOS
            #self.yview_scroll( int(-1*(evt.delta/120)) , 'units') # For windows
        if evt.state == 1:
            self.xview_scroll(-1*(evt.delta), 'units') # For MacOS
           # self.xview_scroll( int(-1*(evt.delta/120)) , 'units') # For windows


# In[5]:


class GUI(Frame):
    def __init__(self, window):
        Frame.__init__(self)
        # TOOLS
        PENCIL, BRUSH, ERASER, LINE,RECTANGLE, OVAL = list(range(6))  #LINE, RECTANGLE, OVAL

        class Paint:
            def __init__(self, canvas):
                self.canvas = canvas
                self._tool, self._color, self._width, self._fill, self._obj = None, None, None, None, None
                self.lastx, self.lasty = None, None
                self.canvas.bind('<Button-1>', self.click)
                self.canvas.bind('<B1-Motion>', self.draw)

            def draw(self, event):
                if self._tool is None:
                    return
                x, y = self.lastx, self.lasty
                if self._tool in (LINE, RECTANGLE, OVAL ):
                    self.canvas.coords(self._obj, (x, y, event.x, event.y))
                elif self._tool in (PENCIL, BRUSH, ERASER):
                    #if self.lastx is not None and self.lasty is not None:
                    if self._tool == PENCIL:
                        self.canvas.create_line(self.lastx, self.lasty, event.x, event.y, fill = self._color, width=5)
                    elif self._tool == BRUSH:
                        if self._width is None:
                            x1, y1 = (event.x - 4), (event.y - 4)
                            x2, y2 = (event.x + 4), (event.y + 4)
                        else:
                            x1, y1 = (event.x - self._width), (event.y - self._width)
                            x2, y2 = (event.x + self._width), (event.y + self._width)
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill = self._color, outline = self._color)
                    elif self._tool == ERASER:
                        if self._width is None:
                            x1, y1 = (event.x - 15), (event.y - 15)
                            x2, y2 = (event.x + 15), (event.y + 15)
                        else:
                            x1, y1 = (event.x - self._width), (event.y - self._width)
                            x2, y2 = (event.x + self._width), (event.y + self._width)
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill = "#ffffff", outline = "#ffffff")
                    self.lastx, self.lasty = event.x, event.y

            # Updates x and y coordinates
            # Anchors starting coordinates for shapes
            def click(self, event):
                if self._tool is None:
                    return
                if self._color is None:
                    self._color = '#000000'
                x, y = event.x, event.y
                if self._tool == LINE:
                    self._obj = self.canvas.create_line((x, y, x, y), fill = self._color, width = self._width)
                elif self._tool == RECTANGLE:
                    if self._fill == True:
                        self._obj = self.canvas.create_rectangle((x, y, x, y), outline = self._color, fill = self._color, width = self._width)
                    else:
                        self._obj = self.canvas.create_rectangle((x, y, x, y), outline = self._color, width = self._width)
                elif self._tool == OVAL:
                    if self._fill == True:
                        self._obj = self.canvas.create_oval((x, y, x, y), outline = self._color, fill = self._color, width = self._width)
                    else:self._obj = self.canvas.create_oval((x, y, x, y), outline = self._color, width = self._width)
                self.lastx, self.lasty = x, y

            # Value updaters

            def select_tool(self, tool):
                print('Tool', tool)
                self._tool = tool

            def select_color(self, color):
                print('Color', color)
                self._color = color

            def select_width(self, width):
                print('Width', width)
                self._width = width

            def select_fill(self, fill):
                print('Fill', fill)
                self._fill = fill


        class Tool:
            def __init__(self, whiteboard, parent=None):
                self.file_to_open = None
                self.custom_color = None
                self._curr_tool = None
                self._curr_color = None
                self._curr_width = None
                self._curr_fill = None

                # TOOL ICONS
                self.pencil = PhotoImage(file = "Images/pencil_tool.gif")
                self.brush = PhotoImage(file = "Images/brush_tool.gif")
                self.eraser = PhotoImage(file = "Images/eraser_tool.gif")
                self.line = PhotoImage(file = "Images/line_tool.gif")
                #self.rectangle = PhotoImage(file = "Images/shape_tool.gif")
                #self.oval = PhotoImage(file = "Images/oval_tool.gif")

                # COLOR ICONS
                self.black = PhotoImage(file = "Images/black.gif") #000000
                self.gray = PhotoImage(file = "Images/gray.gif") #808080
                self.white = PhotoImage(file = "Images/white.gif") #ffffff 
                self.red = PhotoImage(file = "Images/red.gif") #ff0000
                self.yellow = PhotoImage(file = "Images/yellow.gif") #ffff00
                self.green = PhotoImage(file = "Images/green.gif") #00ff00
                self.cyan = PhotoImage(file = "Images/cyan.gif") #00ffff
                self.blue = PhotoImage(file = "Images/blue.gif") #0000ff
                self.magenta = PhotoImage(file = "Images/magenta.gif") #ff00ff
                self.brown = PhotoImage(file = "Images/brown.gif") #883d00
                self.colorwheel = PhotoImage(file = "Images/colorwheel.gif")
                self.pick_custom = PhotoImage(file = "Images/custom.gif")

                # BRUSH WIDTH ICONS
                self.one = PhotoImage(file = "Images/1.gif")
                self.two = PhotoImage(file = "Images/2.gif")
                self.three = PhotoImage(file = "Images/3.gif")
                self.four = PhotoImage(file = "Images/4.gif")
                self.five = PhotoImage(file = "Images/5.gif")
                self.six = PhotoImage(file = "Images/6.gif")

                # SHAPE FILL ICONS
                self.stroke = PhotoImage(file = "Images/stroke.gif")
                self.fill = PhotoImage(file = "Images/fill.gif")



                # FILE MANAGEMENT ICONS
                self.save = PhotoImage(file = "Images/evaluate.png")
                self.clear = PhotoImage(file = "Images/clear.gif")
                #self.im_clear = PhotoImage(file = "Images/open.gif")

                TOOLS = [
                    (self.pencil, PENCIL),
                    #(self.brush, BRUSH),
                    (self.eraser, ERASER)]
                    #(self.line, LINE)]
                    #(self.rectangle, RECTANGLE),
                    #(self.oval, OVAL)]


                COLORS = [
                    (self.black, '#000000', 2),
                    (self.gray, '#808080', 2),
                    (self.white, '#FFFFFF', 2),
                    (self.red, '#FF0000', 1),
                    (self.yellow, '#FFFF00', 1),
                    (self.green, '#00FF00', 1),
                    (self.cyan, '#00FFFF', 1),
                    (self.blue, '#0000FF', 1),
                    (self.magenta, '#FF00FF', 2),
                    (self.brown, '#883d00', 2)]



                WIDTH = [
                    (self.one, 1),
                    (self.two, 3),
                    (self.three, 5),
                    (self.four, 10),
                    (self.five, 20),
                    (self.six, 30)
                ]

                FILL = [
                    (self.stroke, False),
                    (self.fill, True)
                ]

                self.whiteboard = whiteboard
                frame1 = Frame(parent, width = 80, bg = '#C9EDFF')
                #frame2 = Frame(parent, width = 40)
                #frame3=Frame(parent, width = 80, bd=5)
                frame1.pack_propagate(False) # do not shrink/expand based on label size
                #frame2.pack_propagate(False) # do not shrink/expand based on label size
                #frame3.pack_propagate(False)

        #------------------ ICON CREATION AND PLACEMENT ------------------------
                # TOOLS - FRAME 1
                for img, name in TOOLS:
                    lbl = Label(frame1, relief='raised', image = img)
                    lbl._tool = name
                    lbl.bind('<Button-1>', self.update_tool)
                    lbl.pack(padx = 6, pady = 10)

                #spacer = Label(frame1, image = self.white)
                #spacer.pack(padx = 6, pady = 10)
                #spacer = Label(frame1, image = self.white)
                #spacer.pack(padx = 6, pady = 10)

                # SAVE - FRAME 1
                lbl = Label(frame1, relief = 'raised', image = self.save)
                lbl.bind('<Button-1>', self.save_file)
                lbl.pack(padx = 6, pady = 10)
                # CLEAR - FRAME 1
                lbl = Label(frame1, relief = 'raised', image = self.clear)
                lbl.bind('<Button-1>', self.clear_canvas)
                lbl.pack(padx = 6, pady = 10)
                # IMAGE CLEAR - FRAME1
                #lbl = Label(frame1, relief = 'raised', image = self.im_clear)
                #lbl.bind('<Button-1>', self.clear_image)
                #lbl.pack(padx = 6, pady = 10)

                # END OF FRAME 1
                frame1.pack(side = 'left', fill = 'y', expand = False, pady = 6)


        # Update current value and depress selected icon
            def update_tool(self, event):
                lbl = event.widget
                if self._curr_tool:
                    self._curr_tool['relief'] = 'raised'
                lbl['relief'] = 'sunken'
                self._curr_tool = lbl
                self.whiteboard.select_tool(lbl._tool)

            def update_color(self, event):
                lbl = event.widget
                if self._curr_color:
                    self._curr_color['relief'] = 'raised'
                lbl['relief'] = 'sunken'
                self._curr_color = lbl
                self.whiteboard.select_color(lbl._color)

            def update_width(self, event):
                lbl = event.widget
                if self._curr_width:
                    self._curr_width['relief'] = 'raised'
                lbl['relief'] = 'sunken'
                self._curr_width = lbl
                self.whiteboard.select_width(lbl._width)

            def update_fill(self, event):
                lbl = event.widget
                if self._curr_fill:
                    self._curr_fill['relief'] = 'raised'
                lbl['relief'] = 'sunken'
                self._curr_fill = lbl
                self.whiteboard.select_fill(lbl._fill)

            # Opens color picker and selects custom color
        #    def pick_color(self, event):
        #        color = askcolor()
        #        self.whiteboard.select_color(color[1])
        #        self.custom.configure(background = color[1], relief = 'sunken', image = "")
        #       self.custom._color = color[1]
        #        self.custom.bind('<Button-1>', self.update_color)
        #       self._curr_color = self.custom

            def save_file(self, event):
                #filename = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("png files","*.png"),("gif files","*.gif"),("bmp files","*.bmp")))
                x = 0
                y = 23
                #box = (canvas.winfo_rootx(),canvas.winfo_rooty(),canvas.winfo_rootx()+canvas.winfo_width(),canvas.winfo_rooty() + canvas.winfo_height())
                #im = ImageGrab.grab(bbox = box)
                im = ImageGrab.grab(bbox = (x + 95, y + 35, x + 1000, y + 338)) # Screenshot canvas area
                #if filename is None: # on cancel, don't save
                   # return
                im.save('image_0.png')
                img = cv2.imread('/Users/poojaaryamane/Desktop/PythonWD/image_0.png',cv2.IMREAD_GRAYSCALE)
                #im.show()
                if img is not None:
                        #images.append(img)
                        img=~img
                        ret,thresh=cv2.threshold(img,127,255,cv2.THRESH_BINARY)
                        ret,ctrs,ret=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                        cnt=sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
                        w=int(28)
                        h=int(28)
                        train_data=[]
                        #print(len(cnt))
                        rects=[]
                        for c in cnt :
                            x,y,w,h= cv2.boundingRect(c)
                            rect=[x,y,w,h]
                            rects.append(rect)
                        #print(rects)
                        bool_rect=[]
                        for r in rects:
                            l=[]
                            for rec in rects:
                                flag=0
                                if rec!=r:
                                    if r[0]<(rec[0]+rec[2]+10) and rec[0]<(r[0]+r[2]+10) and r[1]<(rec[1]+rec[3]+10) and rec[1]<(r[1]+r[3]+10):
                                        flag=1
                                    l.append(flag)
                                if rec==r:
                                    l.append(0)
                            bool_rect.append(l)
                        #print(bool_rect)
                        dump_rect=[]
                        for i in range(0,len(cnt)):
                            for j in range(0,len(cnt)):
                                if bool_rect[i][j]==1:
                                    area1=rects[i][2]*rects[i][3]
                                    area2=rects[j][2]*rects[j][3]
                                    if(area1==min(area1,area2)):
                                        dump_rect.append(rects[i])
                        #print(len(dump_rect)) 
                        final_rect=[i for i in rects if i not in dump_rect]
                        #print(final_rect)
                        for r in final_rect:
                            x=r[0]
                            y=r[1]
                            w=r[2]
                            h=r[3]
                            im_crop =thresh[y:y+h+10,x:x+w+10]


                            im_resize = cv2.resize(im_crop,(28,28))
                            #cv2.imshow("work",im_resize)
                            #cv2.waitKey(0)
                            #cv2.destroyAllWindows()

                            im_resize=np.reshape(im_resize,(1,28,28))
                            train_data.append(im_resize)
                s=''
                para=0
                sqrt=0
                for i in range(len(train_data)):
                    train_data[i]=np.array(train_data[i])
                    train_data[i]=train_data[i].reshape(1,1,28,28)
                    result=loaded_model.predict_classes(train_data[i])
                    if(result[0]==17):
                        sqrt=1
                    if(result[0]==0):
                        s=s+'0'
                    if(result[0]==1):
                        s=s+'1'
                    if(result[0]==2):
                        s=s+'2'
                    if(result[0]==3):
                        s=s+'3'
                    if(result[0]==4):
                        s=s+'4'
                    if(result[0]==5):
                        s=s+'5'
                    if(result[0]==6):
                        s=s+'6'
                    if(result[0]==7):
                        s=s+'7'
                    if(result[0]==8):
                        s=s+'8'
                    if(result[0]==9):
                        s=s+'9'
                    if(result[0]==10):
                        s=s+'+'
                    if(result[0]==11):
                        s=s+'-'
                    if(result[0]==12):
                        s=s+'*'
                    if(result[0]==13):
                        s=s+'/'
                    if(result[0]==14):
                        s=s+'('
                    if(sqrt==1):
                        para=para+1
                    if(result[0]==15):
                        s=s+')'
                    if(sqrt==1):
                        para=para-1
                    if(result[0]==16):
                        s=s+'m'
                    if(result[0]==18):
                        s=s+'**'
                    #if(result[0]==19):
                        #s=s+'/'
                    #if(result[0]==20):
                        #s=s+'**'
                    if((result[0]==15) & (sqrt==1) & (para==0)):
                        sqrt=0
                        s=s+'**0.5'
                s= re.sub("--","=",s)
                #e= eval(s)
                print(s)

                if '+' in s: 
                    s = s.replace('+', ' plus ')
                if '-' in s: 
                    s = s.replace('-', ' minus ')
                if '=' in s: 
                    s = s.replace('=', ' equals ')
                else:
                    s=s

                s2=('http://api.wolframalpha.com/v2/query?appid=H4THYX-2AVQX9922J&input=solve+'+s+'&podstate=Result__Step-by-step+solution&format=image')

                URL = s2
                response = requests.get(URL)
                with open('wolfram.xml', 'wb') as file:
                    file.write(response.content)


                tree = ET.parse('wolfram.xml')
                groot = tree.getroot()
                steps=0
                for i in range(0,len(groot[1])-1):
                    if(str(groot[1][i].attrib).find('Possible intermediate steps')>=0):
                        steps=1
                        break
                if(steps==1):
                    imgstr=str(groot[1][i][0].attrib)
                else:
                    imgstr=str(groot[1][0][0].attrib)
                start=imgstr.find('https')
                end=imgstr.find(',')-1
                #end
                imgurl=imgstr[start:end]

                response2 = requests.get(imgurl)
                img2 = Image.open(BytesIO(response2.content))
                img2

                img2.save('image_2.gif')

                #img_label = Label(canvas2)
                canvas2.image = PhotoImage(file="image_2.gif")
                #img_label['image'] = img_label.image

                #img_label.pack(expand = True)

                #img_output = PhotoImage(file="image_2.gif")
                show_image = ScrollableImage(canvas2, image=canvas2.image)
                show_image.pack(fill='both', expand = True)

                btn = Button(canvas2, text ="Clear", command = show_image.destroy)
                btn.place(relx = 0.7, relwidth = 0.3, rely=0.97, anchor = 'w')

                # Clear canvas
            def clear_canvas(self, event):
                canvas.delete("all")


        #root = Tk()
        #root.geometry("1500x600+0+0")
        #root.resizable(width = False, height = False)
        #root.title("Matheasy")
        #yscrollbar = Scrollbar(root)
        #yscrollbar.pack(padx=6, pady=6, side='right')
        canvas = Canvas(self, highlightbackground='black', width = 963, height = 500)
        canvas.pack_propagate(False)
        whiteboard = Paint(canvas)
        tool = Tool(whiteboard)
        frame = Frame(canvas,bg='#C0C0C0',bd=5)
        frame.place(relx = 0.5, relwidth = 0.99, relheight = 0.35, rely=0.64,anchor = 'n')
        label_frame=Label(frame, text='Instructions:\n\n 1. Syntax for square root of x: √ ( x )\n 2. Syntax for division: x/y\n 3.Variable for equations: m\n 4. Synatax for power: m^x \n Simply click on the green button for your answer!\n Please make sure to clear output screen before evaluating a new expression.', 
                          bg='#C0C0C0', font=("Times", 15, "bold"))
        label_frame.pack()

        canvas2 = Canvas(self, highlightbackground='black', width=382, height=500)
        #canvas2.config(scrollregion=canvas2.bbox(ALL))

        canvas.pack(expand = False, padx=6, pady=6, side='left')
        canvas2.pack_propagate(False)
        canvas2.pack(pady=6, padx=6)
        self.configure(background = '#C9EDFF')
        #root.mainloop()
        
if __name__ == "__main__":
    root = Tk()
    root.geometry("1345x500+0+0")
    root.resizable(width = True, height = False)
    root.title("MathEasy")
    root.configure(background = '#C9EDFF')
    gui = GUI(root)
    gui.pack(fill="both", expand=True)
    root.mainloop()


# In[ ]:





# In[ ]:




