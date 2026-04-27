import glob
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils import resample

#########################################
#Dataframe
#########################################
rutas=glob.glob("/home/serg/Documentos/Proyecto/Files/Parquet/*.parquet")
dfs=[pd.read_parquet(r) for r in rutas]
df=pd.concat(dfs,ignore_index=True)

#########################################
#Resample
#########################################
UDP_df=df[df[" Label"]=="UDP"]
LDAP_df=df[df[" Label"]=="LDAP"]
MSSQL_df=df[df[" Label"]=="MSSQL"]
Syn_df=df[df[" Label"]=="Syn"]
Benign_df=df[df[" Label"]=="BENIGN"]

n_objetivo=20000

UDP_bal=resample(UDP_df,replace=False,n_samples=n_objetivo,random_state=42)
LDAP_bal=resample(LDAP_df,replace=False,n_samples=n_objetivo,random_state=42)
MSSQL_bal=resample(MSSQL_df,replace=False,n_samples=n_objetivo,random_state=42)
Syn_bal=resample(Syn_df,replace=False,n_samples=n_objetivo,random_state=42)
df=pd.concat([UDP_bal,LDAP_bal,MSSQL_bal,Syn_bal,Benign_df],ignore_index=True)

df.to_parquet(f"/home/serg/Documentos/Proyecto/Files/Training/full.parquet")

#########################################
#Label Encode
#########################################
df["LabelBin"]=(df[" Label"]!="BENIGN").astype("int32")
df=df.drop(columns=[" Label"])

#########################################
#Divide Train, Val y Test
#########################################
x=df.drop(columns=["LabelBin"])
y=df["LabelBin"]

x_train,x_temp,y_train,y_temp=train_test_split(
    x,y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

x_val,x_test,y_val,y_test=train_test_split(
    x_temp,y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)

print("Train:",x_train.shape,y_train.shape)
print("Validation:",x_val.shape,y_val.shape)
print("Test:",x_test.shape,y_test.shape)

#########################################
#To Parquet
#########################################
train_df=x_train.copy()
train_df["LabelBin"]=y_train.copy()

train_df=train_df.sample(frac=1,random_state=42).reset_index(drop=True)

val_df=x_val.copy()
val_df["LabelBin"]=y_val.copy()

test_df=x_test.copy()
test_df["LabelBin"]=y_test.copy()

train_df.to_parquet(f"/home/serg/Documentos/Proyecto/Files/Training/train.parquet")
val_df.to_parquet(f"/home/serg/Documentos/Proyecto/Files/Training/val.parquet")
test_df.to_parquet(f"/home/serg/Documentos/Proyecto/Files/Training/test.parquet")

# 8) Compilar
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

# 9) Guardar el mejor modelo durante entrenamiento
checkpoint_cb = keras.callbacks.ModelCheckpoint(
    filepath="mejor_modelo.keras",
    monitor="val_loss",
    mode="min",
    save_best_only=True
)

callbacks = [
    keras.callbacks.EarlyStopping(
        monitor="val_loss",
        min_delta=1e-2,
        patience=2,
        verbose=1,
    ),
    keras.callbacks.ModelCheckpoint(
        filepath="mejor_modelo.keras",
        monitor="val_loss",
        mode="min",
        save_best_only=True
    )
]

# 10) Entrenar
history = model.fit(
    X_train_bal,
    y_train_bal,
    epochs=20,
    batch_size=256,
    validation_data=(X_val, y_val),
    callbacks=[checkpoint_cb]
)

# 11) Evaluación final
test_loss, test_acc = model.evaluate(X_test, y_test)
print("Test loss:", test_loss)
print("Test acc:", test_acc)

# 12) Guardar también el modelo final
model.save("modelo_final.keras")