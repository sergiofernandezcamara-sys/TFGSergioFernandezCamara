import pandas as pd
import numpy as np
import glob
import os
from tqdm import tqdm
import datetime as dt
from pathlib import Path

#OUTPUT_DIR = Path(r"C:\Users\sergi\Desktop\TFGSergioFernandezCamara\capturas\ready")
#date=dt.datetime.now()
#string=str(OUTPUT_DIR / f"captura-{date}.pcap")
#print(string)

#Variable type
#Schema={
#    " Total Fwd Packets" : "int32",
#    " Fwd Header Length" : "int64",
#    " Bwd Header Length" : "int64",
#    "Subflow Fwd Packets" : "int32",
#    " act_data_pkt_fwd" : "int16",
#    " min_seg_size_forward" : "int32"
#}

#def apply_schema(df,schema):
#    for col,dtype in schema.items():
#        if col in df.columns:
#            df[col]=df[col].astype(dtype)
#    return df

#archivos_input=(
#    glob.glob("C:/Users/sergi/Desktop/TFGSergioFernandezCamara/Files/CSV-01-12/01-12/*.csv") + 
#    glob.glob("C:/Users/sergi/Desktop/TFGSergioFernandezCamara/Files/CSV-03-11/03-11/*.csv")
#)

#def shrink_df(df: pd.DataFrame,skip=None)->pd.DataFrame:

#    if skip is None:
#        skip=set()
#    elif isinstance(skip,str):
#        skip={skip}
#    else:
#        skip=set(skip)
#    
#    for col in df.columns:
#        if col in skip:
#            continue
#
#        s=df[col]
#        col_type=s.dtype
#
#        if pd.api.types.is_datetime64_any_dtype(col_type) or pd.api.types.is_timedelta64_dtype(col_type) or isinstance(col_type, pd.CategoricalDtype):
#            continue
#
#        if pd.api.types.is_bool_dtype(col_type):
#            continue

#        elif pd.api.types.is_integer_dtype(col_type):
#            c_min=s.min()
#            c_max=s.max()
#
#            if np.iinfo(np.int8).min<=c_min<=c_max<=np.iinfo(np.int8).max:
#                df[col]=s.astype(np.int8)
#            elif np.iinfo(np.int16).min<=c_min<=c_max<=np.iinfo(np.int16).max:
#                df[col]=s.astype(np.int16)
#            elif np.iinfo(np.int32).min<=c_min<=c_max<=np.iinfo(np.int32).max:
#                df[col]=s.astype(np.int32)
#            else:
#                df[col]=s.astype(np.int64)

#        elif pd.api.types.is_float_dtype(col_type):
#            c_min=s.min()
#            c_max=s.max()

#            if np.finfo(np.float32).min<=c_min<=c_max<=np.finfo(np.float32).max:
#                df[col]=s.astype(np.float32)
#            else:
#                df[col]=s.astype(np.float64)
    
#    return df

#columns_drop=[
#    "Unnamed: 0",
#    "Flow ID",
#    " Source IP",
#    " Source Port",
#    " Destination IP",
#    " Destination Port",
#    " Timestamp",
#    " Bwd PSH Flags",
#    " Fwd URG Flags",
#    " Bwd URG Flags",
#    "FIN Flag Count",
#    " PSH Flag Count",
#    " ECE Flag Count",
#    "Fwd Avg Bytes/Bulk",
#    " Fwd Avg Packets/Bulk",
#    " Fwd Avg Bulk Rate",
#    " Bwd Avg Bytes/Bulk",
#    " Bwd Avg Packets/Bulk",
#    "Bwd Avg Bulk Rate",
#    " Fwd Header Length.1",
#    " Inbound",
#    "SimillarHTTP"
#]

#for file in tqdm(archivos_input):
#    nombre=os.path.basename(file)
#    print(f"Leyendo: {nombre}")

#    df=pd.read_csv(file,usecols=lambda column: column not in columns_drop)
#    print('\n',"---------------------------------------------------------",'\n')
#    #inicial_mem=df.memory_usage().sum()
#    #print("Uso inicial de memoria: ",inicial_mem,"MB")
#    df=df.replace([np.inf,-np.inf],np.nan)
#    df.dropna(inplace=True)
#    df=shrink_df(df,skip=[' Label'])
#    df=apply_schema(df,Schema)
#    pd.set_option('display.max_rows',None)
#    print(df.dtypes)
#    print('\n',"---------------------------------------------------------",'\n')

    #Columnas todo 0
    #print('\n',"---------------------------------------------------------",'\n')
    #columnas_cero=df.columns[(df==0).all()].tolist()
    #print(columnas_cero)
    #print('\n',"---------------------------------------------------------",'\n')

#Escribir cuantos de cada Label hay por cada doc
#archivos_input=glob.glob("/home/serg/Documentos/Proyecto/Files/Training/*.parquet")

#for file in tqdm(archivos_input):
#    if file != "/home/serg/Documentos/Proyecto/Files/Training/full.parquet":
#        df=pd.read_parquet(file)
#        print(file,':\n',df['LabelBin'].value_counts())

#print(df['LabelBin'].value_counts(),'\n')

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)

#file="C:/Users/sergi/Desktop/TFGSergioFernandezCamara/capturas/csv/captura_2026-05-14_16-55-12.pcap_Flow.csv"
file="C:/Users/sergi/Desktop/TFGSergioFernandezCamara/Files/Parquet/UDP.parquet"
#file="C:/Users/sergi/Desktop/TFGSergioFernandezCamara/Files/CSV-03-11/03-11/UDP.csv"
df=pd.read_parquet(file)

#Imprime todas las columnas
res=df.columns.to_list()
print("Lista de columnas:",'\n')
print(res)
print('\n',"Número de columnas:")
print(len(res))

#Escribir las primeras 100 líneas del doc
#for i in range(3):
#    res = df.iloc[[i]]
#    print(res, "\n")

#df = pd.read_csv(file, low_memory=False)

#for col, dtype in df.dtypes.items():
#    print(f"{col}: {dtype}")

#Comprobar valores enormes    
#df = pd.read_csv(file, low_memory=False)
#df.columns = df.columns.str.strip()

#res=df.columns.to_list()
#print("Lista de columnas:",'\n')
#print(res)
#print('\n',"Número de columnas:")
#print(len(res))

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

# Ver filas con idle sospechosamente grande
#suspicious_idle = df[
#    (df["Idle Mean"] > df["Flow Duration"]) |
#    (df["Idle Max"] > df["Flow Duration"]) |
#    (df["Idle Min"] > df["Flow Duration"])
#]

#print("Filas con idle sospechoso:", len(suspicious_idle))
#print(suspicious_idle[[
#    "Flow ID", "Flow Duration",
#    "Idle Mean", "Idle Std", "Idle Max", "Idle Min"
#]].head(20))