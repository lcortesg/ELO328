import manager as man
import monitor as mon
import train as train
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import scrolledtext
from ttkthemes import ThemedTk
from passlib.hash import sha256_crypt
import stdiomask
import getpass
import json
import os

chk_state = ""
txt_psw = ""
txt_psw2 = ""
txt_user = ""
txt_dpto = ""
txt_mail = ""
txt_debt = ""
window = ""
#txt = ""
#bar = ""

def write_json(data, filename='data/passwords.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

with open("data/passwords.json", "r") as json_file: 
    data = json.load(json_file) 
    users = data["users"]
    passwords = data["passwords"]

def recog():
    messagebox.showwarning('Inicia monitoreo','Iniciando monitoreo\n Presionar "Q" para salir.')
    mon.reconocer()

def recog_kill():
    mon.reconocer_kill()


def entrenar():
    train.train()
    messagebox.showinfo('Entrenamiento','Entrenamiento Finalizado')

def salir():
    res = messagebox.askokcancel('Salir','¿Está seguro que desea cerrar el programa?')
    if res: exit()


def check(): 
    if check_password(txt_psw.get()): 
        txt_psw.delete(0,"end")
        menu()
    else: messagebox.showwarning('Error','Contraseña Incorrecta')
    #messagebox.showerror('Error','Contraseña Incorrecta')

def check_password(password):
    for i in range(len(users)):
        if sha256_crypt.verify(password, passwords[i]):
            return True
    return False

def change():
    if (txt_psw.get() == "" or txt_psw2.get() == "") : res = messagebox.showwarning('Cambio de contraseña','Campo incompleto')
    else:
        if (txt_psw.get() != txt_psw2.get()): messagebox.showwarning('Cambio de contraseña','Las contraseñas no coinciden\n Inténtelo nuevamente.')

        else:
            res = messagebox.askokcancel('Cambio de contraseña','¿Está seguro que desea cambiar la contraseña?')
            if res:
                if change_password(txt_psw.get()): messagebox.showinfo('Cambio de contraseña','Contraseña cambiada satisfactoriamente')
            else:
                messagebox.showwarning('Cambio de contraseña','Cambio de contraseña cancelado')
    txt_psw.delete(0,"end")
    txt_psw2.delete(0,"end")
    chk_state.set(0)
    activate_check()    

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
    man.mostrar_user()

def agregar():
    if (txt_user.get() == "" or txt_dpto.get() == ""): messagebox.showwarning('Agregar usuario','Campos incompletos')
    elif int(txt_mail.get()) < 0: messagebox.showwarning('Agregar usuario','La cantidad de correo debe ser un número entero mayor o igual a 0')
    elif int(txt_debt.get()) < 0: messagebox.showwarning('Agregar usuario','El monto adeudado debe ser un número entero mayor o igual a 0')

    else: 
        man.agregar_user(txt_user.get().upper(), txt_dpto.get().upper(), txt_mail.get(), txt_debt.get())
        txt_user.delete(0,"end")
        txt_dpto.delete(0,"end")
        txt_mail.delete(0,"end")
        txt_debt.delete(0,"end")

def eliminar():
    if txt_user.get() == "": res = messagebox.showwarning('Eliminar usuario','Campos incompletos')
    else:   
        res = messagebox.askyesno('Eliminar usuario','¿Está seguro que desea eliminar al usuario?')
        if res: 
            man.eliminar_user(txt_user.get().upper(), txt_dpto.get().upper())
            txt_user.delete(0,"end")
            txt_dpto.delete(0,"end")
            txt_mail.delete(0,"end")
            txt_debt.delete(0,"end")

def activate_check():
    if chk_state.get() == 1: 
        txt_psw.config(state='normal')
        txt_psw2.config(state='normal')
    else : 
        txt_psw.delete(0,"end")
        txt_psw.config(state='disabled')
        txt_psw2.delete(0,"end")
        txt_psw2.config(state='disabled')

def log_users():
    f = open("data/log.txt", "r")
    window = ThemedTk(theme="yaru")
    window.title("Log de usuarios")
    #window.geometry('350x350')
    txt = scrolledtext.ScrolledText(window,width=50,height=20, font=("Arial Bold", 20))
    for line in f:
        txt.insert(INSERT,line+"\n")
    f.close()
    txt.grid(column=0,row=0)
    window.mainloop()

def menu():
    global window
    window.destroy()
    #window = ThemedTk(theme="yaru")
    window = Tk()
    #ttk.Style().theme_use('adapta')
    window.title("Let me in")

    for i in range(4):
        window.columnconfigure(i, weight=1, minsize=75)
        window.rowconfigure(i, weight=1, minsize=50)

    tab_control = ttk.Notebook(window)

    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab3 = ttk.Frame(tab_control)

    tab_control.add(tab1, text='Monitoreo')
    tab_control.add(tab2, text='Gestión de Usuarios')
    tab_control.add(tab3, text='Cambio de Contraseña')

    # TAB 1
    persona = Label(tab1, text="Monitoreo de Usuarios", font=("Arial Bold", 20))
    persona.grid(column=1, row=1, padx=5, pady=5)

    btn_mon = Button(tab1, text="Monitorear Cámara", font=("Arial Bold", 20), fg="green", command=recog)
    btn_mon.grid(column=1, row=2, padx=5, pady=5)

    btn_log = Button(tab1, text="Log de Usuarios", font=("Arial Bold", 20), fg="blue", command=log_users)
    btn_log.grid(column=1, row=3, padx=5, pady=5)

    btn_exit = Button(tab1, text="Exit", font=("Arial Bold", 20), fg="red", command=salir)
    btn_exit.grid(column=1, row=4, padx=5, pady=5)

    #global bar
    #bar = ttk.Progressbar(window, orient = HORIZONTAL, length = 100)
    #bar['value'] = 70
    #bar.grid(column=2, row=4)

    #btn_closemon = Button(window, text="Cerrar monitor", command=recog_kill)
    #btn_closemon.grid(column=1, row=2)

    #btn_usr = Button(tab1, text="Gestionar Usuarios", command=usuarios)
    #btn_usr.grid(column=1, row=3)

    # TAB 2


    persona = Label(tab2, text="Gestión de Usuarios", font=("Arial Bold", 20))
    persona.grid(column=2, row=0, padx=5, pady=5)

    persona = Label(tab2, text="Usuario:", font=("Arial Bold", 20))
    persona.grid(column=1, row=1, padx=5, pady=5)

    departamento = Label(tab2, text="Depto.:", font=("Arial Bold", 20))
    departamento.grid(column=1, row=2, padx=5, pady=5)

    correo = Label(tab2, text="Correo:", font=("Arial Bold", 20))
    correo.grid(column=1, row=3, padx=5, pady=5)

    deudas = Label(tab2, text="Deudas:", font=("Arial Bold", 20))
    deudas.grid(column=1, row=4, padx=5, pady=5)

    #global txt
    global txt_user
    global txt_dpto
    global txt_mail
    global txt_debt
    txt_user = " "
    txt_dpto = " "

    txt_user = Entry(tab2, width=15, font=("Arial Bold", 20))
    txt_user.grid(column=2, row=1, padx=5, pady=5)

    txt_dpto = Entry(tab2, width=15, font=("Arial Bold", 20))
    txt_dpto.grid(column=2, row=2, padx=5, pady=5)

    txt_mail = Entry(tab2, width=15, font=("Arial Bold", 20))
    txt_mail.grid(column=2, row=3, padx=5, pady=5)
    #txt_mail.insert(END, '0')

    txt_debt = Entry(tab2, width=15, font=("Arial Bold", 20))
    txt_debt.grid(column=2, row=4, padx=5, pady=5)
    #txt_debt.insert(END, '0')

    btn_trn = Button(tab2, text="Entrenar", font=("Arial Bold", 20), command=entrenar)
    btn_trn.grid(column=3, row=0, padx=5, pady=5)

    btn_add = Button(tab2, text="Agregar", font=("Arial Bold", 20), fg="green", command=agregar)
    btn_add.grid(column=3, row=1, padx=5, pady=5)

    btn_del = Button(tab2, text="Eliminar", font=("Arial Bold", 20), fg="red", command=eliminar)
    btn_del.grid(column=3, row=2, padx=5, pady=5)

    btn_show = Button(tab2, text="Mostrar", font=("Arial Bold", 20), fg="blue", command=mostrar)
    btn_show.grid(column=3, row=3, padx=5, pady=5)

    btn_exit2 = Button(tab2, text="Exit", font=("Arial Bold", 20), fg="red", command=salir)
    btn_exit2.grid(column=3, row=4, padx=5, pady=5)

    txt_user.focus()

    # TAB 3
    global txt_psw
    global txt_psw2
    global chk_state

    ps = Label(tab3, text="Cambio de credenciales", font=("Arial Bold", 20))
    ps.grid(column=1, row=1, padx=5, pady=5)
    psw = Label(tab3, text="Ingrese contraseña:", font=("Arial Bold", 20))
    psw.grid(column=1, row=2, padx=5, pady=5)
    psw2 = Label(tab3, text="Reingrese contraseña:", font=("Arial Bold", 20))
    psw2.grid(column=1, row=3, padx=5, pady=5)

    txt_psw = Entry(tab3, width=15, font=("Arial Bold", 20), state='disabled')
    txt_psw.config(show="*")
    txt_psw.grid(column=2, row=2, padx=5, pady=5)

    txt_psw2 = Entry(tab3, width=15, font=("Arial Bold", 20), state='disabled')
    txt_psw2.config(show="*")
    txt_psw2.grid(column=2, row=3, padx=5, pady=5)

    chk_state = IntVar()
    chk_state.set(0)
    chk = Checkbutton(tab3, text='¿Nueva Contraseña?', font=("Arial Bold", 20), fg="red", variable=chk_state, command=activate_check)
    chk.grid(column=2, row=1, padx=5, pady=5)

    btn_cge = Button(tab3, text ="Cambiar", font=("Arial Bold", 20), fg="green",  command=change)
    btn_cge.grid(column=2, row=4, padx=5, pady=5)

    btn_exit3 = Button(tab3, text="Exit", font=("Arial Bold", 20), fg="red", command=salir)
    btn_exit3.grid(column=1, row=4, padx=5, pady=5)

    tab_control.pack(expand=1, fill='both')
    window.mainloop()


'''
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

    btn_exit = Button(window, text="Exit", bg="red", fg="red", command=salir)
    btn_exit.grid(column=1, row=6)

    txt_user.focus()
    window.mainloop()
'''

'''
def menu_old():window = Tk()
    window.geometry('350x200')
    window.title("Let me in - Menú")
 
    #psw = Label(window, text="Nueva Contraseña: ")
    #psw.grid(column=0, row=1)
    global txt_psw
    global chk_state

    txt_psw = Entry(window, width=15, state='disabled')
    txt_psw.config(show="*")
    txt_psw.grid(column=1, row=1)

    

    chk_state = IntVar()
    chk_state.set(False)
    chk = Checkbutton(window, text='Nueva Contraseña', variable=chk_state, command=activate_check)
    chk.grid(column=0, row=1)

    #txt_psw.focus()
    btn_gest = Button(window, text ="Cambiar", bg="red", fg="blue",  command=change)
    btn_man.grid(column=2, row=1)

    btn_mon = Button(window, text="Monitorear Cámara", command=recog)
    btn_mon.grid(column=1, row=2)

    #btn_closemon = Button(window, text="Cerrar monitor", command=recog_kill)
    #btn_closemon.grid(column=1, row=2)

    btn_usr = Button(window, text="Gestionar Usuarios", command=usuarios)
    btn_usr.grid(column=1, row=3)

    btn_trn = Button(window, text="Entrenar Modelo", command=entrenar)
    btn_trn.grid(column=1, row=4)

    btn_exit = Button(window, text="Exit", bg="red", fg="red", command=salir)
    btn_exit.grid(column=1, row=5)
    window.mainloop()
'''

#def login():
#pyglet.font.add_file("data/OpenSans-Regular.ttf")
window = Tk()
#window = ThemedTk(theme="yaru")
#ttk.Style().theme_use('adapta')
window.title("Let me in - Log In")
#window.geometry('350x200')
#global txt_psw
psw = Label(window, text="Contraseña: ", font=("Arial Bold", 20))
psw.grid(column=0, row=1, padx=5, pady=5)
txt_psw = Entry(window, width=15, font=("Arial Bold", 20))
txt_psw.config(show="*")
txt_psw.grid(column=1, row=1, padx=5, pady=5)
txt_psw.focus()
btn_login = Button(window, text="Log In", font=("Arial Bold", 20), fg="green", command=check)
btn_login.grid(column=2, row=1, padx=5, pady=5)
btn_exit = Button(window, text="Exit", font=("Arial Bold", 20), fg="red", command=salir)
btn_exit.grid(column=1, row=2, padx=5, pady=5)
window.mainloop()
#login()
