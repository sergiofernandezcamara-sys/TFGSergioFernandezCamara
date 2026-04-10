import pandas as pd
import numpy as np
import glob
import os
from tqdm import tqdm

archivos_input=(
    glob.glob("/home/serg/Documentos/Proyecto/Files/CSV-01-12/01-12/*.csv") + 
    glob.glob("/home/serg/Documentos/Proyecto/Files/CSV-03-11/03-11/*.csv")
)

columns_drop=[
    "Unnamed: 0",
    "Flow ID",
    " Source IP",
    " Source Port",
    " Destination IP",
    " Destination Port",
    " Timestamp",
    "SimillarHTTP"
]

for file in tqdm(archivos_input):
    nombre=os.path.basename(file)
    print(f"Leyendo: {nombre}")

    df=pd.read_csv(file,usecols=lambda column: column not in columns_drop)
    #inicial_mem=df.memory_usage().sum()
    #print("Uso inicial de memoria: ",inicial_mem,"MB")
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    #df=df.apply(lambda x: x.astype("float32") if np.issubdtype(x.dtype,np.floating) else x)
    #df=df.apply(lambda x: x.astype("int32") if np.issubdtype(x.dtype,np.integer) else x)
    #final_mem=df.memory_usage().sum()
    #print("Uso final de memoria: ",final_mem,"MB")

    basename=nombre.split('.')[0]
    df.to_parquet(f"/home/serg/Documentos/Proyecto/Files/Parquet/{basename}.parquet")
    print(file,':\n',df[' Label'].value_counts())