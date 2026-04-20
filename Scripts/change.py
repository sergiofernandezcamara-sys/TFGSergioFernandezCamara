import pandas as pd
import numpy as np
import glob
import os
from tqdm import tqdm

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

def shrink_df(df: pd.DataFrame,skip=None)->pd.DataFrame:

    if skip is None:
        skip=set()
    elif isinstance(skip,str):
        skip={skip}
    else:
        skip=set(skip)
    
    for col in df.columns:
        if col in skip:
            continue

        s=df[col]
        col_type=s.dtype

        if pd.api.types.is_datetime64_any_dtype(col_type) or pd.api.types.is_timedelta64_dtype(col_type) or pd.api.types.is_categorical_dtype(col_type):
            continue

        if pd.api.types.is_bool_dtype(col_type):
            continue

        elif pd.api.types.is_integer_dtype(col_type):
            c_min=s.min()
            c_max=s.max()

            if np.iinfo(np.int8).min<=c_min<=c_max<=np.iinfo(np.int8).max:
                df[col]=s.astype(np.int8)
            elif np.iinfo(np.int16).min<=c_min<=c_max<=np.iinfo(np.int16).max:
                df[col]=s.astype(np.int16)
            elif np.iinfo(np.int32).min<=c_min<=c_max<=np.iinfo(np.int32).max:
                df[col]=s.astype(np.int32)
            else:
                df[col]=s.astype(np.int64)

        elif pd.api.types.is_float_dtype(col_type):
            c_min=s.min()
            c_max=s.max()

            if np.finfo(np.float32).min<=c_min<=c_max<=np.finfo(np.float32).max:
                df[col]=s.astype(np.float32)
            else:
                df[col]=s.astype(np.float64)
    
    return df

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
    df=shrink_df(df,skip=[' Label'])
    df=apply_schema(df,Schema)
    df.drop_duplicates(inplace=True)
    #final_mem=df.memory_usage().sum()
    #print("Uso final de memoria: ",final_mem,"MB")

    basename=nombre.split('.')[0]
    df.to_parquet(f"/home/serg/Documentos/Proyecto/Files/Parquet/{basename}.parquet")
    print(file,':\n',df[' Label'].value_counts())