import subprocess
import shutil
from pathlib import Path
from datetime import datetime

DUMPCAP_PATH = r"C:\Program Files\Wireshark\dumpcap.exe"
INCOMING_DIR = Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\incoming")
READY_DIR = Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\ready")

for folder in [INCOMING_DIR, READY_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

#dumpcap.exe -D
interface = "5"

def capture_one_pcap():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    incoming_file = INCOMING_DIR / f"captura_{timestamp}.pcap"
    ready_file = READY_DIR / incoming_file.name

    cmd = [
        DUMPCAP_PATH,
        "-i", interface,
        "-s", "0",
        "-F", "pcap",
        "-a", "duration:60",
        "-c", "10000",
        "-w", str(incoming_file)
    ]

    process = subprocess.Popen(cmd)
    process.wait()

    if not incoming_file.exists():
        raise FileNotFoundError(f"No se ha creado el PCAP esperado: {incoming_file}")

    shutil.move(str(incoming_file), str(ready_file))

    print(f"PCAP listo: {ready_file}")

while True:
    capture_one_pcap()