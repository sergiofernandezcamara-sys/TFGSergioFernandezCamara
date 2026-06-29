Configurar entorno.

Abrir PowerShell y situarse dentro de la carpeta Scripts del proyecto:

cd ...\TFGSergioFernandezCamara\Scripts

Crear el entorno virtual:

python -m venv venv

Activar el entorno virtual:

venv\Scripts\Activate.ps1

Actualizar pip:

python -m pip install --upgrade pip

Instalar las dependencias del proyecto:

pip install -r reqs.txt

Dataset.

Instalar el dataset CICDDoS2019 desde el enlace.

https://www.unb.ca/cic/datasets/ddos-2019.html

Descargar el dataset y colocarlo en la carpeta esperada por el proyecto, manteniendo la estructura de carpetas utilizada por los scripts.

La estructura general esperada es similar a:

TFGSergioFernandezCamara
│
├── Files
│ ├── CICDDoS2019
│ ├── CSV-01-12
│ ├── CSV-03-11
│ └── Parquet
│
├── Scripts
│
└── capturas

Dentro de la carpeta CSV-01-12\01-12 hay que modificar el nombre del archivo:

UDP.csv

por:

DrDoS_UDP.csv

Este cambio es necesario para que el código encuentre correctamente el archivo UDP con el nombre esperado.

Instalar Wireshark en Windows.

Durante la instalación, asegurarse de instalar también Npcap.

En la instalación de Npcap, marcar la opción:

Install Npcap in WinPcap API-compatible Mode

No es necesario instalar WinPcap por separado.
CICFlowMeter puede funcionar correctamente usando Npcap si se instala con compatibilidad con la API de WinPcap.

Comprobar que Dumpcap está instalado en:

C:\Program Files\Wireshark\dumpcap.exe

Comprobar que Dumpcap funciona:

& "C:\Program Files\Wireshark\dumpcap.exe" --version

Listar las interfaces de red disponibles:

& "C:\Program Files\Wireshark\dumpcap.exe" -D

Seleccionar el número de interfaz correspondiente a la tarjeta de red que se quiere capturar.

Ejemplo:

5. Wi-Fi

En ese caso, en el script de captura se debe configurar la interfaz en captador.py como:

interface = "5"

También se debe configurar la ruta de Dumpcap:

DUMPCAP_PATH = r"C:\Program Files\Wireshark\dumpcap.exe"

Instalar Java JDK 8.

Comprobar desde CMD o PowerShell:

java -version

javac -version

Si el equipo tiene otra versión de Java instalada, por ejemplo Java 24, se puede forzar el uso de JDK 8 solo en la terminal donde se va a configurar CICFlowMeter.

Ejemplo:

set JAVA_HOME=C:\Program Files\Java\jdk8
set PATH=%JAVA_HOME%\bin;%PATH%

Comprobar de nuevo:

java -version

Descargar CICFlowMeter oficial.

La carpeta inicial tendrá una estructura similar a:

...\CICFlowMeter
│
├── gradle
├── jnetpcap
├── src
├── build.gradle
├── gradlew
└── gradlew.bat

Abrir CMD o PowerShell dentro de la carpeta principal de CICFlowMeter:

cd ...\CICFlowMeter

Ejecutar:

gradlew.bat distZip

O desde PowerShell:

.\gradlew.bat distZip

Este comando genera la carpeta:

...\CICFlowMeter\build

Dentro de build se genera la distribución de CICFlowMeter.

La ruta esperada es:

...\CICFlowMeter\build\distributions

Dentro de esa carpeta debe aparecer la distribución comprimida de CICFlowMeter 4.0.

Descomprimirlo dentro de:

...\CICFlowMeter\build\distributions

Después de descomprimirlo, acceder a:

...\CICFlowMeter\build\distributions\CICFlowMeter-4.0\CICFlowMeter-4.0\bin

Dentro de esa carpeta debe aparecer el archivo:

cfm.bat

Por tanto, la ruta final del ejecutable de CICFlowMeter será:

...\CICFlowMeter\build\distributions\CICFlowMeter-4.0\CICFlowMeter-4.0\bin\cfm.bat

Localizar jnetpcap.

Dentro de la carpeta principal de CICFlowMeter hay una carpeta llamada:

jnetpcap

Entrar en esa carpeta y localizar la versión de jNetPcap para Windows.

La ruta será:

...\CICFlowMeter\jnetpcap\win\jnetpcap-1.4.r1425

Dentro de esa carpeta debe estar el archivo:

jnetpcap.dll

También debe existir el archivo:

jnetpcap.jar

Configurar JNETPCAP con JAVA_OPTS

Para que CICFlowMeter pueda encontrar la librería nativa de jNetPcap, hay que indicar a Java la ruta donde se encuentra jnetpcap.dll.

Esto se hace usando la variable JAVA_OPTS.

set JAVA_OPTS=-Djava.library.path=C:\CICFlowMeter\jnetpcap\win\jnetpcap-1.4.r1425

En el script conversor.py, se debe de configurar la dirección de cfm.bat:

CFM_PATH=Path(r"...\CICFlowMeter\build\distributions\CICFlowMeter-4.0\CICFlowMeter-4.0\bin\cfm.bat")

También se debe configurar la ruta de JNETPCAP:

JNETPCAP_DIR = Path(r"...\CICFlowMeter\jnetpcap\win\jnetpcap-1.4.r1425")

Una vez realizadas estas configuraciones será necesario iniciar jupyter lab para ejecutar Data_train.ipynb:

venv\Scripts\Activate.ps1
jupyter lab

Dentro del notebook habrá que modificar las direcciones de los archivos para que se ajusten a la localización de TFGSergioFernandezCamara dentro del dispositivo.

Cuando se haya terminado de ejecutar todo el notebook, se modificarán las direcciones de todos los scripts de Python.
Todas las direcciones se encuentran en la parte superior de los archivos, se deberán modificar con la dirección correcta de TFGSergioFernandezCamara.