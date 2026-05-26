import subprocess
from pathlib import Path
import shutil
import time
import os

READY_DIR = Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\ready")
DONE_DIR = Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\done")
PROC_DIR = Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\processing")
TRASH_DIR = Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\trash")
CSV_DIR = Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\csv")

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
    subprocess.run(cmd,env=env,capture_output=True,text=True)

def process_next_file():
    pending_files = sorted(READY_DIR.glob("*.pcap"))

    if not pending_files:
        return False
    
    pcap_file = pending_files[0]

    processing_file = PROC_DIR / pcap_file.name
    shutil.move(str(pcap_file), str(processing_file))

    output_file = CSV_DIR

    try:
        convert_to_flow(processing_file,output_file)

        #processing_file.unlink()
        done_file = DONE_DIR / processing_file.name
        shutil.move(str(processing_file), str(done_file))
        print(f"Procesado correctamente: {processing_file.name}")

    except Exception as e:
        failed_file = TRASH_DIR / processing_file.name
        shutil.move(str(processing_file), str(failed_file))
        print(f"Error procesando {processing_file.name}: {e}")

    return True

while True:
    processed = process_next_file()

    if not processed:
        time.sleep(2)