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
import rangos

font = cv2.FONT_HERSHEY_DUPLEX
color = (0, 0, 0)

#Ancho y alto del video que se desea capturar:
# 160.0 x 120.0, 176.0 x 144.0, 320.0 x 240.0, 352.0 x 288.0, 640.0 x 480.0
# 800.00 x 600.0, 1280.0 x 720.0

frame_w = 640
frame_h = 480

global iniciar, posiciones1, posiciones2, n_elementos
posiciones1 = []
posiciones2 = []
iniciar = 0
n_elementos = 15

def abrir():
    if e1.get() != "":
        rangos.principal(e1.get() + '-Tarea 2')
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


def tarea2(dibujar, posicion_inicial, posicion_final):
    
    global iniciar, tarea_dos, posiciones1, posiciones2, n_elementos
    tarea_dos = create_blank(frame_w, frame_h, rgb_color=color)
    
    if e1.get() == "":
        tkMessageBox.showinfo("App", "No ha indicado un nombre de usuario.")
        iniciar = 1
    else:    
        if dibujar == 1:
            posiciones1 = []
            posiciones2 = []
            iniciar = 0

            for i in range(0,n_elementos):
                posiciones1.append(str(random.randint(55, 270)) + "," + str(random.randint(60, 350)))
                posiciones2.append(str(random.randint(315, 600)) + "," + str(random.randint(60, 400)))

            for i in range(0,n_elementos):
                xy1 = posiciones1[i].split(',')
                cv2.circle(tarea_dos, (int(xy1[0]),int(xy1[1])), 10, (255,0,0), -1)
                cv2.putText(tarea_dos, str(i), (int(xy1[0]),int(xy1[1])), font, 0.6, (255,255,255), 0, 4)

                xy2 = posiciones2[i].split(',')
                cv2.circle(tarea_dos, (int(xy2[0]),int(xy2[1])), 10, (0,0,255), -1)
                cv2.putText(tarea_dos, str(i), (int(xy2[0]),int(xy2[1])), font, 0.6, (255,255,255), 0, 4)
        else:
            if posicion_inicial != -1:
                del posiciones1[posicion_inicial]

            n1 = len(posiciones1)

            if posicion_final != -1:
                del posiciones2[posicion_final]

            n2 = len(posiciones2)

            for i in range(0,n1):
                xy1 = posiciones1[i].split(',')
                cv2.circle(tarea_dos, (int(xy1[0]),int(xy1[1])), 10, (255,0,0), -1)
                cv2.putText(tarea_dos, str(i), (int(xy1[0]),int(xy1[1])), font, 0.6, (255,255,255), 0, 4)

            for i in range(0,n2):
                xy2 = posiciones2[i].split(',')
                cv2.circle(tarea_dos, (int(xy2[0]),int(xy2[1])), 10, (0,0,255), -1)
                cv2.putText(tarea_dos, str(i), (int(xy2[0]),int(xy2[1])), font, 0.6, (255,255,255), 0, 4)


                
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

