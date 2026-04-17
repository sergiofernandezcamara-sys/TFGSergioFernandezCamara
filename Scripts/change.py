import pandas as pd
import numpy as np
import glob
import os
from tqdm import tqdm
from fastai.tabular.all import df_shrink

archivos_input=(
    glob.glob("/home/serg/Documentos/Proyecto/Files/CSV-01-12/01-12/*.csv") + 
    glob.glob("/home/serg/Documentos/Proyecto/Files/CSV-03-11/03-11/*.csv")
)

Schema={
    " Total Fwd Packets" : "int32",
    " Fwd Header Length" : "int64",
    " Bwd Header Length" : "int64",
    "Subflow Fwd Packets" : "int32",
    " act_data_pkt_fwd" : "int16",
    " min_seg_size_forward" : "int32"
}

def apply_schema(df,schema):
    for col,dtype in schema.items():
        if col in df.columns:
            df[col]=df[col].astype(dtype)
    return df

columns_drop=[
    "Unnamed: 0",
    "Flow ID",
    " Source IP",
    " Source Port",
    " Destination IP",
    " Destination Port",
    " Timestamp",
    " Bwd PSH Flags",
    " Fwd URG Flags",
    " Bwd URG Flags",
    "FIN Flag Count",
    " PSH Flag Count",
    " ECE Flag Count",
    "Fwd Avg Bytes/Bulk",
    " Fwd Avg Packets/Bulk",
    " Fwd Avg Bulk Rate",
    " Bwd Avg Bytes/Bulk",
    " Bwd Avg Packets/Bulk",
    "Bwd Avg Bulk Rate",
    " Fwd Header Length.1",
    " Inbound",
    "SimillarHTTP"
]

for file in tqdm(archivos_input):
    nombre=os.path.basename(file)
    print(f"Leyendo: {nombre}")

    df=pd.read_csv(file,usecols=lambda column: column not in columns_drop)
    #inicial_mem=df.memory_usage().sum()
    #print("Uso inicial de memoria: ",inicial_mem,"MB")
    df.dropna(inplace=True)
    df=df_shrink(df,obj2cat=False,skip=[' Label'])
    df=apply_schema(df,Schema)
    df.drop_duplicates(inplace=True)
    #final_mem=df.memory_usage().sum()
    #print("Uso final de memoria: ",final_mem,"MB")

    basename=nombre.split('.')[0]
    df.to_parquet(f"/home/serg/Documentos/Proyecto/Files/Parquet/{basename}.parquet")
    print(file,':\n',df[' Label'].value_counts())