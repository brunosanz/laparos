#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import subprocess
import os
   
def center(ventana):
    ventana.update_idletasks()
    w=ventana.winfo_width()
    h=ventana.winfo_height()
    extraW=ventana.winfo_screenwidth()-w
    extraH=ventana.winfo_screenheight()-h
    ventana.geometry("%dx%d%+d%+d" % (w,h,extraW/2,extraH/2))

def ejecutar(archivo):
    if sys.platform == "win32":
        os.system (archivo)
    else:
        os.system ("/usr/bin/python " + archivo)

master = Tk()
master.title("Laparoscopía")
master.resizable(0,0)
if sys.platform == "win32":
    master.geometry("450x220")
else:
    master.geometry("600x220")
master.config(bg="White")

center(master)

Label(master,text="¡Bienvenidos!", bg='#FFFFFF', height=3).grid(row=0,column=0,columnspan=2)


Button(master, text='Tarea 1', relief="groove", cursor="hand2", fg='Black', bg='#DFF0D8', width=15, height=5, command=lambda: ejecutar("tarea1.py"),activebackground="#31b6fd").grid(row=4, column=1, sticky=W, pady=4)


Button(master, text='Tarea 2', relief="groove", cursor="hand2", fg='Black', bg='#F2DEDE', width=15, height=5, command=lambda: ejecutar("tarea2.py")).grid(row=4, column=2, sticky=W, pady=4)

Button(master, text='Ejercicio Libre', relief="groove", cursor="hand2", fg='Black', bg='#FCF8E3', width=15, height=5, command=lambda: ejecutar("tarealibre.py")).grid(row=4, column=3, sticky=W, pady=4)

Button(master, text='Salir', relief="groove", cursor="hand2", fg='White', bg='#f92c57', width=15, height=5, command=exit).grid(row=4, column=4, sticky=W, pady=4)


mainloop()