def create_blank(width, height, rgb_color=(0, 0, 255)):
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
    
    bandera = 0
    
    start_time = 0
    elapsed_time = 0
    minutos = 0
    segundos = 0
    
    minuto = int(float(e2.get())) / 60
    segundo = int(float(e2.get())) % 60 
   
    #graficar(0)
    tarea2(1,-1,-1)

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
       encontrar = 0
       score = 0
       contador = 0
       start = 0
       iniciar_tiempo = 0
       cerrar_archivo = 0
       abrir_archivo = 0
       guardar_imagen = 1
       prueba = 1
    
       while cap.isOpened():
            
           if start == 1 and iniciar_tiempo == 0:
            start_time = time()
            start = 0
            iniciar_tiempo = 1
            
           if iniciar_tiempo == 1:
            elapsed_time = time() - start_time
            
           minutos = int(float(elapsed_time)) / 60
           segundos = int(float(elapsed_time)) % 60

           # Leer un frame
           _, img = cap.read()
            
           # Aplicar desenfoque para eliminar ruido
           frame = cv2.blur(img, (15, 15))

           # Convertir frame de BRG a HSV
           hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

           # Aplicar umbral a la imagen y extraer los pixeles en el rango de colores
           thresh = cv2.inRange(hsv, lower_color_green,upper_color_green)

           # Encontrar los contornos en la imagen extraida
           cnts, h = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

           #Encontrar el contorno de mayor area y especificarlo como best_cnt
           max_area = 0
           for cnt in cnts:
               area = cv2.contourArea(cnt)
               if area > max_area:
                   max_area = area
                   best_cnt = cnt
                    
           # Ejecutar este bloque solo si se encontro un area

           if max_area > 0:
               # Encontrar el centroide del mejor contorno y marcarlo
               M = cv2.moments(best_cnt)

               cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])

               cv2.circle(img, (cx, cy), 7, 255, -1)
               #cv2.putText(img, str(cx) + "," +str(cy), (50, 60), font, 0.6, (255,255,255), 0, 4)
            
               if bandera == 1:
                    cv2.circle(img, (cx, cy), 10, (255,0,0), -1)
                    cv2.putText(img, str(posicion), (cx,cy), font, 0.7, (255,255,255), 0, 4)
                    fo = open(e1.get()  + '-Tarea 2' + "/" + e1.get() + "-tarea 2-" + "prueba " + str(prueba) + "-" + tiempo.strftime("%d-%m-%Y") + ".csv", "a+")
                    #--fo.write(str(cx) + "," + str(cy) + "\n")
                    fo.close()
                    
               # Dibujar un rectangulo alrededor del objeto
               #x, y, w, h = cv2.boundingRect(best_cnt)
               #cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

               if lastX >= 0 and lastY >= 0 and cx >= 0 and cy >= 0:
                
                for i in range(0,len(posiciones1)):
                                        
                    puntos = posiciones1[i].split(',')
                
                    punto = str(cx) + "," + str(cy)
                    
                    if( (punto == posiciones1[0]) or (cx == int(puntos[0]) and cy == int(puntos[1]) - 2 ) or ( cx == int(puntos[0])  + 2 and cy == int(puntos[1])) or (cx == int(puntos[0]) and cy == int(puntos[1])  + 2) or (cx == int(puntos[0])  - 2 and cy == int(puntos[1]))):
                        cv2.circle(img, (cx, cy), 10, (0,255,0), -1)
                        bandera = 1
                        posicion = i
                        encontrar = 1
                        start = 1
                    
                if encontrar == 1:
                
                    puntos2 = posiciones2[posicion].split(',')
                
                    punto2 = str(cx) + "," + str(cy)                                            
                    
                    if( (punto2 == posiciones2[0]) or (cx == int(puntos2[0]) and cy == int(puntos2[1]) - 2 ) or ( cx == int(puntos2[0])  + 2 and cy == int(puntos2[1])) or (cx == int(puntos2[0]) and cy == int(puntos2[1])  + 2) or (cx == int(puntos2[0])  - 2 and cy == int(puntos2[1]))):
                        cv2.circle(img, (cx, cy), 10, (0,255,0), -1)
                        bandera = 0
                        tarea2(0,posicion,posicion)
                        encontrar = 0
                        score += 1
                        contador += 1

               lastX, lastY = cx, cy


           # Mostrar la imagen original con todos los overlays
        
           if minuto == minutos and segundo == segundos:
            cv2.putText(img, "Tiempo Finalizado!", (50, 30), font, 0.6, (255,255,255), 0, 4)
            cv2.putText(img, "Puntaje: " + str(score), (50, 90), font, 0.6, (255,255,255), 0, 4)
            detener_tiempo = True
            bandera = 0
            if cerrar_archivo == 0:
                fo = open(e1.get()  + '-Tarea 2' + "/" + e1.get() + "-tarea 2-" + "prueba " + str(prueba) + "-" + tiempo.strftime("%d-%m-%Y") + ".csv", "a")
                fo.write("Aciertos" + "," + str(score) + "\n")
                fo.close()
                cerrar_archivo = 1
           else:
            if detener_tiempo == True:
                cv2.putText(img, "Tiempo Finalizado!", (50, 30), font, 0.6, (255,255,255), 0, 4)
                cv2.putText(img, "Puntaje: " + str(score), (50, 90), font, 0.6, (255,255,255), 0, 4)
                bandera = 0
                if prueba != int(pack.get()):
                    prueba = prueba + 1
                    detener_tiempo = False
                    start = 0
                    iniciar_tiempo = 0
                    cerrar_archivo = 0
                    score = 0
                    bandera = 0
                    start_time = 0
                    elapsed_time = 0
                    minutos = 0
                    segundos = 0
                    contador = 0
                    tarea2(1,-1,-1)
            else:
                if n_elementos == contador or detener_tiempo == True:
                    cv2.putText(img, "Puntaje: " + str(score), (50, 60), font, 0.6, (255,255,255), 0, 4)
                    bandera = 0
                    if cerrar_archivo == 0:
                        fo = open(e1.get()  + '-Tarea 2' + "/" + e1.get() + "-tarea 2-" + "prueba " + str(prueba) + "-" + tiempo.strftime("%d-%m-%Y") + ".csv", "a")
                        fo.write("Aciertos" + "," + str(score) + "\n")
                        fo.close()
                        cerrar_archivo = 1
                    
                else:
                    cv2.putText(img,"Prueba " + str(prueba), (35, 20), font, 0.6, (255,255,255), 0, 4)
                    d = decimal.Decimal(elapsed_time)
                    decimal.getcontext().prec = 4
                    cv2.putText(img, "Tiempo: " + str(minutos) + " minuto(s), " + str(segundos) + " segundo(s).", (50, 30), font, 0.6, 244, 2, 8)
                    tiempo_realizado = d * 1
                    cv2.putText(img, "Tiempo: " + str(tiempo_realizado), (50, 60), font, 0.6, (255,255,255), 0, 4)
                    cv2.add(img,tarea_dos, img)
                    
            
           # perform the actual resizing of the image and show it
           #------resized = cv2.resize(img, (1366,768), interpolation = cv2.INTER_AREA)    
           cv2.imshow("Laparoscopia: Tarea 2", img)    

           # Salir del bucle si se presiona ESC
           k = cv2.waitKey(5) & 0xFF
           if k == 27:
               # Limpieza y fin de programa
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

