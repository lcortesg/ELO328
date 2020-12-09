# Let Me In

Sistema de reconocimiento de personas.

## Características

- Ingreso mediante contraseña.
- Modificación de contraseña-
- Monitoreo de cámaras de seguridad.
- Registro de usuarios detectados.
- Fotografías que respaldan dichos registros.
- Gestión de usuarios (enrolamiento, eliminación, modificación).
- Entrenamiendo de modelo bajo demanda.

## Instalación

### Requerimientos

- Python 3.3 - 3.8
- CMake
- dlib
- pillow
- numpy
- imutils
- openpyxl
- face_recognition
- opencv-python
- passlib
- stdiomask


### Ejecución

```
$ pip install -r requirements.txt
$ python main.py
```

Alternativamente

```
$ pip3 install -r requirements.txt
$ python3 main.py
```

## To Do
- [x] ~~Search query~~.
- [x] ~~Creación de dataset~~.
- [x] Gestion de usuarios.
- [x] Reconocimiento de usuarios.
- [x] Permitir usuarios con el mismo nombre en diferentes departamentos.
- [x] Modificación de fotografía de usuario encontrado.
- [x] Acceso mediante contraseña.
- [x] Modificación de contraseña.
- [x] Ocultar contraseña escrita.
- [x] Hashear contraseñas almacenadas.
- [x] Captura fotográfica con solo 1 usuario en pantalla.
- [x] Captura fotográfica de ROE exclusivamente.
- [x] Entrenamiento como función convocable.
- [x] Guardar modelos entrenados en archivo pickle.
- [x] Interfaz gráfica.
- [ ] Debugear el programa.
- [ ] Mejoramiento de interfaz gráfica.