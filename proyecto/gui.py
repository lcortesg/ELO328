import administrar as admin
import gestionar as gest
import monitor as mon
import train as train
from tkinter import *

window = Tk()

window.title("Welcome to LikeGeeks app")

window.geometry('350x200')

lbl = Label(window, text="Hello")

lbl.grid(column=0, row=0)

btn = Button(window, text="Click Me")

btn.grid(column=1, row=0)

window.mainloop()




'''

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
'''