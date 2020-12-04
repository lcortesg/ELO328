import administrar as admin
import gestion as gest
import monitor as mon

def main():
    while True:
        modo = input("(U) Gestionar Usuarios. (A) Gestionar Administradores. (M) Monitorear/Reconocer. (Q) Salir. : ")
        if (modo == "Q" or modo == "q"):
            print ("HASTA PRONTO")
            exit()
        if (modo == "U" or modo == "u"):
            gest.gestion_check()
        if (modo == "A" or modo == "a"):
            admin.administrar_check()
        if (modo == "M" or modo == "m"):
            mon.reconocer()
main()