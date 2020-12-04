from passlib.hash import sha256_crypt
import stdiomask
import getpass
import json
import os

def write_json(data, filename='passwords.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 
with open('passwords.json') as json_file: 
    data = json.load(json_file) 
    temp_users = data['users']
    temp_passwords = data['passwords']

while True:
    user = input("Usuario: ")
    if user in temp_users:
        print("Usuario ya se encuentra registrado!")
    else:
        break

while True:
    password = stdiomask.getpass("Contraseña: ")
    password2 = stdiomask.getpass("Reingrese Contraseña: ")
    #password = input("Contraseña: ")
    #password2 = input("Reingrese Contraseña: ")
    if password == password2:
        break
    else:
        print("Las contraseñas no coinciden")

hash = sha256_crypt.hash(password)

with open('passwords.json') as json_file: 
    data = json.load(json_file) 

    temp_users = data['users']
    temp_passwords = data['passwords']

    temp_users.append(user)
    temp_passwords.append(hash)

write_json(data)
print("Usuario ingresado con éxito")



