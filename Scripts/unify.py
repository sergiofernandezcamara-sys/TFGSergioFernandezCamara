import pyarrow as pa
import pyarrow.csv as pc
import pyarrow.parquet as pp
import glob
from tqdm import tqdm

archivos_input=(
    glob.glob("/home/sfk/Documents/Proyecto/Files/CSV-01-12/01-12/*.csv") + 
    glob.glob("/home/sfk/Documents/Proyecto/Files/CSV-03-11/03-11/*.csv")
)
carpeta_output="/home/sfk/Documents/Proyecto/Dataset/Parquet"

for file in tqdm(archivos_input):
    print(f"Leyendo: {file}")

    table=pc.read_csv(file)

    columns_drop=[
        "Unnamed: 0",
        "Flow ID",
        "Source IP",
        "Source Port",
        "Destination IP",
        "Destination Port",
        "Timestamp",
        "Similar HTTP"
    ]

    existing_drop=[col for col in columns_drop if col in table.column_names]
    table=table.drop(existing_drop)

    for i in table.column_names:
        print(f"Columna: {i}")

    ##pp.write_to_dataset(
    ##    table,
    ##    root_path=carpeta_output,
    ##    partition_cols=["Label"]
    ##)

print("Conversión completada")