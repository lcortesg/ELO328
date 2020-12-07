import gestionar as gest
import monitorear as mon
import train as train
from tkinter import *
from passlib.hash import sha256_crypt
import stdiomask
import getpass
import json
import os

txt_psw = "test"

'''
usr_f = Label(window, text=" ")
psw_f = Label(window, text=" ")
usr_f.grid(column=2, row=0)
psw_f.grid(column=2, row=1)
'''

'''
def clicked():
    usr_f.configure(text="Usuario no encontrado")
    psw_f.configure(text="Contraseña incorrecta")
'''

def comprobar(): 
    check_password(txt_psw.get())

def recog():
    mon.reconocer()

def login():
    window = Tk()
    window.title("Let me in - Log In")
    window.geometry('350x200')

    psw = Label(window, text="Contraseña: ")
    psw.grid(column=0, row=1)

    global txt_psw

    print(txt_psw)
    txt_psw = Entry(window,width=10)
    txt_psw.grid(column=1, row=1)

    btn_gest = Button(window, text="Log In", command=comprobar)
    btn_gest.grid(column=3, row=1)
    
    window.mainloop()

def entrenar():
    train.train()
    trn = Label(window, text="Entrenamiento finalizado")
    trn.grid(column=2, row=3)

def administrador():
    admin.administrar_check()

def salir():
    exit()


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
btn = Button(window, text="Click Me", command=clicked)
btn.grid(column=1, row=3)
'''

def gui():
    window = Tk()
    window.title("Let me in - menu")
    window.geometry('350x200')

    btn_mon = Button(window, text="Monitorear", command=recog)
    btn_mon.grid(column=1, row=1)

    btn_closemon = Button(window, text="Cerrar monitor", command=recog)
    btn_closemon.grid(column=2, row=1)

    btn_usr = Button(window, text="Usuarios", command=usuarios)
    btn_usr.grid(column=1, row=2)

    btn_trn = Button(window, text="Entrenar", command=entrenar)
    btn_trn.grid(column=1, row=3)

    btn_adm = Button(window, text="Administrador", command=administrador)
    btn_adm.grid(column=1, row=4)

    btn_exit = Button(window, text="Salir", command=salir)
    btn_exit.grid(column=1, row=5)

    window.mainloop()

login()
