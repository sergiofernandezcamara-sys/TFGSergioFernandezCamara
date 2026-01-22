import pandas as pd
import glob

archivos=(
    glob.glob("/home/sfk/Documents/Proyecto/Dataset/CSV-01-12/01-12/*.csv"),
    glob.glob("/home/sfk/Documents/Proyecto/Dataset/CSV-03-11/03-11/*.csv")
)

first=True
for f in archivos:
    for chunk in pd.read_csv(f,chunksize=500_000):
        chunk.to_csv(
            "output.csv",
            mode="w" if first else "a",
            index=False,
            header=first
        )
        first=False