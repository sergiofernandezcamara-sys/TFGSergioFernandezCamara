import pandas as pd
import numpy as np
import glob
import os
from tqdm import tqdm
#from fastai.tabular.all import df_shrink

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

#columns_drop=[
#    "Unnamed: 0",
#    "Flow ID",
#    " Source IP",
#    " Source Port",
#    " Destination IP",
#    " Destination Port",
#    " Timestamp",
#    " Fwd Header Length.1",
#    " Inbound",
#    "SimillarHTTP"
#]

#for file in tqdm(archivos_input):
#    nombre=os.path.basename(file)
#    print(f"Leyendo: {nombre}")
#
#    df=pd.read_csv(file,usecols=lambda column: column not in columns_drop)
#    print('\n',"---------------------------------------------------------",'\n')
#    #inicial_mem=df.memory_usage().sum()
#    #print("Uso inicial de memoria: ",inicial_mem,"MB")
#    df.dropna(inplace=True)
#    df=df_shrink(df,obj2cat=False,skip=[' Label'])
#    df=apply_schema(df,Schema)
#    pd.set_option('display.max_rows',None)
#    print(df.dtypes)
#    print('\n',"---------------------------------------------------------",'\n')

    #Columnas todo 0
    #print('\n',"---------------------------------------------------------",'\n')
    #columnas_cero=df.columns[(df==0).all()].tolist()
    #print(columnas_cero)
    #print('\n',"---------------------------------------------------------",'\n')



#archivos_input=(
#    glob.glob("/home/serg/Documentos/Proyecto/Files/CSV-01-12/01-12/*.csv") + 
#    glob.glob("/home/serg/Documentos/Proyecto/Files/CSV-03-11/03-11/*.csv")
#)
#Escribir cuantos de cada Label hay por cada doc
archivos_input=glob.glob("/home/serg/Documentos/Proyecto/Files/Training/*.parquet")

for file in tqdm(archivos_input):
    if file != "/home/serg/Documentos/Proyecto/Files/Training/full.parquet":
        df=pd.read_parquet(file)
        print(file,':\n',df['LabelBin'].value_counts())

#print(df['LabelBin'].value_counts(),'\n')

#file="/home/serg/Documentos/Proyecto/Files/Training/train.parquet"
#df=pd.read_parquet(file)

#Imprime todas las columnas
#res=df.columns.to_list()
#print("Lista de columnas:",'\n')
#print(res)
#print('\n',"Número de columnas:")
#print(len(res))

#Escribir las primeras 100 líneas del doc
#for i in range(101):
#    row = [i]
#    print(df.loc[df.index[row]],'\n')
    