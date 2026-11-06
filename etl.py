import logging
import sqlite3

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("etl")


def extraer(ruta):
    return pd.read_csv(ruta)


def transformar(df):
    df = df.dropna(subset=["id_venta", "monto"])
    df = df.drop_duplicates(subset="id_venta").copy()
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["monto"] = df["monto"].astype(float)
    df = df[df["monto"] > 0]
    # Reto 1: rechazar ventas con fecha futura
    return df[df["fecha"] <= pd.Timestamp.today().normalize()]


def cargar(df, ruta_db):
    with sqlite3.connect(ruta_db) as con:
        df.to_sql("ventas", con, if_exists="replace", index=False)


def ejecutar(ruta_csv, ruta_db):
    crudo = extraer(ruta_csv)
    limpio = transformar(crudo)
    cargar(limpio, ruta_db)
    # Reto 2: filas leídas frente a filas cargadas
    log.info("Filas leídas: %d | Filas cargadas: %d | Descartadas: %d",
             len(crudo), len(limpio), len(crudo) - len(limpio))
    return limpio


if __name__ == "__main__":
    ejecutar("data/ventas.csv", "ventas.db")
