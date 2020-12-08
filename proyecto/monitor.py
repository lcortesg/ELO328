'''
@File    :   monitor.py
@Date    :   2020/12/07
@Author  :   Lucas Cortés Gutiérrez.
@Version :   2.0
@Contact :   lucas.cortes.14@sansano.usm.cl"
@Desc    :   Módulo de monitoreo del sistema de reconocimineto de personas "Let Me In"
'''

from tkinter import messagebox
from imutils import paths
import face_recognition
from tkinter import *
import numpy as np
import openpyxl
import pickle
import time
import cv2
import os

def monitor_kill():
    # Libera la cámara y destruye las ventanas
    cv2.VideoCapture(0).release()
    #video_capture.release()
    cv2.destroyAllWindows()

def monitor():
    ultimos = []
    before = time.time()

    with open('data/model.dat', 'rb') as f:
        all_face_encodings = pickle.load(f)
    
    tolerance = 0.6
    video_capture = cv2.VideoCapture(0)
    
    wb = openpyxl.load_workbook("data/info.xlsx")
    ws = wb.active

    known_face_names = list(all_face_encodings.keys())
    known_face_encodings = np.array(list(all_face_encodings.values()))

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    time.sleep(2)
    
    while True:
        ret, frame = video_capture.read()
        frame = cv2.flip(frame, 1)

        # Escalar la imagen a 1/4 de la original
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # convertir la imagen desde BGR a RGB
        rgb_small_frame = small_frame[:, :, ::-1]

        # Se procesa 1 de cada 2 frames
        if process_this_frame:
            # Encuentra todas las caras en un frame dado
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # Revisar coincidencias
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance)
                #matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Desconocido"

                # # Se utiliza la primera coincidencia encontrada en known_face_encodings.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Se utiliza la mejor coincidencia a la cara detectada.
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    
                now = time.time()
                tiempo = time.localtime(now)
                time_log = time.strftime("%Y/%m/%d, %H:%M:%S", tiempo)
                time_pic = time.strftime("%Y-%m-%d, %H-%M-%S", tiempo)
                if name not in ultimos:
                    f = open("data/log.txt","a+")
                    f.write(time_log+" - "+name+"\r\n")
                    f.close
                    cv2.imwrite('data/log_img/'+time_pic+" - "+name+'.jpg',frame)
                    ultimos.append(name)

                if int(now - before) > 60:
                    before = time.time()
                    ultimos.clear()

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Muestra los resultados
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            depto = "Desconocido"
            correo = "0"
            deudas = "0"
            user = name.split("-")
            
            for j in range(1,ws.max_row):
                if (ws.cell(row = j, column = 1).value == user[0] and ws.cell(row = j, column = 2).value == user[1]):
                    name = user[0]
                    depto = user[1]
                    correo = str(ws.cell(row = j, column = 3).value)
                    deudas = str(ws.cell(row = j, column = 4).value)

            # Desescalar la imagen
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            font = cv2.FONT_HERSHEY_DUPLEX
            if (name == "Desconocido"):
                # Dibujar cuadrado
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Dibujar etiqueta
                cv2.rectangle(frame, (left, bottom-35), (right, bottom), (0, 0, 255), cv2.FILLED)
                
            else:
                # Dibujar cuadrado
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                # Dibujar etiqueta con nombre
                cv2.rectangle(frame, (left, bottom-35), (right, bottom), (0, 255, 0), cv2.FILLED)

                if (depto == "Desconocido"):
                    cv2.rectangle(frame, (left-1, bottom+35), (right+1, bottom), (0, 0, 255), cv2.FILLED)
                if (depto != "Desconocido"):
                    cv2.rectangle(frame, (left-1, bottom+35), (right+1, bottom), (0, 255, 0), cv2.FILLED)

                cv2.putText(frame,"Depto. "+depto, (left+6, bottom+30), font, 1.0, (255, 255, 255), 1)

                if (int(correo) > 0):
                    cv2.rectangle(frame, (left-1, bottom+35), (right+1, bottom+65), (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame, "Correo "+correo, (left+6, bottom+60), font, 1.0, (255, 255, 255), 1)

                if (int(deudas) > 0):
                    cv2.rectangle(frame, (left-1, bottom+65), (right+1, bottom+95), (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame, "Deudas "+deudas, (left+6, bottom+90), font, 1.0, (255, 255, 255), 1)

            cv2.putText(frame, name, (left+6, bottom-6), font, 1.0, (255, 255, 255), 1)

        # Muestra imagen resultante
        frame = cv2.resize(frame, (0, 0), fx=0.8, fy=0.8)
        cv2.imshow('Video', frame)

        # Presionar "q" para salir
        #if cv2.waitKey(1) & 0xFF == ord('q'): break
        if cv2.waitKey(1) & 0xFF == 27: break

    # Libera la cámara y destruye las ventanas
    video_capture.release()
    cv2.destroyAllWindows()
    
