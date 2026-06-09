import pandas as pd
import psycopg2

df = pd.read_csv("data/dataset.csv")
print("Dataset original")
print(df)

df = df.drop_duplicates()
df = df.fillna(0)
print("Dataset limpio")
print(df)

df.to_csv("output/dataset_limpio.csv", index=False)
print("Archivo exportado correctamente")

conn = psycopg2.connect(
    host="localhost",
    port=5433,
    database="laboratorio",
    user="admin",
    password="admin123"
)
cursor = conn.cursor()
print("Conexion PostgreSQL exitosa")

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INT,
    nombre VARCHAR(50),
    edad INT,
    ciudad VARCHAR(50)
)
""")
conn.commit()
print("Tabla creada correctamente")

cursor.execute("DELETE FROM clientes")
conn.commit()

for index, row in df.iterrows():
    cursor.execute(
        "INSERT INTO clientes (id, nombre, edad, ciudad) VALUES (%s, %s, %s, %s)",
        (int(row['id']), row['nombre'], int(float(row['edad'])), row['ciudad'])
    )
conn.commit()
print("Datos insertados correctamente")

cursor.execute("SELECT * FROM clientes")
resultado = cursor.fetchall()
print(f"Total registros: {len(resultado)}")
for fila in resultado:
    print(fila)

cursor.close()
conn.close()
print("Proceso finalizado correctamente")
