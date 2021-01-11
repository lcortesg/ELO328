'''
@File    :   main.py
@Date    :   2021/01/05
@Author  :   Lucas Cortés Gutiérrez.
@Version :   4.0
@Contact :   lucas.cortes.14@sansano.usm.cl"
@Desc    :   Interfaz gráfica del sistema de reconocimineto de personas "Let Me In"
'''

# importar los paquetes necesarios.
from passlib.hash import sha256_crypt
from imutils.video import VideoStream
from tkinter import scrolledtext
from contextlib import suppress
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import manager as man
import monitor as mon
from beepy import *
import stdiomask
import time
import json
import cv2
import os

# Definición de variables de texto, responsables de la entrada de datos.
chk_state = ""
txt_psw = ""
txt_psw2 = ""
txt_user = ""
txt_dpto = ""
txt_mail = ""
txt_debt = ""
window = ""

# Definición de variables booleanas responsables de la validación de datos.
mail_check = False
debt_check = False
data_check = False
# Variable que controla los sonidos del sistema.
sounds = True

# Se extrae la contraseña de administración del archivo JSON.
with open("data/passwords.json", "r") as json_file: 
    data = json.load(json_file) 
    users = data["users"]
    passwords = data["passwords"]

# Función que escribe en el archivo JSON la contraseña de administración.
def write_json(data, filename='data/passwords.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

# Función encargada de llevar un registro de los eventos del sistema.
def system_log(evento):
    # Define una variable de tiempo instantánea.
    now = time.time()
    tiempo = time.localtime(now)
    # Formatea el tiempo que irá al log de sistema.
    time_log = time.strftime("%Y/%m/%d, %H:%M:%S", tiempo)
    # Formatea el tiempo que irá en el nombre de las imágenes del log de sistema.
    time_pic = time.strftime("%Y-%m-%d, %H-%M-%S", tiempo)
    
    # Abre el archivo "log_system.txt".
    with open('data/log_system/log_system.txt', 'r') as original: data = original.read()    
    with open('data/log_system/log_system.txt', 'w') as modified: modified.write(time_log+" - "+evento.upper()+"\r\n" + data)

    # Cierra el archivo "log_system.txt".
    original.close
    modified.close

    # Inicia feed de video.
    vs = VideoStream(0).start()
    cv2.startWindowThread()
    # Pausa para el inicio correcto del sensor de imagen.
    time.sleep(0.5)
    
    while True:
        frame = vs.read()
        frame = cv2.flip(frame, 1)
        # Guarda un screnshot del evento de sistema.
        cv2.imwrite('data/log_system/'+time_pic+" - "+evento.upper()+'.jpg',frame)
        break

    # Libera la cámara y destruye las ventanas.
    VideoStream(0).stop()
    cv2.destroyAllWindows()
    vs.stop()


# Función encargada de llamar al módulo de monitoreo.
def monitorear():
    # Llama a la función "system_log()".
    system_log("inicia monitoreo")
    messagebox.showwarning('Inicia monitoreo','Iniciando monitoreo\n Presionar "ESC" para salir.')
    # Inicia la función de monitoreo.
    mon.monitor()
    # Llama a la función "system_log()".
    system_log("finaliza monitoreo")

# Función que detiene el módulo de monitoreo.
def monitorear_kill():
    # Cierra la función de monitoreo.
    mon.monitor_kill()

# Función encargada de llamar al módulo de entrenamiento.
def entrenar():
    # Llama a la función "system_log()".
    system_log("entrenamiento de modelo")
    # Inicia entrenamiento.
    man.train()
    messagebox.showinfo('Entrenamiento','Entrenamiento Finalizado')

# Función que detiene la ejecución del programa.
def salir():
    print('\007')
    res = messagebox.askokcancel('Salir','¿Está seguro que desea cerrar el programa?')
    if res: 
        # Llama a la función "system_log()".
        system_log("cierre de programa")
        exit()

# Función de cierre de sesión.
# Gracias Aline por el nombre de las variables.
def logout(pelota=False):
    if not pelota:
        print('\007')
        pelota = messagebox.askokcancel('Salir','¿Está seguro que desea cerrar sesión?')
    if pelota:
        global window_menu
        window_menu.destroy()
        with suppress(Exception):
            # Definición de las ventanas de GUI como variables globales.
            global window_show
            global window_log
            global window_logs
            window_log.destroy()
            window_logs.destroy()
            window_show.destroy()
        # Llama a la función "system_log()".
        system_log("cierre de sesion")
        # Llamado de ventana de inicio de sesión.
        login()

# Función de verificación de contraseña.
def check_password(event=None):
    # Recorre las contraseñas almacenadas.
    for i in range(len(users)):
        if sha256_crypt.verify(txt_psw.get(), passwords[i]):
            if sounds: beep(sound=1)
            # Llama a la función "system_log()".
            system_log("inicio de sesion")
            # Llama a la ventana de menu.
            menu()

    # Llama a la función "system_log()".
    system_log("contraseña incorrecta")
    # Limpia la contraseña incorrecta.
    txt_psw.delete(0,"end")
    print('\007')
    messagebox.showwarning('Error','Contraseña Incorrecta')
    txt_psw.focus()

# Función encargada de realizar el cambio de contraseña.
def change_password():
    # Si alguno de los campos de contraeña se encuentra vacío.
    if (txt_psw.get() == "" or txt_psw2.get() == "") : 
        res = messagebox.showwarning('Cambio de contraseña','Campo incompleto')
    else:
        # Si las contraseñas no coinciden.
        if (txt_psw.get() != txt_psw2.get()):
            system_log("cambio de contraseña fallido")
            print('\007')
            messagebox.showwarning('Cambio de contraseña','Las contraseñas no coinciden\n Inténtelo nuevamente.')
        else:
            res = messagebox.askokcancel('Cambio de contraseña','¿Está seguro que desea cambiar la contraseña?')
            if res:
                # Llama a la función "system_log()".
                system_log("cambio de contraseña exitoso")
                # Hashea nueva contraseña y la almacena en el archivo correspondiente.
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
                        logout(True)
            else:
                # Llama a la función "system_log()".
                system_log("cambio de contraseña cancelado")
                messagebox.showwarning('Cambio de contraseña','Cambio de contraseña cancelado')
    txt_psw.delete(0,"end")
    txt_psw2.delete(0,"end")
    chk_state.set(0)
    activate_check()    

# Función encargada de imprimir una lista de los usuarios registrados.
def mostrar():
    # Llama a la función "system_log()".
    system_log("mostrar lista de usuarios")
    # Definición de la ventana de lista de usuarios como variable global.
    global window_show
    window_show = Tk()
    window_show.title("Lista de usuarios")
    txt = scrolledtext.ScrolledText(window_show,width=50,height=20, font=("Arial Bold", 20))
    man.show_user(txt)
    txt.grid(column=0,row=0)
    window_show.mainloop()

# Función encargada de la validación de los datos de correo y deudas, en caso favorable debe agregar al usuario a la base de datos.
def agregar():
    mail_check = False
    debt_check = False
    data_check = False

    with suppress(Exception): 
        # Revisa si es que la entrada de correo es un número entero.
        mail_check = True if type(int(txt_mail.get().strip())) == int else False
    with suppress(Exception): 
        # Revisa si es que la entrada de deuda es un número entero.
        debt_check = True if type(int(txt_debt.get().strip())) == int else False

    # Revisa si la variavle de nombre o departamento se encuentran vacías.
    if txt_user.get().strip() == "" or txt_dpto.get().strip() == "":
        # Llama a la función "system_log()".
        system_log("error al agregar usuario")
        print('\007')
        messagebox.showwarning('Agregar usuario','Campos incompletos')
        return False

    # Si tanto las entradas de usuario como la de departamento contienen texto.
    if txt_user.get().strip() != "" and txt_dpto.get().strip() != "": 
        data_check = True

    # Si el correo no es un número.
    if not mail_check:
        # Llama a la función "system_log()".
        system_log("error al agregar usuario")
        print('\007')
        messagebox.showwarning('Agregar usuario','La cantidad de correo debe ser un número')
        txt_mail.delete(0,"end")
        txt_mail.insert(END, '0')

    # Si la deuda no es un número.
    if not debt_check:
        # Llama a la función "system_log()".
        system_log("error al agregar usuario")
        print('\007')
        messagebox.showwarning('Agregar usuario','El monto adeudado debe ser un número')
        txt_debt.delete(0,"end")
        txt_debt.insert(END, '0')

    # Si la cantidad de correo es menor que 0.
    if (mail_check and int(txt_mail.get()) < 0):
        # Llama a la función "system_log()".
        system_log("error al agregar usuario")
        print('\007')
        messagebox.showwarning('Agregar usuario','La cantidad de correo debe ser mayor o igual a 0')
        txt_mail.delete(0,"end")
        txt_mail.insert(END, '0')
        mail_check = False

    # Si la cantidad de deuda es menor a 0.
    if (debt_check and int(txt_debt.get()) < 0):
        # Llama a la función "system_log()".
        system_log("error al agregar usuario")
        print('\007')
        messagebox.showwarning('Agregar usuario','El monto adeudado debe ser mayor o igual a 0')
        txt_debt.delete(0,"end")
        txt_debt.insert(END, '0')
        debt_check = False

    # Si todos los datos son válidos.
    if (mail_check and debt_check and data_check):
        # Llama a la función "system_log()".
        system_log("agregar/modificar usuario")
        man.add_user(txt_user.get().strip().upper(), txt_dpto.get().strip().upper(), txt_mail.get().strip(), txt_debt.get().strip())
        txt_user.delete(0,"end")
        txt_dpto.delete(0,"end")
        txt_mail.delete(0,"end")
        txt_debt.delete(0,"end")
        txt_mail.insert(END, '0')
        txt_debt.insert(END, '0')

# Función encargada de eliminar a un usuario desde la base de datos.
def eliminar():
    # Si alguna de las entradas de texto está vacía.
    if txt_user.get().strip() == "" or txt_dpto.get().strip() == "": 
        # Llama a la función "system_log()".
        system_log("error al eliminar usuario")
        print('\007')
        messagebox.showwarning('Eliminar usuario','Campos incompletos')
    else:   
        res = messagebox.askyesno('Eliminar usuario','¿Está seguro que desea eliminar al usuario?')
        if res: 
            # Llama a la función "system_log()".
            system_log("eliminar usuario")
            # Llama a la función de eliminación de usuarios.
            man.delete_user(txt_user.get().strip().upper(), txt_dpto.get().strip().upper())
            txt_user.delete(0,"end")
            txt_dpto.delete(0,"end")
            txt_mail.delete(0,"end")
            txt_debt.delete(0,"end")
            txt_mail.insert(END, '0')
            txt_debt.insert(END, '0')

# Función encargada de imprimir el log de los usuarios detectados.
def log_users():
    # Llama a la función "system_log()".
    system_log("log de usuarios")
    # Abre archivo de log de usuarios.
    f = open("data/log_user/log_user.txt", "r")
    # Define la ventana de log de usuarios como variable global.
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

# Función encargada de imprimir el log de los eventos del sistema.
def log_system():
    # Llama a la función "system_log()".
    system_log("log de sistema")
    # abre archivo de log de sistema.
    f = open("data/log_system/log_system.txt", "r")
    # Define la ventana de log de sistema como variable global.
    global window_log
    window_logs = Tk()
    window_logs.title("Eventos de sistema")
    #window.geometry('350x350')
    txt_logs = scrolledtext.ScrolledText(window_logs,width=50,height=20, font=("Arial Bold", 20))
    txt_logs.insert(INSERT,"  FECHA   |   HORA   |   EVENTO\n\n")
    for line in f:
        txt_logs.insert(INSERT,line+"\n")
    f.close()
    txt_logs.grid(column=0,row=0)
    window_logs.mainloop()

# Función encargada de revisar el estado del checkbox en la pestaña de cambio de contraseña.
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
    # Definición de la ventana de Log In como variable global.
    global window_login
    window_login.destroy()

    # Definición de la ventana de Log In como variable global.
    global window_menu
    window_menu = Tk()

    window_menu.title("Let me in")

    for i in range(4):
        window_menu.columnconfigure(i, weight=1, minsize=75)
        window_menu.rowconfigure(i, weight=1, minsize=50)

    tab_control = ttk.Notebook(window_menu)

    # Define las pestañas de la GUI.
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab3 = ttk.Frame(tab_control)

    # Define los nombres de las pestañas de la GUI.
    tab_control.add(tab1, text='Monitoreo')
    tab_control.add(tab2, text='Gestión de Usuarios')
    tab_control.add(tab3, text='Cambio de Contraseña')

    ########## TAB 1 ##########
    persona = Label(tab1, text="Monitoreo de Usuarios", font=("Arial Bold", 20))
    persona.grid(column=1, row=1, padx=5, pady=5)

    # Botón de monitoreo.
    btn_mon = Button(tab1, text="Monitorear Cámara", font=("Arial Bold", 20), fg="green", command=monitorear)
    btn_mon.grid(column=1, row=2, padx=5, pady=5)

    # Botón de log de usuarios.
    btn_log_user = Button(tab1, text="Log de Usuarios", font=("Arial Bold", 20), fg="blue", command=log_users)
    btn_log_user.grid(column=1, row=3, padx=5, pady=5)

    # Botón de log de sistema.
    btn_log_system = Button(tab1, text="Log de Sistema", font=("Arial Bold", 20), fg="blue", command=log_system)
    btn_log_system.grid(column=1, row=4, padx=5, pady=5)

    # Botón de log-out.
    btn_exit = Button(tab1, text="Log Out", font=("Arial Bold", 20), fg="red", command=logout)
    btn_exit.grid(column=1, row=5, padx=5, pady=5)

    ########## TAB 2 ##########
    persona = Label(tab2, text="Gestión de Usuarios", font=("Arial Bold", 20))
    persona.grid(column=2, row=0, padx=5, pady=5)

    # Texto de nombre de usuario.
    persona = Label(tab2, text="Usuario:", font=("Arial Bold", 20))
    persona.grid(column=1, row=1, padx=5, pady=5)

    # Texto de número de departamento.
    departamento = Label(tab2, text="Depto.:", font=("Arial Bold", 20))
    departamento.grid(column=1, row=2, padx=5, pady=5)

    # Texto de cantidad de correo.
    correo = Label(tab2, text="Correo:", font=("Arial Bold", 20))
    correo.grid(column=1, row=3, padx=5, pady=5)

    # Texto de monto de deuda.
    deudas = Label(tab2, text="Deudas:", font=("Arial Bold", 20))
    deudas.grid(column=1, row=4, padx=5, pady=5)

    # Definición de variables globales de usuario, departamento, correo, y deuda.
    global txt_user
    global txt_dpto
    global txt_mail
    global txt_debt
    txt_user = " "
    txt_dpto = " "

    # Entrada de texto de nombre de usuario.
    txt_user = Entry(tab2, width=15, font=("Arial Bold", 20))
    txt_user.grid(column=2, row=1, padx=5, pady=5)
    txt_user.bind("<Button-1>", removeValue)

    # Entrada de texto de número de departamento.
    txt_dpto = Entry(tab2, width=15, font=("Arial Bold", 20))
    txt_dpto.grid(column=2, row=2, padx=5, pady=5)
    txt_dpto.bind("<Button-1>", removeValue)

    # Entrada de texto de cantidad de correo.
    txt_mail = IntVar()
    txt_mail = Entry(tab2, width=15, font=("Arial Bold", 20))
    txt_mail.grid(column=2, row=3, padx=5, pady=5)
    txt_mail.insert(END, '0')
    txt_mail.bind("<Button-1>", removeValue)

    # Entrada de texto de monto de deuda.
    txt_debt = IntVar()
    txt_debt = Entry(tab2, width=15, font=("Arial Bold", 20))
    txt_debt.grid(column=2, row=4, padx=5, pady=5)
    txt_debt.insert(END, '0')
    txt_debt.bind("<Button-1>", removeValue)

    # Botón de entrenamiento.
    btn_trn = Button(tab2, text="Entrenar", font=("Arial Bold", 20), command=entrenar)
    btn_trn.grid(column=3, row=0, padx=5, pady=5)

    # Botón de agregar usuario.
    btn_add = Button(tab2, text="Agregar", font=("Arial Bold", 20), fg="green", command=agregar)
    btn_add.grid(column=3, row=1, padx=5, pady=5)

    # Botón de eliminar usuario.
    btn_del = Button(tab2, text="Eliminar", font=("Arial Bold", 20), fg="red", command=eliminar)
    btn_del.grid(column=3, row=2, padx=5, pady=5)

    # Botón de mostrar usuario.
    btn_show = Button(tab2, text="Mostrar", font=("Arial Bold", 20), fg="blue", command=mostrar)
    btn_show.grid(column=3, row=3, padx=5, pady=5)

    # Botón de log-out.
    btn_exit2 = Button(tab2, text="Log Out", font=("Arial Bold", 20), fg="red", command=logout)
    btn_exit2.grid(column=3, row=4, padx=5, pady=5)

    txt_user.focus()

    ########## TAB 3 ##########
    # Definición de variables globales de contraseñas y estado de check-box.
    global txt_psw
    global txt_psw2
    global chk_state

    # Texto de cmabio de contraseña.
    ps = Label(tab3, text="Cambio de credenciales", font=("Arial Bold", 20))
    ps.grid(column=1, row=1, padx=5, pady=5)
    psw = Label(tab3, text="Ingrese contraseña:", font=("Arial Bold", 20))
    psw.grid(column=1, row=2, padx=5, pady=5)
    psw2 = Label(tab3, text="Reingrese contraseña:", font=("Arial Bold", 20))
    psw2.grid(column=1, row=3, padx=5, pady=5)

    # Entrada de texto de contraseña 1.
    txt_psw = Entry(tab3, width=15, font=("Arial Bold", 20), state='disabled')
    txt_psw.config(show="*")
    txt_psw.grid(column=2, row=2, padx=5, pady=5)

    # Entrada de texto de contraseña 2.
    txt_psw2 = Entry(tab3, width=15, font=("Arial Bold", 20), state='disabled')
    txt_psw2.config(show="*")
    txt_psw2.grid(column=2, row=3, padx=5, pady=5)

    chk_state = IntVar()
    chk_state.set(0)
    chk = Checkbutton(tab3, text='¿Nueva Contraseña?', font=("Arial Bold", 20), fg="red", variable=chk_state, command=activate_check)
    chk.grid(column=2, row=1, padx=5, pady=5)

    # Botón de cambio de contraseña.
    btn_cge = Button(tab3, text ="Cambiar", font=("Arial Bold", 20), fg="green",  command=change_password)
    btn_cge.grid(column=2, row=4, padx=5, pady=5)
    
    # Botón de log-out.
    btn_exit3 = Button(tab3, text="Log Out", font=("Arial Bold", 20), fg="red", command=logout)
    btn_exit3.grid(column=1, row=4, padx=5, pady=5)

    tab_control.pack(expand=1, fill='both')
    window_menu.mainloop()

# Ventana de Log In como función invocable
def login():
    # Definición de la ventana de Log In como variable global
    global window_login
    window_login = Tk()
    window_login.title("Let me in - Log In")
    window_login.bind("<Return>", check_password)
    #window.geometry('350x200')

    # Definición de contraseña como variable global.
    global txt_psw
    psw = Label(window_login, text="Contraseña: ", font=("Arial Bold", 20))
    psw.grid(column=0, row=1, padx=5, pady=5)
    txt_psw = Entry(window, width=15, font=("Arial Bold", 20))
    txt_psw.config(show="*")
    txt_psw.grid(column=1, row=1, padx=5, pady=5)
    txt_psw.focus()

    # Botón de log-in.
    btn_login = Button(window_login, text="Log In", font=("Arial Bold", 20), fg="green", command=check_password)
    btn_login.grid(column=2, row=1, padx=5, pady=5)

    # Bontón de exit.
    btn_exit = Button(window_login, text="Exit", font=("Arial Bold", 20), fg="red", command=salir)
    btn_exit.grid(column=1, row=2, padx=5, pady=5)
    window_login.mainloop()

if __name__ == '__main__':
    login()
