import subprocess
from pathlib import Path
import shutil
import time
import os

#Rutas para pruebas de ataque
#READY_DIR = Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\Files\PCAP\DATAready")
#DONE_DIR = Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\Files\PCAP\DATAdone")
#PROC_DIR = Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\Files\PCAP\DATAprocessing")
#CSV_DIR = Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\Files\PCAP\DATAcsv")

READY_DIR = Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\ready")
DONE_DIR = Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\done")
PROC_DIR = Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\processing")
CSV_DIR = Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\csvCreation")
FINAL_DIR=Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\csv")

for folder in [CSV_DIR, PROC_DIR, DONE_DIR, READY_DIR, FINAL_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

def convert_to_flow(pcap_path: Path,output_path: Path):
    CFM_PATH=Path(r"C:\Users\sergi\Desktop\CICFlowMeter\build\distributions\CICFlowMeter-4.0\CICFlowMeter-4.0\bin\cfm.bat")

    JNETPCAP_DIR = Path(r"C:\Users\sergi\Desktop\CICFlowMeter\jnetpcap\win\jnetpcap-1.4.r1425")

    env = os.environ.copy()
    env["JAVA_OPTS"] = f"-Djava.library.path={JNETPCAP_DIR}"

    cmd=[
        "cmd","/c",
        str(CFM_PATH),
        str(pcap_path),
        str(output_path)
    ]
    subprocess.run(cmd,env=env)
    output_file=output_path / f"{pcap_path.name}_Flow.csv"
    csv_file=FINAL_DIR / f"{pcap_path.name}_Flow.csv"
    shutil.move(str(output_file),str(csv_file))

def process_next_file():
    pending_files = sorted(READY_DIR.glob("*"))

    if not pending_files:
        return False
    
    pcap_file = pending_files[0]

    processing_file = PROC_DIR / pcap_file.name
    shutil.move(str(pcap_file), str(processing_file))

    output_file = CSV_DIR

    convert_to_flow(processing_file,output_file)

    #processing_file.unlink()
    done_file = DONE_DIR / processing_file.name
    shutil.move(str(processing_file), str(done_file))
    print(f"Procesado correctamente: {processing_file.name}")

    return True

while True:
    processed = process_next_file()

    if not processed:
        time.sleep(2)