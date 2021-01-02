# Let Me In

Sistema de reconocimiento de personas.

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## [License](LICENSE)

## [Changelog](CHANGELOG.md)

## [Releases](https://github.com/lcortesg/Let-Me-In/releases)

## To Do
- [x] ~~Search query~~.
- [x] ~~Creación de dataset~~.
- [x] Gestion de usuarios.
- [x] Reconocimiento de usuarios.
- [x] Permitir usuarios con el mismo nombre en diferentes departamentos.
- [x] Modificación de datos de usuario encontrado.
- [x] Modificación de fotografía de usuario encontrado.
- [x] Captura fotográfica con solo 1 usuario en pantalla.
- [x] Captura fotográfica de ROE exclusivamente.
- [x] Log In mediante contraseña.
- [x] Capacidad de realizar Log Out
- [x] Modificación de contraseña.
- [x] Ocultar contraseña escrita.
- [x] Hashear contraseñas almacenadas.
- [x] Entrenamiento como función invocable.
- [x] Guardar modelos entrenados en archivo pickle.
- [x] Interfaz gráfica.
- [x] Implementar advertencia al cerrar el monitoreo.
- [x] Log de usuarios como función invocable.
- [x] Mejoramiento de interfaz de monitoreo.
- [x] Mejoramiento de interfaz de enrolamiento.
- [x] Agregar información a pantalla de captura y montitoreo.
- [x] Remoción de duplicados durante etapa de reconocimiento.
- [x] System Log (inicios de sesión, cambios de contraseña, etc).
- [ ] Debugear el programa.
- [ ] Corrección de typos.
- [ ] Mejoramiento de interfaz gráfica.

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

Alternativamente

```
$ chmod a+x start.sh
ejecutar start.sh
```


### Manual de usuario

#### Inicio de sesión
Se debe ingresar la contraseña de administración en el campo de "Contraseña" de la ventana de Log In.

En caso de que la contraseña sea incorrecta, el usuario recibirá una advertencia, y se limpiará el campo de contraseña.
![](https://user-images.githubusercontent.com/9634970/101556883-91469180-399a-11eb-9057-745ad075bf65.png)

#### Monitoreo
Para iniciar el monitoreo se debe presionar el botón "Monitorear Cámara"
![](https://user-images.githubusercontent.com/9634970/101558104-0ca94280-399d-11eb-9991-81364e87b5f3.png)

Ejemplo de monitore
![](https://user-images.githubusercontent.com/9634970/101686746-3d928180-3a48-11eb-8333-66126d339b9e.jpg)

#### Log de usuarios
Para mostrar el registro de usuarios detectados se debe presionar el botón "Log de Usuarios", resultando en:
![](https://user-images.githubusercontent.com/9634970/101558485-d4eeca80-399d-11eb-8eba-1e94a55a0af6.png)

#### Log de sistema
Para mostrar el registro de sistema detectados se debe presionar el botón "Log de Sistema", resultando en:
![](https://user-images.githubusercontent.com/9634970/101558485-d4eeca80-399d-11eb-8eba-1e94a55a0af6.png)

#### Gestión de usuarios
Para gestionar usuarios se deben ingresar los datos del mismo, y proceder a presionar el botón con la opción requerida, ya sea "Agregar" o "Eliminar", en caso de que se desee entrenar el sistema, se debe presionar el botón "Entrenar".

Se ha implementado validación de datos en los campos de "Correo" y "Deudas", para únicamente permitir el ingreso de valores numéricos positivos, en caso de que se intenten ingresar valores erróneos el usuario recibirá una advertencia, y se limpiaran los campos incorrectos.

En caso de que el usuario a agregar y el número de departamento ya se encuentren registrados, el sistema consultará al administrador si desea actualizar la cantidad de correo por retirar y el monto de deuda del usuario, también pondrá a disposición del mismo la posibilidad de actualizar la fotografía del usuario en cuestión.

![](https://user-images.githubusercontent.com/9634970/101558121-17fc6e00-399d-11eb-829c-10aa5ecfbb2e.png)

#### Lista de usuarios
Para mostrar una lista de todos los usuarios registrados se debe presionar el botón "Mostrar", resultando en:
![](https://user-images.githubusercontent.com/9634970/101558872-a45b6080-399e-11eb-8110-534e6d19ff4c.png)

#### Cambio de contraseña
Para cambiar la contraseña de administración se debe hacer click en la casilla "¿Nueva Contraseña?", luego se deben completar los campos de "Ingrese contraseña" y "Reingrese contraseña", ambas deben ser idénticas, luego se debe presionar el botón "Cambiar", en caso de que las contraseñas no coincidan el usuario recibiá una advertencia, se limpiarán los campos de las mismas, y se deberán reingresar ambas otra vez. 
![](https://user-images.githubusercontent.com/9634970/101558142-221e6c80-399d-11eb-8ddc-08c2cb1b36ce.png)


#### Errores y advertencias varias

#### Advertencia de inicio de monitoreo
![](https://user-images.githubusercontent.com/9634970/101558444-c4d6eb00-399d-11eb-9724-86069b1b8e72.png)

#### Advertencia de término de monitoreo
![](https://user-images.githubusercontent.com/9634970/101560108-48460b80-39a1-11eb-8727-ae555c463fc8.png)

#### Advertencia de finalización de entrenamiento
![](https://user-images.githubusercontent.com/9634970/101558556-f8197a00-399d-11eb-9f75-9ed5070aa80c.png)

#### Advertencia de cierre de sesión
![](https://user-images.githubusercontent.com/9634970/101557974-cf44b500-399c-11eb-9076-84e8c75a97c7.png)

#### Advertencia de cierre de programa
![](https://user-images.githubusercontent.com/9634970/101557683-42016080-399c-11eb-8d4b-a501f16aa473.png)

*POR TERMINAR*
#### Advertencia de actualización de datos
#### Advertencia de actualización de fotografía
#### Advertencia de cambio de contraseña exitoso

#### Error de contraseña incorrecta
#### Error de cambio de contraseña
#### Error de tipo de dato (Correo)
#### Error de cantidad (Correo)
#### Error de tipo de dato (Deuda)
#### Error de cantidad (Deuda)


