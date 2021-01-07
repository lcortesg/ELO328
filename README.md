# Let Me In

Sistema de reconocimiento de personas.

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## [License](LICENSE)

## [Contributing](CONTRIBUTING.md)

## [Changelog](CHANGELOG.md)

## [Releases](https://github.com/lcortesg/Let-Me-In/releases)

## Características

- Ingreso mediante contraseña.
- Modificación de contraseña.
- Monitoreo de cámaras de seguridad.
- Registro de usuarios detectados.
- Registros del sistema.
- Fotografías que respaldan dichos registros.
- Gestión de usuarios (enrolamiento, eliminación, modificación).
- Entrenamiendo de modelo bajo demanda.

## Instalación

### [Requerimientos](requirements.txt)

- [Python 3.3 - 3.8](https://www.python.org/downloads/)
- [CMake](https://cmake.org)
- dlib
- pillow
- numpy
- imutils
- openpyxl
- face_recognition
- opencv-python
- passlib
- stdiomask
- simpleaudio
- beepy

Se debe instalar la versión oficial de python (se recomienda la versión 3.8) encontrada en el siguiente [link](https://www.python.org/downloads/). 

Es imperativo que python se instale mediante esta vía, ya que las versiones suministradas por gestores de paquetes tales como brew y cask no incluyen el módulo Tkinter por defecto.

### UNIX (Linux o macOS)
Se deben cambiar los permisos del archivo [install.sh](install.sh) para permitir su ejecución.

```bash
> chmod a+x install.sh
```

En caso de existir problemas con la modificación de permisos, se recomienda setearlos directamente con:

```bash
> chmod 755 install.sh
```

ejecutar [install.sh](install.sh) para instalar las dependencias correspondientes, listadas en el archivo [requirements.txt](requirements.txt).

### Windows

ejecutar [install.bat](install.bat) para instalar las dependencias correspondientes, listadas en el archivo [requirements.txt](requirements.txt).

## Ejecución

### UNIX (Linux o macOS)
Se deben cambiar los permisos del archivo [start.sh](start.sh) para permitir su ejecución.

```bash
> chmod a+x start.sh
```

En caso de existir problemas con la modificación de permisos, se recomienda setearlos directamente con:

```bash
> chmod 755 start.sh
```

Ejecutar [start.sh](start.sh) para correr el programa.

### Windows

Ejecutar [start.bat](start.bat) para correr el programa.

## Instalación y ejecución mediante CLI

En el caso de Linux o macOS se debe instalar [Homebrew](https://brew.sh), mediante el siguiente comando:

```bash
> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Luego instalar [CMake](https://cmake.org) mediante:

```bash
> brew install cmake
```

Si Python3 es el intérprete por defecto del sistema

```bash
> pip install -r requirements.txt
> python main.py
```

Si Python3 no es el intérprete por defecto del sistema

```bash
> pip3 install -r requirements.txt
> python3 main.py
```


## Manual de usuario

### Inicio de sesión
Se debe ingresar la contraseña de administración en el campo de "Contraseña" de la ventana de Log In, por default es "user", en caso de olvidar la contraseña existe una contraseña maestra, solo conocida por los creadores del programa, que permite resetear la contraseña de usuario.

En caso de que la contraseña sea incorrecta, el usuario recibirá una advertencia, y se limpiará el campo de contraseña.
![](https://user-images.githubusercontent.com/9634970/101556883-91469180-399a-11eb-9057-745ad075bf65.png)

### Monitoreo
Para iniciar el monitoreo se debe presionar el botón "Monitorear Cámara"
![](https://user-images.githubusercontent.com/9634970/103463041-2a519980-4d08-11eb-92fc-822d2fc328c3.png)

Ejemplo de monitoreo
![](https://user-images.githubusercontent.com/9634970/101686746-3d928180-3a48-11eb-8333-66126d339b9e.jpg)

### Log de usuarios
Para mostrar el registro de usuarios detectados se debe presionar el botón "Log de Usuarios", resultando en:
![](https://user-images.githubusercontent.com/9634970/101558485-d4eeca80-399d-11eb-8eba-1e94a55a0af6.png)

### Log de sistema
Para mostrar el registro de sistema detectados se debe presionar el botón "Log de Sistema", resultando en:
![](https://user-images.githubusercontent.com/9634970/103463058-4ead7600-4d08-11eb-923d-91230ad10ec1.png)

### Gestión de usuarios
Para gestionar usuarios se deben ingresar los datos del mismo, y proceder a presionar el botón con la opción requerida, ya sea "Agregar" o "Eliminar", en caso de que se desee entrenar el sistema, se debe presionar el botón "Entrenar".

Se ha implementado validación de datos en los campos de "Correo" y "Deudas", para únicamente permitir el ingreso de valores numéricos positivos, en caso de que se intenten ingresar valores erróneos el usuario recibirá una advertencia, y se limpiaran los campos incorrectos.

En caso de que el usuario a agregar y el número de departamento ya se encuentren registrados, el sistema consultará al administrador si desea actualizar la cantidad de correo por retirar y el monto de deuda del usuario, también pondrá a disposición del mismo la posibilidad de actualizar la fotografía del usuario en cuestión.

Para agregar al usuario este debe posicionarse cerca de la cámara, hasta que aparezca un recuadro azul alrededor de su rostro, solo se permitirá la captura en caso de que haya 1 usuario reconocido por la cámara.

Cuando se entrene el modelo se debe esperar a que aparezca la advertencia de finalización de entrenamiento para poder continuar utilizando el programa.

![](https://user-images.githubusercontent.com/9634970/101558121-17fc6e00-399d-11eb-829c-10aa5ecfbb2e.png)

### Lista de usuarios
Para mostrar una lista de todos los usuarios registrados se debe presionar el botón "Mostrar", resultando en:
![](https://user-images.githubusercontent.com/9634970/101558872-a45b6080-399e-11eb-8110-534e6d19ff4c.png)

### Cambio de contraseña
Para cambiar la contraseña de administración se debe hacer click en la casilla "¿Nueva Contraseña?", luego se deben completar los campos de "Ingrese contraseña" y "Reingrese contraseña", ambas deben ser idénticas, luego se debe presionar el botón "Cambiar", en caso de que las contraseñas no coincidan el usuario recibiá una advertencia, se limpiarán los campos de las mismas, y se deberán reingresar ambas otra vez. 
![](https://user-images.githubusercontent.com/9634970/101558142-221e6c80-399d-11eb-8ddc-08c2cb1b36ce.png)


## Errores y advertencias varias

### Advertencia de inicio de monitoreo
![](https://user-images.githubusercontent.com/9634970/101558444-c4d6eb00-399d-11eb-9724-86069b1b8e72.png)

### Advertencia de término de monitoreo
![](https://user-images.githubusercontent.com/9634970/101560108-48460b80-39a1-11eb-8727-ae555c463fc8.png)

### Advertencia de finalización de entrenamiento
![](https://user-images.githubusercontent.com/9634970/101558556-f8197a00-399d-11eb-9f75-9ed5070aa80c.png)

### Advertencia de cierre de sesión
![](https://user-images.githubusercontent.com/9634970/101557974-cf44b500-399c-11eb-9076-84e8c75a97c7.png)

### Advertencia de cierre de programa
![](https://user-images.githubusercontent.com/9634970/101557683-42016080-399c-11eb-8d4b-a501f16aa473.png)

### Advertencia de inicio de enrolamiento
![](https://user-images.githubusercontent.com/9634970/103463402-d72d1600-4d0a-11eb-9605-221b777ab02a.png)

### Advertencia de cancelación de enrolamiento
![](https://user-images.githubusercontent.com/9634970/103463394-cbd9ea80-4d0a-11eb-8a30-4539db175d51.png)

### Advertencia de actualización de fotografía
![](https://user-images.githubusercontent.com/9634970/103463103-aea41c80-4d08-11eb-83fd-6949c46d5c2b.png)

### Advertencia de actualización de datos
![](https://user-images.githubusercontent.com/9634970/103659770-92dc8880-4f4b-11eb-93f3-95117b62cd85.png)

### Advertencia de cambio de contraseña exitoso
![](https://user-images.githubusercontent.com/9634970/103463123-d2676280-4d08-11eb-9ba8-732de724dc2b.png)

### Error de contraseña incorrecta
![](https://user-images.githubusercontent.com/9634970/103463133-e1e6ab80-4d08-11eb-8939-fdc3aa58e2f3.png)

### Error de cambio de contraseña
![](https://user-images.githubusercontent.com/9634970/103463145-fa56c600-4d08-11eb-9796-0cfe3c9b8938.png)

### Error de tipo de dato (Correo)
![](https://user-images.githubusercontent.com/9634970/103463187-646f6b00-4d09-11eb-853c-bffd391707a6.png)

### Error de cantidad (Correo)
![](https://user-images.githubusercontent.com/9634970/103463195-718c5a00-4d09-11eb-9e1e-56d915fa5adc.png)

### Error de tipo de dato (Deuda)
![](https://user-images.githubusercontent.com/9634970/103463208-8ff25580-4d09-11eb-9b34-9cd907e892ee.png)

### Error de cantidad (Deuda)
![](https://user-images.githubusercontent.com/9634970/103463213-984a9080-4d09-11eb-98ae-73ad7d42ae61.png)

### Error de datos incompletos (campo de usuario o departamento vacíos)
![](https://user-images.githubusercontent.com/9634970/103463233-c16b2100-4d09-11eb-93c0-e7b8f7f6e042.png)


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
- [x] Eliminación de temas desde requirements.
- [x] Debugging
- [x] Corrección de typos.
- [x] Mejoramiento de interfaz gráfica.
