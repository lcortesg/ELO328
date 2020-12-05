import administrar as admin
import gestionar as gest
import monitorear as mon
import train as train
import tkinter as tk

def main():
    while True:
        modo = input("(U) Gestionar Usuarios. (A) Gestionar Administradores. (M) Monitorear/Reconocer. (T) Entrenar Modelo. (Q) Salir. : ")
        if (modo == "Q" or modo == "q"):
            print ("HASTA PRONTO")
            exit()
        if (modo == "U" or modo == "u"):
            gest.gestion_check()
        if (modo == "A" or modo == "a"):
            admin.administrar_check()
        if (modo == "M" or modo == "m"):
            mon.reconocer()
        if (modo == "T" or modo == "t"):
            train.train()
main()