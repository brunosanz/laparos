import csv
import scipy.io
import cv2
import numpy as np
from os import listdir
import os.path

def sigmoid(z):
    
    g = 1 / (1 + np.exp(-z))
    
    return g

def redLaparoscopia(Theta1, Theta2, X):

    m = X.ndim

    A_1 = np.zeros((Theta1.shape))
    A_2 = np.zeros((Theta2.shape))

    X = np.r_[[1],X]
    
    X = np.array([X])
    
    a1 = X.T
    
    z2 = np.dot(Theta1, a1)
    
    a2 = sigmoid(z2)
    
    a2 = np.squeeze(np.asarray(a2))#Matriz a vector
    
    a2 = np.r_[[1],a2]
    
    a2 = np.array([a2])
    
    a2 = a2.T
    
    z3 = np.dot(Theta2, a2)
    
    a3 = sigmoid(z3)

    return a3
    
def im2double(im):
    min_val = np.min(im.ravel())
    max_val = np.max(im.ravel())
    out = (im.astype('float') - min_val) / (max_val - min_val)
    return out

def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

def create_blank(width, height, rgb_color=(255, 255, 255)):

    image = np.zeros((height, width, 3), np.uint8)

    color = tuple(reversed(rgb_color))
    
    image[:] = color

    return image

def createImage(directorio, frame_w, frame_h, dir_img):
    
    os.makedirs(dir_img)
    
    for archivo in listdir(directorio):
        img = create_blank(frame_w, frame_h, rgb_color=(0,0,0))
        iniciar = 0
        reader = csv.reader(open(directorio + '/' + archivo, 'rb'))
        for index,row in enumerate(reader):
            if row[0] != "TF":
                if iniciar == 0:
                    lastX, lastY = int(row[0]), int(row[1])
                    iniciar = 1
                cv2.line(img, (int(row[0]), int(row[1])), (lastX, lastY), (255, 255, 255), 1)
                lastX, lastY = int(row[0]), int(row[1])

        cv2.imwrite(dir_img + '/' + archivo + '.png',img)

def suma_Matriz(matriz):
    
    data = []
    mOriginal = matriz.T
    matriz = np.sum(np.around(matriz,3), axis=0)
    index_min = np.argmin(matriz)
    index_max = np.argmax(matriz)
    if index_max != 0:
        index_max = index_max - 1
    
    mOriginal = np.delete(mOriginal, index_min, 0)
    mOriginal = np.delete(mOriginal, index_max, 0)
    
    row , col = mOriginal.shape
    for i in range(0, row):
        data.append(np.argmax(mOriginal[i]))
    
    kind = np.bincount(data)
    return np.argmax(kind) + 1

def showResult(kind):
    reader = csv.reader(open('class.csv', 'rb'))
    
    for index,row in enumerate(reader):
        if int(row[0]) == kind:
            return row[1]
        
def deleteDir(directorio):
    for archivo in listdir(directorio):
        if os.path.exists(directorio + '/' + archivo):
            os.remove(directorio + '/' + archivo)
    os.rmdir(directorio)
            

def principal(directorio):
    
    frame_w = 641
    frame_h = 481
    color = (255, 255, 255)
    font = cv2.FONT_HERSHEY_SIMPLEX

    dir_img = directorio + '/' + 'img'
    dir_datos = directorio + '/' + 'datos'
    suma = 0

    #Cargar pesos 
    mat = scipy.io.loadmat('pesos.mat')

    Theta1 = mat['Theta1']
    Theta2 = mat['Theta2']
    
    resultado = create_blank(frame_w, frame_h, rgb_color=color)
    
    createImage(dir_datos, frame_w, frame_h, dir_img)

    for archivo in listdir(dir_img):
        #Leer imagen
        img = cv2.imread(dir_img + '/' + archivo)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #Convertir matriz a vector
        #X = np.asarray(gray_img).reshape(-1)
        X = gray_img.ravel()
        
        if suma != 1:
            sum_matriz = redLaparoscopia(Theta1,Theta2,X)
            suma = 1
        else:
            sum_matriz = np.concatenate((sum_matriz, redLaparoscopia(Theta1,Theta2,X)), axis=1)

    cv2.putText(resultado, "Resultado:", (20, 60), font, 0.6, 244, 2, 4)
    cv2.putText(resultado, "--------------------------", (20, 100), font, 0.6, 244, 2, 4)
    cv2.putText(resultado, "En esta tarea tienes un " + showResult(suma_Matriz(sum_matriz)) + ".", (20, 120), font, 0.6, 244, 2, 4)
    cv2.putText(resultado, "Presione cualquier tecla para salir...", (20, 160), font, 0.6, 244, 2, 4)
    cv2.imshow("Laparoscopia: Tarea 1", resultado)
    deleteDir(dir_img)
    deleteDir(dir_datos)
    cv2.waitKey(0)
    cv2.destroyAllWindows()