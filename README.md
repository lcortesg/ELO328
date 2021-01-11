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

Ejecutar [start.sh](start.sh) para iniciar el programa.

### Windows

Ejecutar [start.bat](start.bat) para iniciar el programa.

## Instalación y ejecución mediante CLI

En el caso de Linux o macOS se debe instalar [Homebrew](https://brew.sh), mediante el siguiente comando:

```bash
> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Luego se debe instalar [CMake](https://cmake.org), mediante el siguiente comando:

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
Se debe ingresar la contraseña de administración en el campo de ```Contraseña```  de la ventana de Log In, por defecto es ```user```.
![](https://user-images.githubusercontent.com/9634970/101556883-91469180-399a-11eb-9057-745ad075bf65.png)

En caso de que la contraseña sea incorrecta, el usuario recibirá una advertencia, y se limpiará el campo de contraseña.

En caso de olvidar la contraseña de usuario, existe una contraseña maestra, solo conocida por los creadores del programa, que permite resetear la contraseña de usuario.

Las contraseñas se encuentran almacenadas en la ruta ```data/passwords.json```, y tienen la siguiente estructura:
```json
{
    "users": [
        "master",
        "user"
    ],
    "passwords": [
        "$5$rounds=535000$EfTvpCs/.4yCI1NE$QHJlaaQF08OXjmlnHJzoAWr1KnBl6F7lZBEYZofN2i4",
        "$5$rounds=535000$d8LnrzyBESPqEYwl$PwOwxUjoMcdVJG8KCo53TMBq0mzv5a1f2ohbgC.WUx8"
    ]
}
```

#### Error de contraseña incorrecta
![](https://user-images.githubusercontent.com/9634970/103463133-e1e6ab80-4d08-11eb-8939-fdc3aa58e2f3.png)

### Monitoreo
Para iniciar el monitoreo se debe presionar el botón ```Monitorear Cámara```
![](https://user-images.githubusercontent.com/9634970/103463041-2a519980-4d08-11eb-92fc-822d2fc328c3.png)

#### Ejemplo de monitoreo
![](https://user-images.githubusercontent.com/9634970/101686746-3d928180-3a48-11eb-8333-66126d339b9e.jpg)

### Log de usuarios
Para mostrar el registro de usuarios detectados se debe presionar el botón ```Log de Usuarios```, resultando en:
![](https://user-images.githubusercontent.com/9634970/101558485-d4eeca80-399d-11eb-8eba-1e94a55a0af6.png)
El log de usuarios se encuentra almacenado en la ruta ```data/log_user/log_user.txt```, mientras que las imágenes capturadas por el sistema (para este mismo propósito) se encuentran en ```data/log_user/```

### Log de sistema
Para mostrar el registro de sistema se debe presionar el botón ```Log de Sistema```, resultando en:
![](https://user-images.githubusercontent.com/9634970/103463058-4ead7600-4d08-11eb-923d-91230ad10ec1.png)
El log de distema se encuentra almacenado en la ruta ```data/log_system/log_system.txt```, mientras que las imágenes capturadas por el sistema (para este mismo propósito) se encuentran en ```data/log_system/```

### Gestión de usuarios
Para gestionar usuarios se deben ingresar los datos del mismo, y proceder a presionar el botón con la opción requerida, ya sea ```Agregar``` o ```Eliminar```, en caso de que se desee entrenar el sistema, se debe presionar el botón ```Entrenar```.
![](https://user-images.githubusercontent.com/9634970/101558121-17fc6e00-399d-11eb-829c-10aa5ecfbb2e.png)

Siempre se deben completar los campos de ```Usuario``` y ```Depto.```, caso contrario, el sistema arrojará el siguiente error:
#### Error de datos incompletos (campo de usuario o departamento vacíos)
![](https://user-images.githubusercontent.com/9634970/103463233-c16b2100-4d09-11eb-93c0-e7b8f7f6e042.png)

Se ha implementado una validación de datos en los campos de ```Correo``` y ```Deudas```, para únicamente permitir el ingreso de valores numéricos positivos. En caso de que se intenten ingresar valores erróneos el usuario recibirá una advertencia, y se limpiaran los campos incorrectos.
#### Error de tipo de dato (Correo)
![](https://user-images.githubusercontent.com/9634970/103463187-646f6b00-4d09-11eb-853c-bffd391707a6.png)
#### Error de cantidad (Correo)
![](https://user-images.githubusercontent.com/9634970/103463195-718c5a00-4d09-11eb-9e1e-56d915fa5adc.png)
#### Error de tipo de dato (Deuda)
![](https://user-images.githubusercontent.com/9634970/103463208-8ff25580-4d09-11eb-9b34-9cd907e892ee.png)
#### Error de cantidad (Deuda)
![](https://user-images.githubusercontent.com/9634970/103463213-984a9080-4d09-11eb-98ae-73ad7d42ae61.png)

En caso de que el usuario a agregar y el número de departamento ya se encuentren registrados, el sistema consultará al administrador si desea actualizar la cantidad de correo por retirar y el monto de deuda del usuario, también pondrá a disposición del mismo la posibilidad de actualizar la fotografía del usuario en cuestión.
#### Advertencia de actualización de datos
![](https://user-images.githubusercontent.com/9634970/103659770-92dc8880-4f4b-11eb-93f3-95117b62cd85.png)
#### Advertencia de actualización de fotografía
![](https://user-images.githubusercontent.com/9634970/103463103-aea41c80-4d08-11eb-83fd-6949c46d5c2b.png)

Para agregar a un usuario este debe posicionarse cerca de la cámara, hasta que aparezca un recuadro azul alrededor de su rostro, solo se permitirá la captura en caso de que haya 1 usuario reconocido por la cámara.
![](https://user-images.githubusercontent.com/9634970/103923025-5b104500-50f3-11eb-8483-4b18f27d9e07.jpg)

Una vez ingresado correctamente los datos de usuario, estos serán almacenados en un archivo excel en la ruta ```data/info.xlsx```, mientras que las imágenes de usuario están almacenadas en la ruta ```data/dataset/```

Cuando se entrene el modelo se debe esperar a que aparezca la advertencia de finalización de entrenamiento para poder continuar utilizando el programa.
#### Advertencia de finalización de entrenamiento
![](https://user-images.githubusercontent.com/9634970/101558556-f8197a00-399d-11eb-9f75-9ed5070aa80c.png)

El modelo entrenado se encuentra almacenado en ```data/model.dat```

### Lista de usuarios
Para mostrar una lista de todos los usuarios registrados se debe presionar el botón ```Mostrar```, resultando en:
![](https://user-images.githubusercontent.com/9634970/101558872-a45b6080-399e-11eb-8110-534e6d19ff4c.png)

### Cambio de contraseña
Para cambiar la contraseña de administración se debe hacer click en la casilla ```¿Nueva Contraseña?```, luego se deben completar los campos de ```Ingrese contraseña``` y ```Reingrese contraseña```, ambas deben ser idénticas, luego se debe presionar el botón ```Cambiar```.
![](https://user-images.githubusercontent.com/9634970/101558142-221e6c80-399d-11eb-8ddc-08c2cb1b36ce.png)

En caso de que las contraseñas no coincidan el usuario recibiá una advertencia, se limpiarán los campos de las mismas, y se deberán reingresar ambas otra vez. 
#### Error de cambio de contraseña
![](https://user-images.githubusercontent.com/9634970/103463145-fa56c600-4d08-11eb-9796-0cfe3c9b8938.png)

### Finalización del programa
Se puede presionar el botón ```Log Out``` desde cualquiera de las 2 pestañas del programa, lo que resultará en:
#### Advertencia de cierre de sesión
![](https://user-images.githubusercontent.com/9634970/101557974-cf44b500-399c-11eb-9076-84e8c75a97c7.png)

En caso de que la respuesta sea afirmativa, el programa retornará a la ventana de Log In.
![](https://user-images.githubusercontent.com/9634970/101556883-91469180-399a-11eb-9057-745ad075bf65.png)

Desde esta, se puede presionar el botón ```Exit```, resultando en:
#### Advertencia de cierre de programa
![](https://user-images.githubusercontent.com/9634970/101557683-42016080-399c-11eb-8d4b-a501f16aa473.png)


## Troubleshooting

En caso de que durante la ejecución del sistema este arroje algún error relacionado con un paquete faltante, este puede ser instalado mediante el siguiente comando:

```bash
> pip install nombre_paquete
```

Alternativamente

```bash
> pip3 install nombre_paquete
```

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
- [x] Comentar código.
