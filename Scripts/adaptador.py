from pathlib import Path
import shutil
import time
import numpy as np
import pandas as pd
from joblib import load
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import keras

CSV_DIR=Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\csv")
CSV_PROC_DIR=Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\csv_proc")
CSV_DONE_DIR=Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\csv_done")
ADAPT_FILE=Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\csv_adapt")

columns_drop=[
    "Unnamed: 0",
    "Flow ID",
    "Src IP",
    "Src Port",
    "Dst IP",
    "Dst Port",
    "Timestamp",
    "Bwd PSH Flags",
    "Fwd URG Flags",
    "Bwd URG Flags",
    "FIN Flag Cnt",
    "PSH Flag Cnt",
    "ECE Flag Cnt",
    "Fwd Byts/b Avg",
    "Fwd Pkts/b Avg",
    "Fwd Blk Rate Avg",
    "Bwd Byts/b Avg",
    "Bwd Pkts/b Avg",
    "Bwd Blk Rate Avg",
    "Label"
]

Schema={
    "Protocol": " Protocol",
    "Flow Duration": " Flow Duration",
    "Tot Fwd Pkts": " Total Fwd Packets",
    "Tot Bwd Pkts": " Total Backward Packets",
    "TotLen Fwd Pkts": "Total Length of Fwd Packets",
    "TotLen Bwd Pkts": " Total Length of Bwd Packets",
    "Fwd Pkt Len Max": " Fwd Packet Length Max",
    "Fwd Pkt Len Min": " Fwd Packet Length Min",
    "Fwd Pkt Len Mean": " Fwd Packet Length Mean",
    "Fwd Pkt Len Std": " Fwd Packet Length Std",
    "Bwd Pkt Len Max": "Bwd Packet Length Max",
    "Bwd Pkt Len Min": " Bwd Packet Length Min",
    "Bwd Pkt Len Mean": " Bwd Packet Length Mean",
    "Bwd Pkt Len Std": " Bwd Packet Length Std",
    "Flow Byts/s": "Flow Bytes/s",
    "Flow Pkts/s": " Flow Packets/s",
    "Flow IAT Mean": " Flow IAT Mean",
    "Flow IAT Std": " Flow IAT Std",
    "Flow IAT Max": " Flow IAT Max",
    "Flow IAT Min": " Flow IAT Min",
    "Fwd IAT Tot": "Fwd IAT Total",
    "Fwd IAT Mean": " Fwd IAT Mean",
    "Fwd IAT Std": " Fwd IAT Std",
    "Fwd IAT Max": " Fwd IAT Max",
    "Fwd IAT Min": " Fwd IAT Min",
    "Bwd IAT Tot": "Bwd IAT Total",
    "Bwd IAT Mean": " Bwd IAT Mean",
    "Bwd IAT Std": " Bwd IAT Std",
    "Bwd IAT Max": " Bwd IAT Max",
    "Bwd IAT Min": " Bwd IAT Min",
    "Fwd PSH Flags": "Fwd PSH Flags",
    "Fwd Header Len": " Fwd Header Length",
    "Bwd Header Len": " Bwd Header Length",
    "Fwd Pkts/s": "Fwd Packets/s",
    "Bwd Pkts/s": " Bwd Packets/s",
    "Pkt Len Min": " Min Packet Length",
    "Pkt Len Max": " Max Packet Length",
    "Pkt Len Mean": " Packet Length Mean",
    "Pkt Len Std": " Packet Length Std",
    "Pkt Len Var": " Packet Length Variance",
    "SYN Flag Cnt": " SYN Flag Count",
    "RST Flag Cnt": " RST Flag Count",
    "ACK Flag Cnt": " ACK Flag Count",
    "URG Flag Cnt": " URG Flag Count",
    "CWE Flag Count": " CWE Flag Count",
    "Down/Up Ratio": " Down/Up Ratio",
    "Pkt Size Avg": " Average Packet Size",
    "Fwd Seg Size Avg": " Avg Fwd Segment Size",
    "Bwd Seg Size Avg": " Avg Bwd Segment Size",
    "Subflow Fwd Pkts": "Subflow Fwd Packets",
    "Subflow Fwd Byts": " Subflow Fwd Bytes",
    "Subflow Bwd Pkts": " Subflow Bwd Packets",
    "Subflow Bwd Byts": " Subflow Bwd Bytes",
    "Init Fwd Win Byts": "Init_Win_bytes_forward",
    "Init Bwd Win Byts": " Init_Win_bytes_backward",
    "Fwd Act Data Pkts": " act_data_pkt_fwd",
    "Fwd Seg Size Min": " min_seg_size_forward",
    "Active Mean": "Active Mean",
    "Active Std": " Active Std",
    "Active Max": " Active Max",
    "Active Min": " Active Min",
    "Idle Mean": "Idle Mean",
    "Idle Std": " Idle Std",
    "Idle Max": " Idle Max",
    "Idle Min": " Idle Min"
}

