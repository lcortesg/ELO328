import administrar as admin
import gestionar as gest
import monitorear as mon
import train as train
from tkinter import *



txt_usr = " "
txt_psw = " "
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

def enviar_u():
    gest.gestion_gui(txt_usr, txt_psw)

def recog():
    mon.reconocer()

def usuarios():
    window = Tk()
    window.title("Let me in - Gestion de usuarios")
    window.geometry('350x200')

    usr = Label(window, text="Usuario")
    usr.grid(column=0, row=0)

    psw = Label(window, text="Contraseña")
    psw.grid(column=0, row=1)

    txt_usr = Entry(window,width=10)
    txt_usr.grid(column=1, row=0)
    txt_usr.focus()

    txt_psw = Entry(window,width=10)
    txt_psw.grid(column=1, row=1)

    btn_gest = Button(window, text="Log In", command=enviar_u)
    btn_gest.grid(column=2, row=3)

    window.mainloop()
    
    #gest.gestion_check()

def entrenar():
    train.train()
    trn = Label(window, text="Entrenamiento finalizado")
    trn.grid(column=2, row=3)

def administrador():
    admin.administrar_check()

def salir():
    exit()

'''
btn = Button(window, text="Click Me", command=clicked)
btn.grid(column=1, row=3)
'''

def main():
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

main()
