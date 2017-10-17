#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import cv2
import cv
import numpy as np
from Tkinter import *
import ttk
import tkMessageBox
import time as tiempo
from time import time
import os.path
import random
import decimal
from os import listdir
import sys
import normalizar

font = cv2.FONT_HERSHEY_SIMPLEX
color = (0, 0, 0)

#Ancho y alto del video que se desea capturar:
# 160.0 x 120.0, 176.0 x 144.0, 320.0 x 240.0, 352.0 x 288.0, 640.0 x 480.0
# 800.00 x 600.0, 1280.0 x 720.0

frame_w = 640
frame_h = 480

global iniciar, posiciones1
posiciones1 = []
iniciar = 0

def abrir():
    if e1.get() != "":
        normalizar.datos(e1.get() + '-Tarea 1')
    else:
        tkMessageBox.showinfo("App", "No ha indicado un nombre de usuario.")

def createDir(directorio):
    if os.path.exists(directorio):
        tkMessageBox.showinfo("App", "El nombre de usuario ya existe.")
    else:
        if e1.get() != "":
            os.mkdir(directorio)
            start_camera()
        else:
            tkMessageBox.showinfo("App", "No ha indicado un nombre de usuario.")


def graficar(archivo):
    
    global espiral, iniciar
    espiral = create_blank(frame_w, frame_h, rgb_color=color)
    lastX = -1
    lastY = -1
    bandera = -1
    leer = 0
    ver = 0
    i = 0
    
    if e1.get() == "":
        tkMessageBox.showinfo("App", "No ha indicado un nombre de usuario.")
        iniciar = 1
    else:            
        if archivo == 1:
            try:
                leer = 1
                ver = 1
                img = cv2.imread(e1.get() + tiempo.strftime("%d-%m-%Y") + ".png",1)
                reader = csv.reader(open(e1.get() + tiempo.strftime("%d-%m-%Y") + ".csv", 'rb'))
                espiral = img
            except Exception:
                leer = 0
                ver = 0
                iniciar = 0
                tkMessageBox.showwarning("App", "No se encontró el archivo. Intente con otro.")
                pass                
        else:
            if os.path.exists(e1.get() + ".csv"):
                os.remove(e1.get() + ".csv")
            
            reader = csv.reader(open("espiral.csv", 'rb'))
            leer = 1
            iniciar = 0
        
        if leer == 1:
            for index,row in enumerate(reader):
                if row[0] == "TF":
                    minutos = int(float(row[1])) / 60
                    segundos = int(float(row[1])) % 60
                    cv2.putText(img, "Tiempo: " + str(minutos) + " minuto(s), " + str(segundos) + " segundo(s).", (250, 20), font, 0.6, 244, 2, 8)
                    break
                else:
                    if bandera == -1:
                        if archivo != 1:
                            cv2.line(espiral, (int(row[0]), int(row[1])), (int(row[0]), int(row[1])), (0, 255, 0), 2)
                            lastX, lastY = int(row[0]), int(row[1])
                        else:
                            cv2.line(espiral, (int(row[0]), int(row[1])), (int(row[0]), int(row[1])), (0, 0, 255), 2)
                            lastX, lastY = int(row[0]), int(row[1])
                        bandera = 1
                    else:
                        if archivo != 1:#archivo del practicante
                            cv2.line(espiral, (int(row[0]), int(row[1])), (lastX, lastY), (0, 255, 0), 2)
                            lastX, lastY = int(row[0]), int(row[1])
                        else:
                            cv2.line(espiral, (int(row[0]), int(row[1])), (lastX, lastY), (0, 0, 255), 2)
                            lastX, lastY = int(row[0]), int(row[1])
                i = i + 1
            
        if ver == 1:
            cv2.imshow('Graficar Recorrido',espiral)
            k = cv2.waitKey(0) & 0xFF
            if k == 27:         # wait for ESC key to exit
                cv2.destroyAllWindows()
    
                
def rotateImage(image, angle):
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
 
    # rotate the image by 180 degrees
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def show_entry_fields():
   print("Nombre del archivo: %s" % (e1.get()))

def static_pos(posX,posY):
    static_pos.cx = posX
    static_pos.cy = posY
    return static_pos.cx, static_pos.cy
   
def center(ventana):
    ventana.update_idletasks()
    w=ventana.winfo_width()
    h=ventana.winfo_height()
    extraW=ventana.winfo_screenwidth()-w
    extraH=ventana.winfo_screenheight()-h
    ventana.geometry("%dx%d%+d%+d" % (w,h,extraW/2,extraH/2))

