from imutils.video import VideoStream
import face_recognition
import numpy as np
import argparse
import openpyxl
import imutils
import time
import cv2
import sys
import os

#wb = openpyxl.load_workbook("info.xlsx")
#ws = wb.active

while True:
    modo = input("(A) Agregar Usuario. (E) Eliminar Usuario. (M) Mostrar Usuarios. (Q) Salir. : ")
    eliminar = False
    agregar = False

    if (modo == "Q" or modo == "q"):
        exit()
    if (modo == "E" or modo == "e"):
        eliminar = True
    if (modo == "A" or modo == "a"):
        agregar = True
    if (modo == "M" or modo == "m"):
        mostrar = True

    if mostrar:
        wb = openpyxl.load_workbook("info.xlsx")
        ws = wb.active
        for i in range(1,ws.max_row):
            nombre = ws.cell(row = i, column = 1).value
            depto = ws.cell(row = i, column = 2).value
            correo = ws.cell(row = i, column = 3).value
            deudas = ws.cell(row = i, column = 4).value
            print(nombre, depto, correo, deudas)

    if eliminar:
        encontrado = False
        usuario = input("Ingrese el nombre del usuario a eliminar : ")
        try:
            os.remove("dataset/"+usuario+".jpg")
            print("IMAGEN DE USUARIO ELIMINADA")   
        except:
            print("IMAGEN DE USUARIO NO ENCONTRADA")

        wb = openpyxl.load_workbook("info.xlsx")
        ws = wb.active
        for i in range(1,ws.max_row):
            cell = ws.cell(row = i, column = 1).value
            if (cell == usuario):
                encontrado = True
                ws.delete_rows(i,1)
                wb.save('info.xlsx')   
                print("USUARIO ELIMINADO DE LA BASE DE DATOS") 
        if (not encontrado):
            print("USUARIO NO ENCONTRADO EN LA BASE DE DATOS")

    if agregar:
        usuario = input("Ingrese el nombre del usuario a enrolar : ")
        encontrado = False

        wb = openpyxl.load_workbook("info.xlsx")
        ws = wb.active

        for i in range(1,ws.max_row):
            cell = ws.cell(row = i, column = 1).value
            if (cell == usuario):
                print("USUARIO YA SE ENCUENTRA REGISTRADO")
                encontrado = True
                video = False
                agregar = False
                break

        if (agregar):
            depto = input("Ingrese numero de departamento : ")
            print("(C) Capturar Imagen. (Q) Salir. : ")
            video = True
            #vs = VideoStream(src=0).start()
            vs = VideoStream(0).start()
            cv2.startWindowThread()
            cv2.namedWindow("REGISTRAR USUARIO")
            #time.sleep(2.0)
        
        while video:
            if encontrado:
                video = False
                break
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
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
                cara = True

            cv2.imshow('REGISTRAR USUARIO', frame)
            #cv2.startWindowThread()

            key = cv2.waitKey(1) & 0xFF

             # Utilizar tecla "c" para capturar imagen
            if key == ord('c') and cara == True: 
                cv2.imwrite('dataset/'+usuario+'.jpg',picture)
                print("IMAGEN CAPTURADA")
                cv2.destroyAllWindows()
                #VideoStream(0).stop()
                vs.stop()
                video = False
                break
         
            if key == ord("q"):
                print("ENROLAMIENTO CANCELADO")
                cv2.destroyAllWindows()
                #VideoStream(0).stop()
                vs.stop()
                video = False
                agregar = False
                break

        if (not encontrado and agregar):
            ws.insert_rows(2)
            ws.cell(row=2, column=1).value = usuario
            ws.cell(row=2, column=2).value = depto
            ws.cell(row=2, column=3).value = 0
            ws.cell(row=2, column=4).value = 0
            wb.save('info.xlsx')
            agregar = False
            print("USUARIO AGREGADO A LA BASE DE DATOS")
        
    