def prediction_to_if():
    pass

    #time_cols = [
    #    "Flow Duration",
    #    "Flow IAT Mean", "Flow IAT Std", "Flow IAT Max", "Flow IAT Min",
    #    "Fwd IAT Total", "Fwd IAT Mean", "Fwd IAT Std", "Fwd IAT Max", "Fwd IAT Min",
    #    "Bwd IAT Total", "Bwd IAT Mean", "Bwd IAT Std", "Bwd IAT Max", "Bwd IAT Min",
    #    "Active Mean", "Active Std", "Active Max", "Active Min",
    #    "Idle Mean", "Idle Std", "Idle Max", "Idle Min",
    #]

    #summary = df[time_cols].describe().T[["min", "max", "mean", "std"]]
    #print(summary)

    #suspicious_idle = df[
    #    (df["Idle Mean"] > df["Flow Duration"]) |
    #    (df["Idle Max"] > df["Flow Duration"]) |
    #    (df["Idle Min"] > df["Flow Duration"])
    #]
    #df.drop(suspicious_idle,inplace=True)

def adapt_and_predict(file: Path):
    df=pd.read_csv(file,usecols=lambda column: column not in columns_drop)

    df=df.rename(columns=Schema)

    df=df.replace([np.inf,-np.inf],np.nan)
    df = df.dropna().reset_index(drop=True)

    ##############################
    df.to_csv(ADAPT_FILE / file.name,index=False)
    ##############################

    df_float = df.astype("float32").to_numpy()

    model=keras.models.load_model("mejor_modelo.keras")
    ##############################
    print("Comprobación shape: ")
    print(df.columns.tolist())
    print(df.shape)
    print(model.input_shape)
    ##############################

    scaler=load('scaler.bin')
    df_scaled = scaler.transform(df_float)

    proba=model.predict(df_scaled)
    pred = (proba >= 0.5).astype(int)

    ##############################
    print("Columnas raras: ")
    df_scaled_debug = pd.DataFrame(df_scaled, columns=df.columns)

    attack_indices = np.where(pred.flatten() == 1)[0]

    print("Flujos clasificados como ataque:")
    print(attack_indices)

    for i in attack_indices:
        print(f"\n--- Flujo {i} ---")
        print(f"Probabilidad: {proba[i][0]:.6f}")
        print("Valores originales:")
        print(df.iloc[i])

        print("\nColumnas más raras tras escalar:")
        print(
            df_scaled_debug.iloc[i]
            .sort_values(key=abs, ascending=False)
            .head(15)
        )
    ##############################

    ##############################
    cols_debug = [
        " ACK Flag Count",
        " RST Flag Count",
        " SYN Flag Count",
        "Fwd PSH Flags",
        " Init_Win_bytes_backward",
        " Down/Up Ratio"
    ]

    for col in cols_debug:
        idx = df.columns.get_loc(col)
        print("\n", col)
        print("media scaler:", scaler.mean_[idx])
        print("escala scaler:", scaler.scale_[idx])
        print("valores originales en ataques:")
        print(df.loc[attack_indices, col].values)
        print("valores escalados en ataques:")
        print(df_scaled_debug.loc[attack_indices, col].values)
    ##############################

    ##############################
    packets_total = (
        df[" Total Fwd Packets"] +
        df[" Total Backward Packets"]
    )

    payload_total = (
        df["Total Length of Fwd Packets"] +
        df[" Total Length of Bwd Packets"]
    )
    ##############################

    salida_predict = open("myfile.txt", "w")
    salida_predict.write(f"Predicción de {file.name}\n")
    for i, (p, c) in enumerate(zip(proba.flatten(), pred.flatten())):
        salida_predict.write(
            f"Flujo {i}: "
            f"prob={p:.12f}, "
            f"clase={c}, "
            f"paquetes={packets_total.iloc[i]}, "
            f"payload={payload_total.iloc[i]}, "
            f"ACK={df[' ACK Flag Count'].iloc[i]}, "
            f"RST={df[' RST Flag Count'].iloc[i]}, "
            f"SYN={df[' SYN Flag Count'].iloc[i]}, "
            f"duracion={df[' Flow Duration'].iloc[i]}\n"
        )

def control_function():
    pending_files=sorted(CSV_DIR.glob("*.csv"))

    if not pending_files:
        return False
    
    csv_file=pending_files[0]
    processing_file=CSV_PROC_DIR / csv_file.name
    shutil.move(str(csv_file),str(processing_file))

    adapt_and_predict(processing_file)

    #processing_file.unlink()
    done_file=CSV_DONE_DIR / processing_file.name
    shutil.move(str(processing_file),str(done_file))

    return True

while True:
    csv_convert=control_function()
    
    if not csv_convert:
        time.sleep(2)