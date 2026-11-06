import pandas as pd
from etl import transformar


def datos_crudos():
    return pd.DataFrame({
        "id_venta": [1, 2, 2, None],
        "fecha": ["2026-01-05"] * 4,
        "monto": ["100.5", "-20", "-20", "50"],
    })


def test_sin_duplicados_ni_nulos():
    df = transformar(datos_crudos())
    assert df["id_venta"].is_unique
    assert df["id_venta"].notna().all()


def test_montos_positivos():
    df = transformar(datos_crudos())
    assert (df["monto"] > 0).all()


# Reto 1: prueba para fechas futuras
def test_rechaza_fechas_futuras():
    df = pd.DataFrame({
        "id_venta": [1, 2],
        "fecha": ["2026-01-05", "2999-01-01"],
        "monto": ["10", "20"],
    })
    resultado = transformar(df)
    assert list(resultado["id_venta"]) == [1]
