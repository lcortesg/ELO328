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
from contextlib import suppress
from tkinter import messagebox
from ttkthemes import ThemedTk
from tkinter import ttk
from tkinter import *
import manager as man
import monitor as mon
from beepy import *
import stdiomask
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
mail_check = False
debt_check = False
data_check = False
sounds = True
talk = False

'''
print('\a')
print('\007')
os.system("say beep")
'''


# Se extrae la contraseña del administración del archivo JSON.
with open("data/passwords.json", "r") as json_file: 
    data = json.load(json_file) 
    users = data["users"]
    passwords = data["passwords"]

# Función que escribe en el archivo JSON la contraseña de administración.
def write_json(data, filename='data/passwords.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

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
    print('\007')
    res = messagebox.askokcancel('Salir','¿Está seguro que desea cerrar el programa?')
    if res: 
        exit()

# Fucnión de cierre de sesión.
def logout(pelota=False):
    if not pelota:
        print('\007')
        pelota = messagebox.askokcancel('Salir','¿Está seguro que desea cerrar sesión?')
    if pelota:
        global window_menu
        window_menu.destroy()
        with suppress(Exception):
            global window_show
            window_show.destroy()
        with suppress(Exception):
            global window_log
            window_log.destroy()
        login()

# Función de verificación de contraseña.
def check_password(event=None):
    for i in range(len(users)):
        if sha256_crypt.verify(txt_psw.get(), passwords[i]):
            if sounds: 
                beep(sound=1)
            menu()
    txt_psw.delete(0,"end")
    print('\007')
    messagebox.showwarning('Error','Contraseña Incorrecta')
    txt_psw.focus()

# Función encargada de realizar el cambio de contraseña.
def change_password():
    if (txt_psw.get() == "" or txt_psw2.get() == "") : 
        res = messagebox.showwarning('Cambio de contraseña','Campo incompleto')
    else:
        if (txt_psw.get() != txt_psw2.get()): 
            print('\007')
            messagebox.showwarning('Cambio de contraseña','Las contraseñas no coinciden\n Inténtelo nuevamente.')
        else:
            res = messagebox.askokcancel('Cambio de contraseña','¿Está seguro que desea cambiar la contraseña?')
            if res:
                hash = sha256_crypt.hash(txt_psw.get())
                for i in range(len(users)):
                    if users[i] == "user":
                        users.pop(i)
                        passwords.pop(i)
                        users.append("user")
                        passwords.append(hash)
                        write_json(data)
                        if sounds: 
                            beep(sound=1)
                        messagebox.showinfo('Cambio de contraseña','Contraseña cambiada satisfactoriamente')
                        logout(pelota=True)
            else:
                messagebox.showwarning('Cambio de contraseña','Cambio de contraseña cancelado')
    txt_psw.delete(0,"end")
    txt_psw2.delete(0,"end")
    chk_state.set(0)
    activate_check()    

# Función encargada de imprimir una lista de los usuarios registrados.
def mostrar():
    global window_show
    window_show = Tk()
    window_show.title("Lista de usuarios")
    txt = scrolledtext.ScrolledText(window_show,width=50,height=20, font=("Arial Bold", 20))
    man.show_user(txt)
    txt.grid(column=0,row=0)
    window_show.mainloop()

# Función encargada de validar el tipo de dato en las entradas de correo y deudas y de agregar al usuario a la base de datos.
def agregar():
    mail_check = False
    debt_check = False
    data_check = False
    with suppress(Exception): 
        mail_check = True if type(int(txt_mail.get().strip())) == int else False
    with suppress(Exception): 
        debt_check = True if type(int(txt_debt.get().strip())) == int else False

    if txt_user.get().strip() == "" or txt_dpto.get().strip() == "": 
        print('\007')
        messagebox.showwarning('Agregar usuario','Campos incompletos')
        return False

    if not mail_check:
        print('\007')
        messagebox.showwarning('Agregar usuario','La cantidad de correo debe ser un número')
        txt_mail.delete(0,"end")
        txt_mail.insert(END, '0')

    if not debt_check:
        print('\007')
        messagebox.showwarning('Agregar usuario','El monto adeudado debe ser un número')
        txt_debt.delete(0,"end")
        txt_debt.insert(END, '0')

    if (mail_check and int(txt_mail.get()) < 0):
        print('\007')
        messagebox.showwarning('Agregar usuario','La cantidad de correo debe ser mayor o igual a 0')
        txt_mail.delete(0,"end")
        txt_mail.insert(END, '0')

    if (debt_check and int(txt_debt.get()) < 0):
        print('\007')
        messagebox.showwarning('Agregar usuario','El monto adeudado debe ser mayor o igual a 0')
        txt_debt.delete(0,"end")
        txt_debt.insert(END, '0')

    if txt_user.get().strip() != "" and txt_dpto.get().strip() != "": 
        data_check = True

    if (mail_check and debt_check and data_check):
        man.add_user(txt_user.get().strip().upper(), txt_dpto.get().strip().upper(), txt_mail.get().strip(), txt_debt.get().strip())
        txt_user.delete(0,"end")
        txt_dpto.delete(0,"end")
        txt_mail.delete(0,"end")
        txt_debt.delete(0,"end")
        txt_mail.insert(END, '0')
        txt_debt.insert(END, '0')

# Función encargada de eliminar a un usuario desde la base de datos.
def eliminar():
    if txt_user.get().strip() == "" or txt_dpto.get().strip() == "": 
        print('\007')
        messagebox.showwarning('Eliminar usuario','Campos incompletos')
    else:   
        res = messagebox.askyesno('Eliminar usuario','¿Está seguro que desea eliminar al usuario?')
        if res: 
            man.delete_user(txt_user.get().strip().upper(), txt_dpto.get().strip().upper())
            txt_user.delete(0,"end")
            txt_dpto.delete(0,"end")
            txt_mail.delete(0,"end")
            txt_debt.delete(0,"end")
            txt_mail.insert(END, '0')
            txt_debt.insert(END, '0')

# Función encargada de imprimir un log de los usuarios detectados.
def log_users():
    f = open("data/log.txt", "r")
    global window_log
    window_log = Tk()
    window_log.title("Log de usuarios")
    #window.geometry('350x350')
    txt_log = scrolledtext.ScrolledText(window_log,width=50,height=20, font=("Arial Bold", 20))
    txt_log.insert(INSERT,"  FECHA   |   HORA   |   USUARIO   |   DEPARTAMENTO\n\n")
    for line in f:
        txt_log.insert(INSERT,line+"\n")
    f.close()
    txt_log.grid(column=0,row=0)
    window_log.mainloop()

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

# Función encargada de vaciar los valores por defecto en los campos "txt_mail" y "txt_debt" al hacer click sobre ellos.
def removeValue(event):
    event.widget.delete(0, 'end')

# Ventana menu principal y sus pestañas correspondientes como función invocable.
def menu():
    global window_login
    window_login.destroy()
    #window = ThemedTk(theme="yaru")
    global window_menu
    window_menu = Tk()
    #ttk.Style().theme_use('adapta')
    window_menu.title("Let me in")

    for i in range(4):
        window_menu.columnconfigure(i, weight=1, minsize=75)
        window_menu.rowconfigure(i, weight=1, minsize=50)

    tab_control = ttk.Notebook(window_menu)

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

    btn_exit = Button(tab1, text="Log Out", font=("Arial Bold", 20), fg="red", command=logout)
    btn_exit.grid(column=1, row=4, padx=5, pady=5)

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

    global txt_user
    global txt_dpto
    global txt_mail
    global txt_debt
    txt_user = " "
    txt_dpto = " "

    txt_user = Entry(tab2, width=15, font=("Arial Bold", 20))
    txt_user.grid(column=2, row=1, padx=5, pady=5)
    txt_user.bind("<Button-1>", removeValue)

    txt_dpto = Entry(tab2, width=15, font=("Arial Bold", 20))
    txt_dpto.grid(column=2, row=2, padx=5, pady=5)
    txt_dpto.bind("<Button-1>", removeValue)

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

    btn_add = Button(tab2, text="Agregar", font=("Arial Bold", 20), fg="green", command=agregar)
    btn_add.grid(column=3, row=1, padx=5, pady=5)

    btn_del = Button(tab2, text="Eliminar", font=("Arial Bold", 20), fg="red", command=eliminar)
    btn_del.grid(column=3, row=2, padx=5, pady=5)

    btn_show = Button(tab2, text="Mostrar", font=("Arial Bold", 20), fg="blue", command=mostrar)
    btn_show.grid(column=3, row=3, padx=5, pady=5)

    btn_exit2 = Button(tab2, text="Log Out", font=("Arial Bold", 20), fg="red", command=logout)
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

    btn_cge = Button(tab3, text ="Cambiar", font=("Arial Bold", 20), fg="green",  command=change_password)
    btn_cge.grid(column=2, row=4, padx=5, pady=5)

    btn_exit3 = Button(tab3, text="Log Out", font=("Arial Bold", 20), fg="red", command=logout)
    btn_exit3.grid(column=1, row=4, padx=5, pady=5)

    tab_control.pack(expand=1, fill='both')
    window_menu.mainloop()

# Ventana de Log In como función invocable
def login():
    # Creación de la ventana de Log In como variable global
    global window_login
    window_login = Tk()
    #window_login = ThemedTk(theme="yaru")
    window_login.title("Let me in - Log In")
    window_login.bind("<Return>", check_password)
    #window.geometry('350x200')
    global txt_psw
    psw = Label(window_login, text="Contraseña: ", font=("Arial Bold", 20))
    psw.grid(column=0, row=1, padx=5, pady=5)
    txt_psw = Entry(window, width=15, font=("Arial Bold", 20))
    txt_psw.config(show="*")
    txt_psw.grid(column=1, row=1, padx=5, pady=5)
    txt_psw.focus()

    btn_login = Button(window_login, text="Log In", font=("Arial Bold", 20), fg="green", command=check_password)
    btn_login.grid(column=2, row=1, padx=5, pady=5)

    btn_exit = Button(window_login, text="Exit", font=("Arial Bold", 20), fg="red", command=salir)
    btn_exit.grid(column=1, row=2, padx=5, pady=5)
    window_login.mainloop()

if __name__ == '__main__':
    login()