def create_blank(width, height, rgb_color=(255, 255, 255)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image

def start_camera():
    
    cx = 0
    cy = 0

    cx2 = 0
    cy2 = 0

    lastX = -1
    lastY = -1
    
    graficar(0)

    if iniciar != 1:
       # Indices de las propiedades de video (no editar)
       FRAME_PROP_WIDTH = 3
       FRAME_PROP_HEIGHT = 4
       # Definir rango de color a identificar (HSV)
       lower_color_blue = np.array([90, 90, 90], dtype=np.uint8)
       upper_color_blue = np.array([120, 255, 255], dtype=np.uint8)

       lower_color_green = np.array([31,38,30], dtype=np.uint8)
       upper_color_green = np.array([49,255,255], dtype=np.uint8)
       
       # Iniciar captura de video con el tamano deseado
       cap = cv2.VideoCapture(1)
       cap.set(FRAME_PROP_WIDTH, frame_w)
       cap.set(FRAME_PROP_HEIGHT, frame_h)

       inicio = 0
       fin = 0
       detener = 0
       detener_tiempo = False
       inicio_tiempo = 0
       prueba = 1
       finalizar = 0

       while cap.isOpened():   

           # Leer un frame
           _, img = cap.read()
            
           # Aplicar desenfoque para eliminar ruido
           frame = cv2.blur(img, (15, 15))

           # Convertir frame de BRG a HSV
           hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

           # Aplicar umbral a la imagen y extraer los pixeles en el rango de colores
           thresh = cv2.inRange(hsv, lower_color_green,upper_color_green)
           thresh2 = cv2.inRange(hsv, lower_color_green,upper_color_green)

           # Encontrar los contornos en la imagen extraida
           cnts, h = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
           cnts2, h2 = cv2.findContours(thresh2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

           #Encontrar el contorno de mayor area y especificarlo como best_cnt
           max_area = 0
           for cnt in cnts:
               area = cv2.contourArea(cnt)
               if area > max_area:
                   max_area = area
                   best_cnt = cnt

           # Ejecutar este bloque solo si se encontro un area
           cv2.circle(img, (408,241), 7, 255, -1)
            
           cv2.circle(img, (178,384), 7, (0,0,255), -1)
           if max_area > 0:
               # Encontrar el centroide del mejor contorno y marcarlo
               M = cv2.moments(best_cnt)

               cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])

               cv2.circle(img, (cx, cy), 7, 255, -1)
               # Dibujar un rectangulo alrdedor del objeto
               x, y, w, h = cv2.boundingRect(best_cnt)

               #cv2.putText(img, str(cx) + "," + str(cy), (cx, cy), font, 0.5, 244, 2, 8)
                          
               if lastX >= 0 and lastY >= 0 and cx >= 0 and cy >= 0:
                    
                #Dibuja recorrido del objeto
                #cv2.line(img_line, (cx, cy), (lastX, lastY), (0, 255, 0), 2)
                
                if (cx == 407 and cy ==240) or (cx == 408 and cy == 240) or (cx == 409 and cy == 240) or (cx == 407 and cy == 241) or (cx == 408 and 241) or (cx == 409 and cy == 241) or (cx == 407 and cy == 242) or (cx == 408 and cy == 242) or (cx == 409 and cy == 242):
                    inicio = 1
                    fin = 0
                    detener = 0
                    if inicio_tiempo == 0:
                        start_time = time()
                        inicio_tiempo = 1

                if (cx == 177 and cy == 383) or (cx == 178 and cy == 383) or (cx == 179 and cy == 383) or (cx == 177 and cy == 384) or (cx == 178 and cy == 384) or (cx == 179 and cy == 384) or (cx == 177 and cy == 384) or (cx == 178 and cy == 385) or (cx == 179 and cy == 385):
                    inicio = 0
                    fin = 1
                    #cv2.putText(img, str(time() - start_time), (170, 60), font, 0.8, 244, 2, 8)

                if inicio == 1 and fin == 0:
                    #Mensaje al iniciar la tarea
                    #cv2.circle(img, (25, frame_h - 25), 8, (0, 0, 255), -1)
                    #cv2.putText(img,"Finalizar", (35, frame_h - 20), font, 0.6, (0, 0, 255), 2, 2)
                    #cv2.putText(img,"Esc-Salir", (125, frame_h - 20), font, 0.6, (0, 255, 0), 2, 2)
                    cv2.circle(img, (25, 15), 8, (0, 0, 255), -1)
                    cv2.putText(img,"Finalizar", (35, 20), font, 0.6, (0, 0, 255), 2, 2)
                    cv2.putText(img,"Esc-Salir", (125, 20), font, 0.6, (0, 255, 0), 2, 2)
        
                    fo = open(e1.get()  + '-Tarea 1' + "/" + e1.get() + "-tarea 1-" + "prueba " + str(prueba) + "-" + tiempo.strftime("%d-%m-%Y") + ".csv", "a")
                    fo.write(str(cx) + "," + str(cy) + "\n")
                    
                    elapsed_time = time() - start_time
                    minutos = int(float(elapsed_time)) / 60
                    segundos = int(float(elapsed_time)) % 60
                    d = decimal.Decimal(elapsed_time)
                    decimal.getcontext().prec = 4
                else:
                    cv2.circle(img, (25,15), 8, (255, 0, 0), -1)
                    if finalizar == 0:
                        cv2.putText(img,"Iniciar Prueba " + str(prueba), (35, 20), font, 0.6, 244, 2, 2)
                    else:
                        cv2.putText(img,"Fin de Pruebas ", (35, 20), font, 0.6, 244, 2, 2)
                    cv2.putText(img,"Esc-Salir", (200, 20), font, 0.6, (0, 255, 0), 2, 2)
                                    
                if fin == 1:                    
                    if detener == 0:
                        elapsed_time = time() - start_time
                        fo = open(e1.get() + '-Tarea 1' + "/" + e1.get() + "-tarea 1-" + "prueba " + str(prueba) + "-" + tiempo.strftime("%d-%m-%Y") + ".csv", "a+")
                        fo.write("TF" + "," + str(elapsed_time) + "\n")
                        fo.close()
                        detener = 1
                        
                    #Realizar otra prueba.
                        if prueba != int(pack.get()):
                            inicio = 0
                            fin = 0
                            detener_tiempo = False
                            inicio_tiempo = 0
                            prueba = prueba + 1
                        else:
                             finalizar = 1
                                
               #lastX, lastY = static_pos(cx,cy)
               lastX, lastY = cx, cy

           
           # we need to keep in mind aspect ratio so the image does
           # not look skewed or distorted -- therefore, we calculate
           # the ratio of the new image to the old image
           r = 100.0 / img.shape[1]
           dim = (100, int(img.shape[0] * r))
           
           
           cv2.add(espiral,img,img)        
            
           # perform the actual resizing of the image and show it
           #w,h = master.maxsize()
           #resized = cv2.resize(img, (w,h), interpolation = cv2.INTER_AREA)    
           cv2.imshow("Laparoscopia: Tarea 1", img)

           # Salir del bucle si se presiona ESC
           k = cv2.waitKey(5) & 0xFF
           if k == 27:
               # Limpieza y fin de programa
    ##           cap.release()
               cv2.destroyAllWindows()
               break
         

