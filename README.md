# Sistema de automatización de trámites administrativos mediante IA telefónica

## Descripción

Este proyecto consiste en un sistema local de desarrollo que permite simular la realización de trámites administrativos mediante un **agente conversacional accesible a través de una llamada VoIP**.

El sistema consta de varios componentes que trabajan conjuntamente:

- **Aplicación web desarrollada con Flask**, pensada para empleados de las Administraciones públicas, desde donde pueden gestionar y tramitar las peticiones recibidas en el sistema.
- **Agente conversacional en Dialogflow**, encargado de interpretar y recuperar la información del usuario durante la llamada.
- **Bot de Discord**, utilizado para extraer el audio de la llamada y comunicarse con Dialogflow.
- **Servicio de correo electrónico**, encargado de enviar notificaciones a los empleados desde la plataforma web.
- **Ngrok**, utilizado para exponer el servidor local a internet y poder comunicar la plataforma web con Dialogflow.

El objetivo de este proyecto es facilitar el acceso a servicios administrativos a los sectores de la población con dificultades para utilizar las herramientas digitales actuales, simplificando el proceso mediante una llamada y reduciendo así la brecha digital.

>Nota: La memoria completa del TFG se encuentra en la ruta ```/documents/memoria.pdf``` dentro del repositorio.
---

## Dependencias del sistema

El sistema depende de varios servicios externos:

- Discord
- Dialogflow
- Google Cloud
- Ngrok

### Software necesario

- Python 3.13 o superior
- pip
- Navegador web moderno
- Cuenta en Ngrok
- Cuenta en Google Cloud
- Cuenta en Discord

Todas las dependencias están definidas en ```requirements.txt```.

---

## Instalación del proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/humaral/tfg.git
cd tfg
```

### 2. Crear el entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/macOS

```bash
source venv/bin/activate
```

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

> Crear un archivo ```.env``` con las variables de entorno del proyecto. Debe incluir al menos las siguientes variables:

- **DIALOGFLOW_CREDENTIALS**
- **DISCORD_TOKEN**
- *VOSK_MODEL_PATH* (*opcional*).

---

## Configuración del agente de Dialogflow

El repositorio incluye una copia exportada del agente conversacional utilizado por el sistema, ubicada en:
```/scripts_aux/services/models/Operador.zip```

Pasos para importar el agente:

1. Acceder a la [consola de Dialogflow](https://dialogflow.cloud.google.com) - <https://dialogflow.cloud.google.com>.
2. Crear un nuevo agente.
3. Seleccionar la opción **Import from ZIP** en la configuración.
4. Subir el archivo **Operador.zip**.

---

## Configuración de Google Cloud

Para que la aplicación pueda comunicarse con Dialogflow y para poder usar los servicios de STT es necesario disponer de credenciales de Google Cloud.

1. Acceder a la [consola de Google Cloud](https://console.cloud.google.com/) - <https://console.cloud.google.com/>.
2. Crear un proyecto de Google Cloud.
3. Activar el servicio de facturación.
4. Vincular el agente de Dialogflow al proyecto.
5. Activar el servicio de Speech-to-Text en el proyecto. (*opcional*)
6. Crear una **Cloud Resource Manager API** asociada a los servicios de Dialogflow y STT y descargar el archivo JSON con sus credenciales.
7. Añadir en el archivo ```.env``` la variable de entorno **DIALOGFLOW_CREDENTIALS** con la ruta donde se almacene el archivo JSON con las credenciales.

---

## Configuración de Vosk

En caso de preferir usar un modelo local para realizar el Speech-to-Text:

1. Descargar el [modelo Vosk](https://alphacephei.com/vosk/models) en <https://alphacephei.com/vosk/models>.
2. Descomprimir la carpeta y añadirla al proyecto.
3. Añadir en el archivo ```.env``` la variable de entorno **VOSK_MODEL_PATH** con la ruta donde se almacene la carpeta con el modelo.
4. Acceder al archivo ```scripts_aux\services\discord_bot.py``` y cambiar la variable global ```USE_LOCAL_STT=True```.

---

## Configuración del bot de Discord

El código del bot se encuentra en: ```scripts_aux\services\discord_bot.py```

Para utilizar este código hay que seguir los siguientes pasos:

1. Acceder a [Discord Developer Portal](https://discord.com/developers) - <https://discord.com/developers>.
2. Crear una nueva aplicación.
3. Añadir un bot a la aplicación.
4. Copiar el token de autenticación del bot y añadirlo en ```.env``` en la variable **DISCORD_TOKEN**.
5. Crear un servidor de Discord.
6. Generar un enlace de invitación desde el portal de desarrolladores e invitar al bot al servidor de Discord.
7. Crear un canal de voz en el servidor de Discord, limitado a 2 usuarios.

> Nota: El bot debe tener permisos para conectarse a canales de voz, hablar y mover miembros.

---

## Configuración de Ngrok

Antes de iniciar Ngrok por primera vez:

1. Acceder al [dashboard de Ngrok](https://dashboard.ngrok.com/) - <https://dashboard.ngrok.com/>.
2. Copiar el Authtoken y añadirlo al entorno con el comando ```ngrok config add-authtoken TU_TOKEN_NGROK```.
3. Ir a la pestaña Domains en el dashboard de Ngrok y copiar la URL pública donde se levantará la aplicación web.
4. En la consola de Dialogflow, acceder a la pestaña de fulfillment y añadir la URL del webhook de la aplicación web - **https://TU_URL_NGROK/webhook**.

---

## Despliegue del sistema

### 1. Iniciar el servidor de correo smtpd

```bash
py -m aiosmtpd -n -l localhost:1025
```

> Los correos electrónicos se recibirán en texto plano en el terminal donde se ejecute este comando.

### 2. Iniciar el servidor Flask

```bash
py app.py
```

> La aplicación web quedará disponible en ```http://localhost:5000```.

### 3. Iniciar el servicio de Ngrok

```bash
ngrok http 5000
```

> Ngrok generará una URL pública para conectar el servicio externo de Dialogflow con el servidor local.

### 4. Iniciar el bot de Discord

```bash
py .\scripts_aux\services\discord_bot.py
```

> El bot se conectará al servidor de Discord y cuando el usuario entre al canal de voz, dará comienzo la llamada.

---

## Autor

Proyecto desarrollado como **Trabajo de Fin de Grado de la titulación de Grado en Ingeniería Informática, mención en Computación, de la Universidad de Valladolid**.

Autor: **Hugo Martín Alonso**

---
