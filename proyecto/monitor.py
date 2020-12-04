from imutils import paths
import face_recognition
import numpy as np
import openpyxl
import cv2
import os

def reconocer():
    tolerance = 0.6
    video_capture = cv2.VideoCapture(0)
    imagePaths = list(paths.list_images('data/img'))
    known_face_encodings = []
    known_face_names = []

    wb = openpyxl.load_workbook("data/info.xlsx")
    ws = wb.active

    '''
    for i in imagePaths:
        #name = i.strip("/dataset").strip(".jpg")
        name = i[8:-4]
        image = str(i)+"_image"
        vars()[image] = face_recognition.load_image_file(i)
        encoding = str(i)+"_face_encoding"
        vars()[encoding] = face_recognition.face_encodings(vars()[image])[0]
        known_face_encodings.append(vars()[encoding])
        known_face_names.append(name)
    '''

    for i in imagePaths:
        name = i[9:-4]
        #known_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(i))[0])
        known_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(i),known_face_locations=None, num_jitters=1, model='large')[0])
        known_face_names.append(name)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True


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
                    cv2.rectangle(frame, (left, bottom+35), (right, bottom), (0, 0, 255), cv2.FILLED)
                if (depto != "Desconocido"):
                    cv2.rectangle(frame, (left, bottom+35), (right, bottom), (0, 255, 0), cv2.FILLED)

                cv2.putText(frame,"Depto. "+depto, (left+6, bottom+30), font, 1.0, (255, 255, 255), 1)

                if (int(correo) > 0):
                    cv2.rectangle(frame, (left, bottom+35), (right, bottom+65), (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame, "Correo "+correo, (left+6, bottom+60), font, 1.0, (255, 255, 255), 1)

                if (int(deudas) > 0):
                    cv2.rectangle(frame, (left, bottom+65), (right, bottom+95), (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame, "Deudas "+deudas, (left+6, bottom+90), font, 1.0, (255, 255, 255), 1)

            cv2.putText(frame, name, (left+6, bottom-6), font, 1.0, (255, 255, 255), 1)

        # Muestra imagen resultante
        cv2.imshow('Video', frame)

        # Presionar "q" para salir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera la cámara y destruye las ventanas
    video_capture.release()
    cv2.destroyAllWindows()

#reconocer()
