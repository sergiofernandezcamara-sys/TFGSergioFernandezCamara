import subprocess
import time
from pathlib import Path

PYTHON = "C:/Users/sergi/Desktop/TFGSergioFernandezCamara/Scripts/venv/Scripts/python.exe"

SCRIPTS = [
    ("Dashboard", "C:/Users/sergi/Desktop/TFGSergioFernandezCamara/Scripts/dashboard.py", 5),
    ("Adaptador", "C:/Users/sergi/Desktop/TFGSergioFernandezCamara/Scripts/adaptador.py", 15),
    ("Conversor", "C:/Users/sergi/Desktop/TFGSergioFernandezCamara/Scripts/conversor.py", 5),
    ("Captador", "C:/Users/sergi/Desktop/TFGSergioFernandezCamara/Scripts/captador.py", 0),
]

for title, script, wait_time in SCRIPTS:
    subprocess.Popen(
        [
            "cmd",
            "/k",
            f'title {title} & {PYTHON} {script}'
        ],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    time.sleep(wait_time)