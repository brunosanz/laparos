import csv
import numpy as np
from Tkinter import *
import ttk
import tkMessageBox
import cv2
import os.path
import decimal
import time as tiempo
import time
from os import listdir
import redlaparoscopia

font = cv2.FONT_HERSHEY_SIMPLEX

def createDir(directorio):
    if os.path.exists(directorio):
        deleteDir(directorio)
        os.makedirs(directorio)
    else:
        os.makedirs(directorio)
        
def deleteDir(directorio):
    for archivo in listdir(directorio):
        if os.path.exists(directorio + '/' + archivo):
            os.remove(directorio + '/' + archivo)
    os.rmdir(directorio)

def separar(numero):
    parte_entera = int(numero) #Parte entera con o sin signo
    parte_decimal = abs(numero) - abs(int(numero)) #Parte decimal
    
    return parte_entera, parte_decimal  
    
def norm(directorio_raiz, nombre_archivo):
    lista_original = []
    lista_final = []
    arreglo_quitar = []
    contador = 0
    tiempo = []
    dir_dat = 'datos'

    reader = csv.reader(open('norepetidos.csv', 'r'))

    for index,row in enumerate(reader):
        lista_original.append(row[0] + "," + row[1])
        contador+=1

    if os.path.exists("normalizados.csv"):
        os.remove("normalizados.csv")

    for i in xrange(0,contador,(contador / 229)):
        fo = open("normalizados.csv", "a")
        fo.write(str(lista_original[i]) + "\n")
        
    tiempo.append(str(lista_original[contador - 1]))
        
    fo.close()
    
    if os.path.exists(nombre_archivo):
        os.remove(nombre_archivo)
    
    contador = 0
    
    reader = csv.reader(open('normalizados.csv', 'r'))

    for index,row in enumerate(reader):
        lista_final.append(row[0] + "," + row[1])
        contador+=1
    
    contador = contador - 1
    
    parte_entera, parte_decimal = separar(decimal.Decimal(contador) / decimal.Decimal(229))

    quitar_numero = parte_decimal * contador
    
    parte_entera, parte_decimal = separar(quitar_numero)
    
    contador_final = 0
    posicion = 0
    
    for j in range (0, parte_entera):
        arreglo_quitar.append((j + 1)  * (contador / parte_entera))
        
    for i in range(0,contador):
        if posicion < parte_entera:
            if arreglo_quitar[posicion] == i:
                posicion+=1
            else:
                contador_final+=1
        else:
            contador_final+=1

    if contador_final != 229:
        quitar = contador_final - 229
    else:
        quitar = 0
    
    for k in range (0, (parte_entera - abs(quitar))):
        arreglo_quitar.append((k + 1)  * (contador / parte_entera - abs(quitar)))
    
    posicion = 0
    
    for i in range(0,contador):
        if posicion < parte_entera - abs(quitar):
            if arreglo_quitar[posicion] == i:
                posicion+=1
            else:
                fo = open(directorio_raiz + '/' + dir_dat + '/' + nombre_archivo.lstrip(directorio_raiz + '/'), "a")
                fo.write(str(lista_final[i]) + "\n")
        else:
            fo = open(directorio_raiz + '/' + dir_dat + '/' + nombre_archivo.lstrip(directorio_raiz + '/'), "a")
            fo.write(str(lista_final[i]) + "\n")
    
    fo.write(tiempo[0])

    fo.close()

def quitar_repetidos(nombre_datos):
    lista_original = []
    lista_nueva = []
    contador = 0
    j = 0

    reader = csv.reader(open(nombre_datos, 'r'))

    for index,row in enumerate(reader):
        lista_original.append(row[0] + "," + row[1])
        contador+=1

    if os.path.exists("norepetidos.csv"):
        os.remove("norepetidos.csv")

    for i in lista_original:
        if i not in lista_nueva:
            fo = open("norepetidos.csv", "a")
            fo.write(i + "\n")
            lista_nueva.append(i)
            j+=1

    fo.close()

def graficar(nombre_imagen, nombre_datos, nombre_ventana,guardar_nombre_imagen, n):
    
    lastX = -1
    lastY = -1
    bandera = -1
    minutos = 0.0
    segundos = 0.0

    img = cv2.imread(nombre_imagen,1)

    reader = csv.reader(open(nombre_datos, 'rb'))
    for index,row in enumerate(reader):
        #cv2.waitKey(100)
        if row[0] == "TF":
            minutos = int(float(row[1])) / 60
            segundos = int(float(row[1])) % 60
            cv2.putText(img, "Tiempo: " + str(minutos) + " minuto(s), " + str(segundos) + " segundo(s).", (50, 30), font, 0.6, 244, 2, 8)
            break
        else:
            if bandera == -1:
                cv2.line(img, (int(row[0]), int(row[1])), (int(row[0]), int(row[1])), (0, 0, 255), 2)
                lastX, lastY = int(row[0]), int(row[1])
                bandera = 1
            else:
                cv2.line(img, (int(row[0]), int(row[1])), (lastX, lastY), (0, 0, 255), 2)
                lastX, lastY = int(row[0]), int(row[1])
   
    cv2.imshow(nombre_ventana + " " + n,img)
    cv2.imwrite(guardar_nombre_imagen,img)

def datos(directorio):
    
    directorio_raiz = directorio
    dir_dat = 'datos'
    createDir(directorio_raiz + '/' + dir_dat)
    
    for archivo in os.listdir(directorio):
        path = os.path.join(directorio, archivo)
        if os.path.isdir(path):
            continue
        else:
            quitar_repetidos(directorio + '/' + archivo)
            norm(directorio_raiz, directorio + '/' + archivo.strip('.csv') + '-final.csv')
    
    if os.path.exists("normalizados.csv"):
        os.remove("normalizados.csv")
    if os.path.exists("norepetidos.csv"):
        os.remove("norepetidos.csv")
    redlaparoscopia.principal(directorio)