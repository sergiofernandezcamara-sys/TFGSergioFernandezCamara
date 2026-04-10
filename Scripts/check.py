import pandas as pd
import glob
from tqdm import tqdm

#archivos_input=(
#    glob.glob("/home/serg/Documentos/Proyecto/Files/CSV-01-12/01-12/*.csv") + 
#    glob.glob("/home/serg/Documentos/Proyecto/Files/CSV-03-11/03-11/*.csv")
#)
#for file in tqdm(archivos_input):
#    df=pd.read_csv(file)
#    print(file,':\n',df[' Label'].value_counts())

#print(df[' Label'].value_counts(),'\n')

file="/home/serg/Documentos/Proyecto/Files/Parquet/UDP.parquet"
df=pd.read_parquet(file)

for i in range(101):
    row = [i]
    print(df.loc[df.index[row]],'\n')
    