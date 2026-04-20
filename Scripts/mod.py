import pandas as pd

df=pd.read_parquet("/home/serg/Documentos/Proyecto/Files/Parquet/DrDoS_UDP.parquet")

df[' Label']=df[' Label'].replace("DrDoS_UDP","UDP")

df.to_parquet("/home/serg/Documentos/Proyecto/Files/Parquet/DrDoS_UDP.parquet")

#df=df.drop(df[df[" Label"].isin(["NetBIOS","UDPLag"])].index)

#df.to_parquet(f"/home/serg/Documentos/Proyecto/Files/Parquet/LDAP.parquet")