# -*- coding: utf-8 -*-
#!/usr/bin/python
import csv
import cv2
import cv
import numpy as np
from Tkinter import *
import tkMessageBox
import time as tiempo
from time import time
import os.path
import random
import decimal

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
        tkMessageBox.showinfo("App", "No ha indicado un nombre de archivo.")
        iniciar = 1
    else:            
        if archivo == 1:
            try:
                leer = 1
                ver = 1
                img = cv2.imread(e1.get() + ".png",1)
                reader = csv.reader(open(e1.get() + ".csv", 'rb'))
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
            
            reader = csv.reader(open("ideales.csv", 'rb'))
            leer = 1
            iniciar = 0
        
        if leer == 1:
            for index,row in enumerate(reader):
            
                if row[0] == "TF":
                    break
                else:
                    if bandera == -1:
                        cv2.line(espiral, (int(row[0]), int(row[1])), (int(row[0]), int(row[1])), (0, 255, 0), 2)
                        lastX, lastY = int(row[0]), int(row[1])
                        cv2.circle(espiral, (int(row[0]), int(row[1])), 7, 255, -1)
                        bandera = 1
                    else:
                        cv2.line(espiral, (int(row[0]), int(row[1])), (lastX, lastY), (0, 255, 0), 2)
                        lastX, lastY = int(row[0]), int(row[1])
                i = i + 1
    
            if i - 1 == index:
                cv2.circle(espiral, (int(row[0]), int(row[1])), 7, (0,0,255), -1)
            
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
   
    #img_line = create_blank(frame_w, frame_h, rgb_color=color)
    
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
       cap = cv2.VideoCapture(0)
       cap.set(FRAME_PROP_WIDTH, frame_w)
       cap.set(FRAME_PROP_HEIGHT, frame_h)

       inicio = 0
       fin = 0
       detener = 0
       detener_tiempo = False
       inicio_tiempo = 0

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

           max_area2 = 0
           for cnt2 in cnts2:
               area2 = cv2.contourArea(cnt2)
               if area2 > max_area2:
                   max_area2 = area2
                   best_cnt2 = cnt2

           #Inicio y detener
           #cv2.putText(img,"Inicio", (25, frame_h - 25), font, 0.8, 244, 2, 8)
           #cv2.rectangle(img, (10, frame_h - 60), (100, frame_h - 10), (255, 0, 0), 2)

           #cv2.putText(img,"Fin", (frame_w - 85, 45), font, 0.8, 244, 2, 8)
           #cv2.rectangle(img, (frame_w - 100, 10), (frame_w - 10, 60), (0, 0, 255), 2)

           # Ejecutar este bloque solo si se encontro un area

           if max_area > 0:
               # Encontrar el centroide del mejor contorno y marcarlo
               M = cv2.moments(best_cnt)

               cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])

               cv2.circle(img, (cx, cy), 7, 255, -1)
               # Dibujar un rectangulo alrdedor del objeto
               x, y, w, h = cv2.boundingRect(best_cnt)

               if lastX >= 0 and lastY >= 0 and cx >= 0 and cy >= 0:
                    
                #Dibuja recorrido del objeto
                #cv2.line(img_line, (cx, cy), (lastX, lastY), (0, 255, 0), 2)
                
                if (cx == 407 and cy ==240) or (cx == 408 and cy == 240) or (cx == 409 and cy == 240) or (cx == 407 and cy == 241) or (cx == 408 and 241) or (cx == 409 and cy == 241) or (cx == 407 and cy == 242) or (cx == 408 and cy == 242) or (cx == 409 and cy == 242):
                    inicio = 1
                    fin = 0
                    ##start_time = time()
                    if inicio_tiempo == 0:
                        start_time = time()
                        inicio_tiempo = 1

                if (cx == 177 and cy == 383) or (cx == 178 and cy == 383) or (cx == 179 and cy == 383) or (cx == 177 and cy == 384) or (cx == 178 and cy == 384) or (cx == 179 and cy == 384) or (cx == 177 and cy == 384) or (cx == 178 and cy == 385) or (cx == 179 and cy == 385):
                    inicio = 0
                    fin = 1
                    #cv2.putText(img, str(time() - start_time), (170, 60), font, 0.8, 244, 2, 8)

                if inicio == 1 and fin == 0:
                    cv2.rectangle(img, (10, frame_h - 60), (100, frame_h - 10), (255, 0, 0), -1)
                    fo = open(e1.get() + tiempo.strftime("%d-%m-%Y") + ".csv", "a")
                    fo.write(str(cx) + "," + str(cy) + "\n")
                    
                    elapsed_time = time() - start_time
                    minutos = int(float(elapsed_time)) / 60
                    segundos = int(float(elapsed_time)) % 60
                    d = decimal.Decimal(elapsed_time)
                    decimal.getcontext().prec = 4
                    #cv2.putText(img, "Tiempo: " + str(d * 1), (50, 30), font, 0.6, 244, 2, 8)

                
                if fin == 1:                    
                    if detener == 0:
                        elapsed_time = time() - start_time
                        fo = open(e1.get() + tiempo.strftime("%d-%m-%Y") + ".csv", "a+")
                        fo.write("TF" + "," + str(elapsed_time) + "\n")
                        fo.close()
                    cv2.rectangle(img, (frame_w - 100, 10), (frame_w - 10, 60), (0, 0, 255), -1)
                    cv2.add(img,espiral,img)
                    cv2.imwrite(e1.get() + tiempo.strftime("%d-%m-%Y") + ".png",img)
                    detener = 1


               #lastX, lastY = static_pos(cx,cy)
               lastX, lastY = cx, cy

           if max_area2 > 0:
               # Encontrar el centroide del mejor contorno y marcarlo
               M2 = cv2.moments(best_cnt2)

               lastX2, lastY2 = static_pos(cx2,cy2)

               cx2, cy2 = int(M2['m10']/M2['m00']), int(M2['m01']/M2['m00'])

               #cv2.circle(img, (cx2, cy2), 5, (0,255,0), -1)

                # Dibujar un rectangulo alrdedor del objeto
               x2, y2, w2, h2 = cv2.boundingRect(best_cnt2)
               #cv2.rectangle(img, (x2, y2), (x2+w2, y2+h2), (0, 255, 0), 2)

    ##           if lastX2 > 0 and lastY2 > 0 and cx2 > 0 and cy2 > 0:
    ##               cv2.line(img_line2, (cx2, cy2), (lastX2, lastY2), (0, 255, 0), 2)
    ##               fo = open(e1.get() + ".txt", "a+")
    ##               fo.write("X2 = " + str(cx) + "," + "Y2 = " + str(cy) + "\n")


           # Mostrar la imagen original con todos los overlays
           #cv2.add(img,img_line,img)
           #cv2.add(img,img_line2,img)
           cv2.add(img,espiral,img)
           cv2.imshow('Laparoscopia: Tarea 1', img)

           # Mostrar la mascara con los pixeles extraidos
           #cv2.imshow('thresh', thresh)

           # clear the stream in preparation for the next frame
    #       rawCapture.truncate(0)

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
master.geometry("250x200")
master.config(bg="White")

#center(master)

Label(master,text="Bienvenidos!", bg='#FFFFFF').grid(row=0,column=0,columnspan=2)

Label(master, text="Archivo:", bg='#FFFFFF').grid(row=2, column=0)
e1 = Entry(master, width=23, bg='#EEE')
e1.grid(row=2, column=1)


Button(master, text='Iniciar', fg='Black', bg='#DFF0D8', width=20, command=start_camera).grid(row=3, column=1,columnspan=2, sticky=W, pady=4)
#Button(master, text='Detener', fg='Black', bg='#F2DEDE', width=20, command=stop_camera).grid(row=4, column=1, columnspan=2, sticky=W, pady=4)
Button(master, text='Analizar', fg='Black', bg='#FCF8E3', width=20, command=lambda: graficar(1)).grid(row=5, column=1, columnspan=2, sticky=W, pady=4)

Button(master, text='Salir', fg='Black', bg='#D9EDF7', width=20, command=exit).grid(row=6, column=1, columnspan=2, sticky=W, pady=4)

mainloop()
