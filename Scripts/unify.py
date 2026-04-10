import pyarrow as pa
import pyarrow.csv as pc
import pyarrow.parquet as pp
import pyarrow.dataset as ds
import glob
from tqdm import tqdm
import gc

file=("/home/serg/Documentos/Proyecto/Files/CSV-01-12/01-12/DrDoS_DNS.csv")
#for file in tqdm(archivos_input):    
print(f"Leyendo: {file}")

table_str=pc.read_csv(file,read_options=pc.ReadOptions(
    autogenerate_column_names=False))
columnas=table_str.column_names
del table_str
convert_options=pc.ConvertOptions(
    column_types={col: pa.string() for col in columnas})

reader=pc.open_csv(file,read_options=pc.ReadOptions(block_size=10_000_000),
                                    convert_options=convert_options)

#reader=pc.open_csv(file,read_options=pc.ReadOptions(block_size=10_000_000))

for batch in reader:
    table=pa.Table.from_batches([batch])

    clean_names=[name.strip() for name in table.column_names]
    table=table.rename_columns(clean_names)

    columns_drop=[
        "Unnamed: 0",
        "Flow ID",
        "Source IP",
        "Source Port",
        "Destination IP",
        "Destination Port",
        "Timestamp",
        "SimillarHTTP"
    ]

    columns_keep=[col for col in table.column_names if col not in columns_drop]
    table=table.select(columns_keep)

    columnas_no_num=["Label"]
    arrays_convertidos=[]
    nombres=[]

    for col_name in table.column_names:
        col=table[col_name]
        if col_name in columnas_no_num:
            arrays_convertidos.append(col)
            nombres.append(col_name)
            continue

        try:
            col_num=pa.compute.cast(col,pa.float64(),safe=False)
        except:
            arrays_convertidos.append(col)
            nombres.append(col_name)
            continue

        arrays_convertidos.append(col_num)
        nombres.append(col_name)

    mask=None
    for col in table.column_names:
        column=table[col]
        valid=pa.compute.is_valid(column)

        if pa.types.is_floating(column.type) or pa.types.is_integer(column.type):
            finite=pa.compute.is_finite(column)
            valid=pa.compute.and_(valid,finite)
            
        if mask is None:
            mask=valid
        else:
            mask=pa.compute.and_(mask,valid)

    table=table.filter(mask)

    contador=0
    ds.write_dataset(
        table,
        "savedir",
        format="parquet",
        partitioning=ds.partitioning(pa.schema([table.schema.field("Label")])),
        existing_data_behavior="overwrite_or_ignore",
        basename_template=f"part-{contador}-{{i}}.parquet"
    )

    del table
    del mask
    del columns_drop
    del columns_keep
    del clean_names
    gc.collect()

print("Conversión completada")