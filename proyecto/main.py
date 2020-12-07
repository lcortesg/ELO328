import gestionar as gest
import monitorear as mon
import train as train
from tkinter import *
from passlib.hash import sha256_crypt
import stdiomask
import getpass
import json
import os

# LA CONTRASEÑA MAESTRA ES master

def write_json(data, filename='data/passwords.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

with open("data/passwords.json", "r") as json_file: 
    data = json.load(json_file) 
    users = data["users"]
    passwords = data["passwords"]

def check_password(password):
    for i in range(len(users)):
        if sha256_crypt.verify(password, passwords[i]):
            print ("BIENVENIDO")
            main()
    print ("CONTRASEÑA INCORRECTA")

def change_password(password):
    hash = sha256_crypt.hash(password)
    for i in range(len(users)):
        if users[i] == "user":
            users.pop(i)
            passwords.pop(i)
            users.append("user")
            passwords.append(hash)
            write_json(data)
            print("Contraseña modificada con éxito")
            main()

def main():
    while True:
        modo = input("(M) Monitorear. (U) Gestionar Usuarios. (C) Cambiar Contraseña. (T) Entrenar Modelo. (Q) Salir. : ")

        if (modo == "Q" or modo == "q"):
            print ("HASTA PRONTO")
            exit()

        if (modo == "U" or modo == "u"):
            gest.gestion()

        if (modo == "C" or modo == "c"):
            password = stdiomask.getpass("NEW PASSWORD: ")
            change_password(password)

        if (modo == "M" or modo == "m"):
            mon.reconocer()

        if (modo == "T" or modo == "t"):
            train.train()
'''
while True:
    password = stdiomask.getpass("PASSWORD: ")
    check_password(password)
'''