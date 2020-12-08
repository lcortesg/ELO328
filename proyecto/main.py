'''
@File    :   main.py
@Date    :   2020/12/07
@Author  :   Lucas Cortés Gutiérrez.
@Version :   2.0
@Contact :   lucas.cortes.14@sansano.usm.cl"
@Desc    :   Interfaz gráfica del sistema de reconocimineto de personas "Let Me In"
'''

from passlib.hash import sha256_crypt
from tkinter import scrolledtext
from tkinter import messagebox
from ttkthemes import ThemedTk
from tkinter import ttk
from tkinter import *
import manager as man
import monitor as mon
import stdiomask
#import getpass
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

# Función que escribe en el archivo JSON la contraseña de administración.
def write_json(data, filename='data/passwords.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

# Fucnión que extrae la contraseña del administración del archivo JSON.
with open("data/passwords.json", "r") as json_file: 
    data = json.load(json_file) 
    users = data["users"]
    passwords = data["passwords"]

# Función encargada de llamar al módulo de monitoreo.
def monitorear():
    messagebox.showwarning('Inicia monitoreo','Iniciando monitoreo\n Presionar "ESC" para salir.')
    mon.monitor()

# Función que detiene el módulo de monitoreo.
def monitorear_kill():
    mon.monitor_kill()

# Función encargada de llamar al módulo de entrenamiento.
def entrenar():
    man.train()
    messagebox.showinfo('Entrenamiento','Entrenamiento Finalizado')

# Función que detiene la ejecución del programa.
def salir():
    res = messagebox.askokcancel('Salir','¿Está seguro que desea cerrar el programa?')
    if res: exit()

# Función que llama al menu principal una vez la contraseña fue verificada.
def check(event=None): 
    if check_password(txt_psw.get()): 
        txt_psw.delete(0,"end")
        menu()
    else: messagebox.showwarning('Error','Contraseña Incorrecta')

# Función que verifica que la contraseña ingresada sea la corecta.
def check_password(password):
    for i in range(len(users)):
        if sha256_crypt.verify(password, passwords[i]):
            return True
    return False

# Función que se encarga de comparar los campos de cambio de contraseña.
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

# Función encargada de realizar el cambio de contraseña.
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

# Función encargada de imprimir una lista de los usuarios registrados.
def mostrar():
    man.show_user()

# Función encargada de validar el tipo de dato en la variable "txt_mail".
def check_mail():
    try:
        mail_check = True if type(int(txt_mail.get())) == int else False

        if mail_check: check_debt()
    except:
        mail_check = False
        messagebox.showwarning('Agregar usuario','La cantidad de correo debe ser un número')
        txt_mail.delete(0,"end")

# Función encargada de validar el tipo de dato en la variable "txt_debt".
def check_debt():
    try:
        debt_check = True if type(int(txt_debt.get())) == int else False
        if debt_check: agregar()

    except:
        debt_check = False
        messagebox.showwarning('Agregar usuario','El monto adeudado debe ser un número')
        txt_debt.delete(0,"end")

# Función encargada de agregar un nuevo usuario a la base de datos.
def agregar():
    if (int(txt_mail.get()) < 0 or int(txt_debt.get()) < 0):
        if int(txt_mail.get()) < 0: 
            messagebox.showwarning('Agregar usuario','La cantidad de correo debe ser mayor o igual a 0')
            txt_mail.delete(0,"end")
        elif int(txt_debt.get()) < 0: 
            messagebox.showwarning('Agregar usuario','El monto adeudado debe ser mayor o igual a 0')
            txt_debt.delete(0,"end")
    else: 
        man.add_user(txt_user.get().upper(), txt_dpto.get().upper(), txt_mail.get(), txt_debt.get())
        txt_user.delete(0,"end")
        txt_dpto.delete(0,"end")
        txt_mail.delete(0,"end")
        txt_debt.delete(0,"end")
        txt_mail.insert(END, '0')
        txt_debt.insert(END, '0')

# Función encargada de eliminar a un usuario desde la base de datos.
def eliminar():
    if txt_user.get() == "": res = messagebox.showwarning('Eliminar usuario','Campos incompletos')
    else:   
        res = messagebox.askyesno('Eliminar usuario','¿Está seguro que desea eliminar al usuario?')
        if res: 
            man.delete_user(txt_user.get().upper(), txt_dpto.get().upper())
            txt_user.delete(0,"end")
            txt_dpto.delete(0,"end")
            txt_mail.delete(0,"end")
            txt_debt.delete(0,"end")

# Función encargada de imprimir un log de los usuarios detectados.
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

# Función encargada de revisar el estado de un check en la pestaña de cambio de contraseña.
def activate_check():
    if chk_state.get() == 1: 
        txt_psw.config(state='normal')
        txt_psw2.config(state='normal')
    else : 
        txt_psw.delete(0,"end")
        txt_psw.config(state='disabled')
        txt_psw2.delete(0,"end")
        txt_psw2.config(state='disabled')

# Función encargada de vaciar los valores por defecto en los campos "txt_mail" y "txt_debt".
def removeValue(event):
    event.widget.delete(0, 'end')

# Función que construye el menu principal y sus pestañas correspondientes.
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

    ########## TAB 1 ##########
    persona = Label(tab1, text="Monitoreo de Usuarios", font=("Arial Bold", 20))
    persona.grid(column=1, row=1, padx=5, pady=5)

    btn_mon = Button(tab1, text="Monitorear Cámara", font=("Arial Bold", 20), fg="green", command=monitorear)
    btn_mon.grid(column=1, row=2, padx=5, pady=5)

    btn_log = Button(tab1, text="Log de Usuarios", font=("Arial Bold", 20), fg="blue", command=log_users)
    btn_log.grid(column=1, row=3, padx=5, pady=5)

    btn_exit = Button(tab1, text="Exit", font=("Arial Bold", 20), fg="red", command=salir)
    btn_exit.grid(column=1, row=4, padx=5, pady=5)

    #global bar
    #bar = ttk.Progressbar(window, orient = HORIZONTAL, length = 100)
    #bar['value'] = 70
    #bar.grid(column=2, row=4)

    #btn_closemon = Button(window, text="Cerrar monitor", command=monitorear_kill)
    #btn_closemon.grid(column=1, row=2)

    #btn_usr = Button(tab1, text="Gestionar Usuarios", command=usuarios)
    #btn_usr.grid(column=1, row=3)

    ########## TAB 2 ##########
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

    txt_mail = IntVar()
    txt_mail = Entry(tab2, width=15, font=("Arial Bold", 20))
    txt_mail.grid(column=2, row=3, padx=5, pady=5)
    txt_mail.insert(END, '0')
    txt_mail.bind("<Button-1>", removeValue)

    txt_debt = IntVar()
    txt_debt = Entry(tab2, width=15, font=("Arial Bold", 20))
    txt_debt.grid(column=2, row=4, padx=5, pady=5)
    txt_debt.insert(END, '0')
    txt_debt.bind("<Button-1>", removeValue)

    btn_trn = Button(tab2, text="Entrenar", font=("Arial Bold", 20), command=entrenar)
    btn_trn.grid(column=3, row=0, padx=5, pady=5)

    btn_add = Button(tab2, text="Agregar", font=("Arial Bold", 20), fg="green", command=check_mail)
    btn_add.grid(column=3, row=1, padx=5, pady=5)

    btn_del = Button(tab2, text="Eliminar", font=("Arial Bold", 20), fg="red", command=eliminar)
    btn_del.grid(column=3, row=2, padx=5, pady=5)

    btn_show = Button(tab2, text="Mostrar", font=("Arial Bold", 20), fg="blue", command=mostrar)
    btn_show.grid(column=3, row=3, padx=5, pady=5)

    btn_exit2 = Button(tab2, text="Exit", font=("Arial Bold", 20), fg="red", command=salir)
    btn_exit2.grid(column=3, row=4, padx=5, pady=5)

    txt_user.focus()

    ########## TAB 3 ##########
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


#def login():
window = Tk()
#window = ThemedTk(theme="yaru")
#ttk.Style().theme_use('adapta')
window.title("Let me in - Log In")
window.bind("<Return>", check)

#window.geometry('350x200')
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

