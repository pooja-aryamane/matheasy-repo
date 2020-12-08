#!/usr/bin/env python
# coding: utf-8

# In[1]:


import speech_recognition as sr     # import the library
from os import system
import tkinter as tk 
#HEIGHT = 700
#WIDTH = 800


# In[2]:


class GUI(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self)

        def s2s():
            r = sr.Recognizer()                 # initialize recognizer
            with sr.Microphone() as source:     # mention source it will be either Microphone or audio files.
                print("Speak Anything :")
                audio = r.listen(source)        # listen to the source
                try:
                    text = r.recognize_google(audio)# use recognizer to convert our audio into text part.
                    if 'x' in text:
                        text = text.replace('x', '*')
                    if 'raise to' in text: 
                        text = text.replace('raise to', '^')
                    if 'raised to' in text: 
                        text = text.replace('raised to', '^')
                    if 'divided by' in text: 
                        text = text.replace('divided by', '/')
                    if 'into' in text: 
                        text = text.replace('into', '*')
                    if 'square' in text: 
                        text = text.replace('square', '**2')
                    if 'cube' in text: 
                        text = text.replace('cube', '**3')
                    if 'half' in text:
                        text = text.replace('half','0.5')
                    if 'plus' in text:
                        text = text.replace('plus', '+')
                    if 'minus' in text:
                        text = text.replace('minus', '-')
                    else:
                        text = text
                    final_str = "You said: %s \nAnswer Is: %s" % (text, str(eval(text)))
                except:
                    final_str = "Sorry could not recognize your voice"   # In case of voice not recognized  clearly
            s = eval(text)
            system('say %s' % (s))
            label['text'] = final_str                                                       

        canvas = tk.Canvas(self, height= 250, width = 1345, bg = '#C9EDFF', highlightbackground = '#C9EDFF')
        canvas.pack()
        canvas.pack_propagate(False)

        frame = tk.Frame(self, bg = '#C9EDFF')
        frame.place(relx = 0.5, rely = 0.1, relwidth = 0.495, relheight = 0.8, anchor = 'ne')

        output_canvas = tk.Canvas(self, bg='#FFFFFF', highlightbackground='black')
        output_canvas.place(relx = 0.5, rely = 0.1, relwidth = 0.495, relheight = 0.8, anchor='nw')
        output_canvas.pack_propagate(False)

        label = tk.Label(output_canvas, bg='#FFFFFF')
        label.place(relwidth=0.5, relheight=0.4, rely= 0.4, relx = 0.5, anchor = 'n')

        button = tk.Button(frame, text = "Simple Question? \nClick & Ask!", command = s2s)
        button.configure(font = ('Sans','20','bold'))

        button.place(relheight = 1, relwidth = 1)
        
        self.configure(background = '#C9EDFF')
        

if __name__ == "__main__":
    root = tk.Tk()
    #root.pack_propagate(False)
    gui = GUI(root)
    gui.pack(fill="both", expand=True)
    tk.mainloop()
                          


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




