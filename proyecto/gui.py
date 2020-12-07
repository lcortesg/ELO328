import gestionar as gest
import monitorear as mon
import train as train
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import scrolledtext
from passlib.hash import sha256_crypt
import stdiomask
import getpass
import json
import os

txt_psw = ""
txt_user = ""
txt_dpto = ""
txt_mail = ""
txt_debt = ""
f = ""

def write_json(data, filename='data/passwords.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

with open("data/passwords.json", "r") as json_file: 
    data = json.load(json_file) 
    users = data["users"]
    passwords = data["passwords"]

class DestroyTest():
    def __init__(self, top):
        self.top=top
        self.top.geometry("+10+10")

        self.frame=Frame(self.top)
        self.frame.grid()

        test_label=Label(self.frame, text="Label")
        test_label.grid(row=1, column=0)

        destroy_button=Button(self.frame, text="Destroy Frame", \
                                 command=self.destroy)
        destroy_button.grid(row=10, column=0)

        exit_button=Button(self.top, text="Exit", command=top.quit)
        exit_button.grid(row=10, column=0)
    def destroy(self):
        self.frame.destroy()
        self.new_toplevel=Toplevel(self.top, takefocus=True)
        self.new_toplevel.geometry("+50+50")
        self.new_toplevel.grid()

        lbl=Label(self.new_toplevel, text="New Toplevel")
        lbl.grid()

'''
def login():
    window = Tk()
    window.title("Let me in - Log In")
    window.geometry('350x200')
    psw = Label(window, text="Contraseña: ")
    psw.grid(column=0, row=1)
    global txt_psw
    #widget = Entry(window, show="*", width=15)
    txt_psw = Entry(window,width=15)
    txt_psw.config(show="*")
    txt_psw.grid(column=1, row=1)
    txt_psw.focus()
    btn_gest = Button(window, text="Log In", command=check)
    btn_gest.grid(column=3, row=1)

    btn_exit = Button(window, text="Salir", command=salir)
    btn_exit.grid(column=1, row=2)
    window.mainloop()
'''

def check(): 
    if check_password(txt_psw.get()): 
        txt_psw.delete(0,"end")
        menu()
    else: messagebox.showwarning('Error','Contraseña Incorrecta')
    #messagebox.showerror('Error','Contraseña Incorrecta')

def change():
    res = messagebox.askokcancel('Cambio de contraseña','¿Está seguro que desea cambiar la contraseña?')
    if res:
        if change_password(txt_psw.get()):
            messagebox.showinfo('Cambio de contraseña','Contraseña cambiada satisfactoriamente')
            txt_psw.delete(0,"end")
    else:
        txt_psw.delete(0,"end")
        messagebox.showwarning('Cambio de contraseña','Cambio de contraseña cancelado')

def recog():
    messagebox.showwarning('Inicia monitoreo','Presionar "Q" para salir.')
    mon.reconocer()

def recog_kill():
    mon.reconocer_kill()


def entrenar():
    train.train()
    messagebox.showinfo('Entrenamiento','Entrenamiento Finalizado')

def salir():
    res = messagebox.askokcancel('Salir','¿Está seguro que desea cerrar el programa?')
    if res: exit()

def check_password(password):
    for i in range(len(users)):
        if sha256_crypt.verify(password, passwords[i]):
            return True
    return False

def change_password(password):
    hash = sha256_crypt.hash(password)
    for i in range(len(users)):
        if users[i] == "user":
            users.pop(i)
            passwords.pop(i)
            users.append("user")
            passwords.append(hash)
            write_json(data)
            return True

def mostrar():
    gest.mostrar_user()

def agregar():
    if txt_user.get() == "": res = messagebox.showwarning('Agregar usuario','Campos incompletos')
    else: gest.agregar_user(txt_user.get().upper(), txt_dpto.get().upper(), txt_mail.get(), txt_debt.get())

def eliminar():
    if txt_user.get() == "": res = messagebox.showwarning('Eliminar usuario','Campos incompletos')
    else:   
        res = messagebox.askyesno('Eliminar usuario','¿Está seguro que desea eliminar al usuario?')
        if res: gest.eliminar_user(txt_user.get().upper(), txt_dpto.get().upper())


def usuarios():
    window = Tk()
    window.geometry('350x200')
    window.title("Let me in - Gestión de Usuarios")

    btn_add = Button(window, text="Agregar", command=agregar)
    btn_add.grid(column=0, row=1)

    btn_del = Button(window, text="Eliminar", command=eliminar)
    btn_del.grid(column=1, row=1)

    btn_show = Button(window, text="Mostrar", command=mostrar)
    btn_show.grid(column=2, row=1)

    persona = Label(window, text="Usuario: ")
    persona.grid(column=0, row=2)

    departamento = Label(window, text="Departamento: ")
    departamento.grid(column=0, row=3)

    correo = Label(window, text="Correo: ")
    correo.grid(column=0, row=4)

    deudas = Label(window, text="Deudas: ")
    deudas.grid(column=0, row=5)


    global txt_user
    global txt_dpto
    global txt_mail
    global txt_debt
    txt_user = " "
    txt_dpto = " "

    txt_user = Entry(window, width=15)
    txt_user.grid(column=1, row=2)

    txt_dpto = Entry(window, width=15)
    txt_dpto.grid(column=1, row=3)

    txt_mail = Entry(window, width=15)
    txt_mail.grid(column=1, row=4)

    txt_debt = Entry(window, width=15)
    txt_debt.grid(column=1, row=5)

    btn_exit = Button(window, text="Exit", command=salir)
    btn_exit.grid(column=1, row=6)

    txt_user.focus()
    window.mainloop()

def menu():
    f.destroy()
    window.title("Let me in - Menú")

    psw = Label(window, text="Nueva Contraseña: ")
    psw.grid(column=0, row=1)
    global txt_psw
    txt_psw = Entry(window,width=15)
    txt_psw.config(show="*")
    txt_psw.grid(column=1, row=1)
    #txt_psw.focus()
    btn_gest = Button(window, text="Cambiar", command=change)
    btn_gest.grid(column=2, row=1)

    btn_mon = Button(window, text="Monitorear", command=recog)
    btn_mon.grid(column=1, row=2)

    #btn_closemon = Button(window, text="Cerrar monitor", command=recog_kill)
    #btn_closemon.grid(column=1, row=2)

    btn_usr = Button(window, text="Usuarios", command=usuarios)
    btn_usr.grid(column=1, row=3)

    btn_trn = Button(window, text="Entrenar", command=entrenar)
    btn_trn.grid(column=1, row=4)

    btn_exit = Button(window, text="Exit", command=salir)
    btn_exit.grid(column=1, row=5)
    window.mainloop()
#login()

window = Tk()
f = Frame(window)
window.title("Let me in - Log In")
window.geometry('350x200')
psw = Label(window, text="Contraseña: ")
psw.grid(column=0, row=1)
#global txt_psw
#widget = Entry(window, show="*", width=15)
txt_psw = Entry(window,width=15)
txt_psw.config(show="*")
txt_psw.grid(column=1, row=1)
txt_psw.focus()
btn_gest = Button(window, text="Log In", command=check)
btn_gest.grid(column=2, row=1)

btn_exit = Button(window, text="Exit", command=salir)
btn_exit.grid(column=1, row=2)
window.mainloop()


