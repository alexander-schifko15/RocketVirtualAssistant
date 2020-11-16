# Import library here

from tkinter import *
import time
import datetime
from PIL import ImageTk,Image
import os
import sqlite3
from tkinter import messagebox
import webbrowser
import tkinter as tk

# Splash screen
def splash():
	sroot = Tk()
	sroot.geometry('450x400')
	sroot.title("Splash window")
	# Hide border
	sroot.overrideredirect(1)
	# Center splash window
	sroot.eval('tk::PlaceWindow . center')
	sroot.configure()
	img = Image.open("Logo.jpg")
	render = ImageTk.PhotoImage(img)
	img = Label(sroot, image = render)
	img.image = render
	img.place(x = -167, y = -60)
	#spath = "Logo.JGP"
	#simg = ImageTk.PhotoImage(Image.open(spath))
	#my = Label(sroot,image=simg)
	#my.image = simg
	#my.place(x=0,y=0)

	def call_mainroot():
		sroot.destroy()
		mainroot()

	sroot.after(2500, call_mainroot)         #Time frame for splash screen

splash()

def mainroot():
	# Main screen
	root = Tk()
	root.geometry('350x500')
	root.configure(background='#F0F8FF')
	root.title('Rocket Voice Assistant')
	#root.overrideredirect(1)
	# Text field and scroll bar
	t = Text(root, height = 31, width = 45)
	t.place(x = 13, y = 10)
	Quote = "Rocket Voice Assistant"
	t.insert(tk.END, Quote)
	t.config(state = DISABLED)

	# Center main window
	root.eval('tk::PlaceWindow . center')
	# Popup window when closing the program
	def on_closing():
		if messagebox.askokcancel("Warning", "Do you want to quit the application?", icon = 'warning'):
			root.destroy()
	root.protocol("WM_DELETE_WINDOW", on_closing)

	# Function to open website
	new = 1
	url = "http://et791.ni.utoledo.edu/~ylu10/schedule/"
	def openweb():
		webbrowser.open(url, new = new)

	# This is the section of code which creates buttons
	Button(root, text='Start', bg='#FFFACD', font=('arial', 12, 'normal'), padx = 10, pady = 5, relief = GROOVE).place(x=25, y=425)
	Button(root, text='Quit', bg='#FFFACD', font=('arial', 12, 'normal'), command = on_closing, padx = 10, pady = 5, relief = GROOVE).place(x=107, y=425)
	Button(root, text='Class Schedule', bg='#FFFACD', font=('arial', 12, 'normal'), command=openweb, padx = 10, pady = 5, relief = GROOVE).place(x=185, y=425)

	root.mainloop()

# End Of main window

# Getting rid of splash window and call main window

mainloop()