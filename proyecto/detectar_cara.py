import os
import cv2
import numpy as np
import argparse
from functions import *
 
# Argumentos del programa.
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imagen", required=False, help="Ruta de la imagen")
args = vars(ap.parse_args())

