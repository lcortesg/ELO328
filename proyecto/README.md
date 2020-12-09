# Let Me In

Sistema de reconocimiento de personas.

## Características

- Ingreso mediante contraseña.
- Modificación de contraseña.
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

### Uso de la interfaz

#### Ventana de Log In

![](https://user-images.githubusercontent.com/9634970/101556883-91469180-399a-11eb-9057-745ad075bf65.png)

#### Cierre de programa

![](https://user-images.githubusercontent.com/9634970/101557683-42016080-399c-11eb-8d4b-a501f16aa473.png)

#### Cierre de sesión

![](https://user-images.githubusercontent.com/9634970/101557974-cf44b500-399c-11eb-9076-84e8c75a97c7.png)

#### Monitoreo

![](https://user-images.githubusercontent.com/9634970/101558104-0ca94280-399d-11eb-9991-81364e87b5f3.png)

#### Advertencia de inicio de monitoreo

![](https://user-images.githubusercontent.com/9634970/101558444-c4d6eb00-399d-11eb-9724-86069b1b8e72.png)

#### Advertencia de término de monitoreo

![](https://user-images.githubusercontent.com/9634970/101560108-48460b80-39a1-11eb-8727-ae555c463fc8.png)

#### Log de usuarios

![](https://user-images.githubusercontent.com/9634970/101558485-d4eeca80-399d-11eb-8eba-1e94a55a0af6.png)

#### Gestión de usuarios

![](https://user-images.githubusercontent.com/9634970/101558121-17fc6e00-399d-11eb-829c-10aa5ecfbb2e.png)

#### Advertencia de entrenamiento

![](https://user-images.githubusercontent.com/9634970/101558556-f8197a00-399d-11eb-9f75-9ed5070aa80c.png)

#### Lista de usuarios

![](https://user-images.githubusercontent.com/9634970/101558872-a45b6080-399e-11eb-8110-534e6d19ff4c.png)

#### Cambio de contraseña

![](https://user-images.githubusercontent.com/9634970/101558142-221e6c80-399d-11eb-8ddc-08c2cb1b36ce.png)

#### Errores comunes

*Por terminar*


## To Do
- [x] ~~Search query~~.
- [x] ~~Creación de dataset~~.
- [x] Gestion de usuarios.
- [x] Reconocimiento de usuarios.
- [x] Permitir usuarios con el mismo nombre en diferentes departamentos.
- [x] Modificación de fotografía de usuario encontrado.
- [x] Log In mediante contraseña.
- [x] Capacidad de realizar Log Out
- [x] Modificación de contraseña.
- [x] Ocultar contraseña escrita.
- [x] Hashear contraseñas almacenadas.
- [x] Captura fotográfica con solo 1 usuario en pantalla.
- [x] Captura fotográfica de ROE exclusivamente.
- [x] Entrenamiento como función convocable.
- [x] Guardar modelos entrenados en archivo pickle.
- [x] Interfaz gráfica.
- [x] Implementar advertencia al cerrar el monitoreo.
- [ ] Debugear el programa.
- [ ] Corrección de typos.
- [ ] Mejoramiento de interfaz gráfica.