Label(master,text="Tarea 2", bg='#FFFFFF').grid(row=0,column=0,columnspan=2)

Label(master, text="Usuario:", bg='#FFFFFF').grid(row=2, column=0)
e1 = Entry(master, width=23, bg='#EEE')
e1.grid(row=2, column=1)

Label(master, text="Repeticiones:", bg='#FFFFFF').grid(row=3, column=0)

pack = ttk.Combobox(master, state="readonly", values=('5','6','7','8'))
pack.grid(row=3, column=1,columnspan=2, sticky=W, pady=4)
pack.set("5")

Label(master, text="Tiempo:", bg='#FFFFFF').grid(row=4, column=0)
e2 = Entry(master, width=23, bg='#EEE')
e2.grid(row=4, column=1)
e2.insert(0, "80")
Label(master, text="segundos.", bg='#FFFFFF').grid(row=4, column=3)

Button(master, text='Iniciar',cursor="hand2", fg='Black', bg='#DFF0D8', width=20, command=lambda:createDir(e1.get() + '-Tarea 2')).grid(row=5, column=1,columnspan=2, sticky=W, pady=4)
Button(master, text='Analizar',cursor="hand2", fg='Black', bg='#FCF8E3', width=20, command=abrir).grid(row=6, column=1, columnspan=2, sticky=W, pady=4)

Button(master, text='Salir', cursor="hand2", fg='Black', bg='#D9EDF7', width=20, command=exit).grid(row=7, column=1, columnspan=2, sticky=W, pady=4)

mainloop()
