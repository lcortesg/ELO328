'''
@File    :   train.py
@Date    :   2020/12/07
@Author  :   Lucas Cortés Gutierrez.
@Version :   2.0
@Contact :   lucas.cortes.14@sansano.usm.cl"
@Desc    :   Módulo de entrenamiento del sistema de reconocimineto de personas "Let Me In"
'''

from imutils import paths
import face_recognition
import numpy as np
import pickle
import cv2
import os

verbose = False


def train():
    if verbose: print("ENTRENANDO MODELO")
    all_face_encodings = {}
    imagePaths = list(paths.list_images('data/dataset'))

    for i in imagePaths:
        name = i[13:-4]
        all_face_encodings[name] = face_recognition.face_encodings(face_recognition.load_image_file(i),known_face_locations=None, num_jitters=10, model='large')[0]

    with open('data/model.dat', 'wb') as model:
        pickle.dump(all_face_encodings, model)
    if verbose: print("ENTRENAMIENTO FINALIZADO")