master = Tk()
master.title("Laparoscopía")
master.resizable(0,0)
if sys.platform == "win32":
    master.geometry("300x220")
else:
    master.geometry("350x220")
master.config(bg="White")

center(master)

Label(master,text="Tarea 1", bg='#FFFFFF').grid(row=0,column=0,columnspan=2)

Label(master, text="Usuario:", bg='#FFFFFF').grid(row=2, column=0)
e1 = Entry(master, width=23, bg='#EEE')
e1.grid(row=2, column=1)

Label(master, text="Repeticiones:", bg='#FFFFFF').grid(row=3, column=0)

pack = ttk.Combobox(master, state="readonly", values=('5','6','7','8'))
pack.grid(row=3, column=1,columnspan=2, sticky=W, pady=4)
pack.set("5")

Button(master, text='Iniciar', cursor="hand2", fg='Black', bg='#DFF0D8', width=20, command=lambda:createDir(e1.get() + '-Tarea 1')).grid(row=4, column=1,columnspan=2, sticky=W, pady=4)
Button(master, text='Analizar', cursor="hand2", fg='Black', bg='#FCF8E3', width=20, command=abrir).grid(row=5, column=1, columnspan=2, sticky=W, pady=4)

Button(master, text='Salir', cursor="hand2", fg='Black', bg='#D9EDF7', width=20, command=exit).grid(row=6, column=1, columnspan=2, sticky=W, pady=4)

mainloop()
