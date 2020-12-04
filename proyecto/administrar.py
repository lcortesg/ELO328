from passlib.hash import sha256_crypt
import stdiomask
import getpass
import json
import os

master = "$5$rounds=535000$EfTvpCs/.4yCI1NE$QHJlaaQF08OXjmlnHJzoAWr1KnBl6F7lZBEYZofN2i4"

def write_json(data, filename='data/passwords.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

def mostrar_admin():
    with open('data/passwords.json') as json_file: 
        data = json.load(json_file) 
        users = data['users']
        passwords = data['passwords']
    print("User - Password (SHA256)")
    for u in range(len(users)):
        print(users[u], " - ", passwords[u])

def agregar_admin():
    with open('data/passwords.json') as json_file: 
        data = json.load(json_file) 
        users = data['users']
        passwords = data['passwords']

    while True:
        user = input("Usuario: ")
        if user in users:
            print("Usuario ya se encuentra registrado!")
            administrar()
        else:
            break

    while True:
        password = stdiomask.getpass("Contraseña: ")
        password2 = stdiomask.getpass("Reingrese Contraseña: ")
        if password == password2:
            break
        else:
            print("Las contraseñas no coinciden")

    hash = sha256_crypt.hash(password)
    users.append(user)
    passwords.append(hash)
    write_json(data)
    print("Usuario ingresado con éxito")


def eliminar_admin():
    with open('data/passwords.json') as json_file: 
        data = json.load(json_file) 
        users = data['users']
        passwords = data['passwords']

    user = input("Usuario: ")
    if user not in users:
        print("Usuario no se encuentra registrado!")
        administrar()

    while True:
        password = stdiomask.getpass("Contraseña: ")
        for u in range(len(users)):
            if users[u] == user:
                if sha256_crypt.verify(password, passwords[u]):
                    hash = sha256_crypt.hash(password)
                    users.pop(u)
                    passwords.pop(u)
                    write_json(data)
                    print("Usuario eliminado con éxito")
                else:
                    print ("CONTRASEÑA INCORRECTA")
                administrar()

def cambiar_admin():
    with open('data/passwords.json') as json_file: 
        data = json.load(json_file) 
        users = data['users']
        passwords = data['passwords']
    while True:
        user = input("Usuario: ")
        if user in users:
            break
        else:
            print("Usuario no se encuentra registrado!")
            administrar()

    while True:
        password_old = stdiomask.getpass("Ingrese contraseña actual: ")
        for u in range(len(users)):
            if users[u] == user:
                if sha256_crypt.verify(password_old, passwords[u]):
                    while True:
                        password = stdiomask.getpass("Ingrese nueva contraseña: ")
                        password2 = stdiomask.getpass("Reingrese nueva contraseña: ")
                        if password == password2:
                            break
                        else:
                            print("Las contraseñas no coinciden")
                    hash = sha256_crypt.hash(password)
                    users.pop(u)
                    passwords.pop(u)
                    users.append(user)
                    passwords.append(hash)
                    write_json(data)
                    print("Contraseña modificada con éxito")
                else:
                    print ("CONTRASEÑA INCORRECTA")
                administrar()

def administrar():
    while True:
        modo = input("(A) Agregar Usuario. (E) Eliminar Usuario. (M) Mostrar Usuarios. (C) Cambiar Contraseña. (Q) Salir. : ")
        if (modo == "Q" or modo == "q"):
            print ("HASTA PRONTO")
            exit()
        if (modo == "E" or modo == "e"):
            eliminar_admin()
        if (modo == "A" or modo == "a"):
            agregar_admin()
        if (modo == "M" or modo == "m"):
            mostrar_admin()
        if (modo == "C" or modo == "c"):
            cambiar_admin()

def administrar_check():
    while True:
        login = stdiomask.getpass("INGRESE CONTRASEÑA MAESTRA: ")
        
        if sha256_crypt.verify(login, master):
            print ("BIENVENIDO")
            administrar()
        else:
            print ("CONTRASEÑA INCORRECTA")
            administrar_check()
#administrar_check()




