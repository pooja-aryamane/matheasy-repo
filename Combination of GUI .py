#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
os.chdir('/Users/poojaaryamane/Desktop/PythonWD')


# In[ ]:


import tkinter as tk
import GUI1
import GUI2

# the first gui owns the root window
win1 = tk.Tk()
gui1 = GUI1.GUI(win1)
gui1.pack(fill="both", expand=True)
win1.resizable(width = True, height = False)
win1.configure(background = '#C9EDFF')
#win1.title = 'MathEasy'

# the second GUI is in a Toplevel
win2 = tk.Toplevel(win1)
gui2 = GUI2.GUI(win2)
gui2.pack(fill="both", expand=True)

tk.mainloop()


# In[ ]:




