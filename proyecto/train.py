from imutils import paths
import face_recognition
import numpy as np
import pickle
import cv2
import os

def train():
    print("ENTRENANDO MODELO")
    all_face_encodings = {}
    imagePaths = list(paths.list_images('data/img'))

    for i in imagePaths:
        name = i[9:-4]
        all_face_encodings[name] = face_recognition.face_encodings(face_recognition.load_image_file(i),known_face_locations=None, num_jitters=1, model='large')[0]

    with open('data/encodings.dat', 'wb') as f:
        pickle.dump(all_face_encodings, f)
    print("ENTRENAMIENTO FINALIZADO")
