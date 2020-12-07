import train as train
from passlib.hash import sha256_crypt
from imutils.video import VideoStream
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from ttkthemes import ThemedTk
import face_recognition
import numpy as np
import openpyxl
import stdiomask
import getpass
import imutils
import json
import time
import cv2
import sys
import os

auto_train = False
verbose = False

def mostrar_user():
    wb = openpyxl.load_workbook("data/info.xlsx")
    ws = wb.active
    window = ThemedTk(theme="yaru")
    window.title("Lista de usuarios")
    #window.geometry('350x350')
    txt = scrolledtext.ScrolledText(window,width=50,height=20, font=("Arial Bold", 20))
    
    for i in range(1,ws.max_row):
        nombre = ws.cell(row = i, column = 1).value
        depto = ws.cell(row = i, column = 2).value
        mail = ws.cell(row = i, column = 3).value
        debt = ws.cell(row = i, column = 4).value
        txt.insert(INSERT,nombre + " - " + depto + " - " + str(mail) + " - " + str(debt)+"\n")
        if verbose: print(nombre, " - ", depto)
    
    txt.grid(column=0,row=0)
    window.mainloop()
    #gestion()

def eliminar_user(usuario, depto):
    #mostrar_user()
    encontrado = False
    #usuario = input("Ingrese el nombre del usuario a eliminar : ").upper()
    #depto = input("Ingrese el número de departamento : ")
    try:
        os.remove("data/dataset/"+usuario+"-"+depto+".jpg")
        if verbose: print("IMAGEN DE USUARIO ELIMINADA")   
    except:
        messagebox.showwarning('Error','Imagen de usuario no encontrada')
        if verbose: print("IMAGEN DE USUARIO NO ENCONTRADA")

    wb = openpyxl.load_workbook("data/info.xlsx")
    ws = wb.active
    for i in range(1,ws.max_row):
        usr_cell = ws.cell(row = i, column = 1).value
        dep_cell = ws.cell(row = i, column = 2).value
        if (usr_cell == usuario and dep_cell == depto):
            encontrado = True
            ws.delete_rows(i,1)
            wb.save('data/info.xlsx')  
            messagebox.showwarning('Eliminar usuario','Usuario Eliminado') 
            if verbose: print("USUARIO ELIMINADO DE LA BASE DE DATOS")
            if auto_train: train.train() 
    if (not encontrado):
        messagebox.showwarning('Eliminar usuario','Usuario no encontrado en la base de datos') 
        if verbose: print("USUARIO NO ENCONTRADO EN LA BASE DE DATOS")

def agregar_user(usuario, depto, mail, debt):
    wb = openpyxl.load_workbook("data/info.xlsx")
    ws = wb.active
    encontrado = False
    act_data = True
    capturar = True
    actualizar = False
    for i in range(1,ws.max_row):
        usr_cell = ws.cell(row = i, column = 1).value
        dep_cell = ws.cell(row = i, column = 2).value
        mail_cell = ws.cell(row = i, column = 3).value
        debt_cell = ws.cell(row = i, column = 4).value
        if (usr_cell == usuario and dep_cell == depto):
            encontrado = True
            if verbose: print("USUARIO YA SE ENCUENTRA REGISTRADO")
            #actualizar = input("¿Desea actualizar la imagen del usuario? (Y) Si. (N) No. : ")
            actualizar = messagebox.askyesno('Usuario ya registrado','Usuario ya registrado\n¿Desea actualizar la imagen del usuario?')
            if actualizar: act_data = False
            else: 
                messagebox.showwarning('Captura fotográfica','Actualización de imagen cancelada')
                capturar= False

    if capturar:
        messagebox.showwarning('Captura fotográfica','Presionar "C" para capturar, "Q" para salir.')
        video = True
        #vs = VideoStream(src=0).start()
        vs = VideoStream(0).start()
        cv2.startWindowThread()
        cv2.namedWindow("REGISTRAR USUARIO")
        #time.sleep(2.0)
        
        while video:
            cara = False
            frame = vs.read()
            frame = cv2.flip(frame, 1)
            picture = frame.copy()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_small_frame)

            for (top, right, bottom, left) in face_locations:
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                picture = picture[top:bottom, left:right]
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
                if len(face_locations) == 1:
                    cara = True      
            frame_show = frame.copy()
            frame_show = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            cv2.imshow('REGISTRAR USUARIO', frame_show)
            #cv2.startWindowThread()

            key = cv2.waitKey(1) & 0xFF

            # Presionar "c" para capturar imagen
            if key == ord('c') and cara == True: 
                cv2.imwrite('data/dataset/'+usuario+"-"+depto+'.jpg',picture)
                if verbose: print("IMAGEN CAPTURADA")
                cv2.destroyAllWindows()
                #VideoStream(0).stop()
                vs.stop()
                video = False
                #messagebox.showwarning('Captura fotográfica','Imagen capturada')
                break

            # Presionar "q" para salir
            if key == ord("q"):
                if verbose: print("ENROLAMIENTO CANCELADO")
                cv2.destroyAllWindows()
                #VideoStream(0).stop()
                vs.stop()
                video = False
                act_data = False
                messagebox.showwarning('Captura fotográfica','Enrolamiento Cancelado')
                break

        if ((not encontrado and act_data) or actualizar):
            if actualizar:
                for i in range(1,ws.max_row):
                    usr_cell = ws.cell(row = i, column = 1).value
                    dep_cell = ws.cell(row = i, column = 2).value
                    if (usr_cell == usuario and dep_cell == depto):
                        encontrado = True
                        ws.delete_rows(i,1)
                        wb.save('data/info.xlsx')  
            ws.insert_rows(2)
            ws.cell(row=2, column=1).value = usuario
            ws.cell(row=2, column=2).value = depto
            try:
                ws.cell(row=2, column=3).value = int(mail)
                ws.cell(row=2, column=4).value = int(debt)
            except:
                ws.cell(row=2, column=3).value = 0
                ws.cell(row=2, column=4).value = 0
            wb.save('data/info.xlsx')
            messagebox.showwarning('Agregar usuario','Usuario Agregado')
            if verbose: print("USUARIO AGREGADO A LA BASE DE DATOS")
            if auto_train: train.train()
            #quit()
