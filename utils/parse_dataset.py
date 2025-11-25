from pathlib import Path
import ijson
import sys

def procesar_archivo(ruta_json):
    """
    Lee un JSON muy grande (array de objetos) usando streaming con ijson.
    Devuelve un generador que produce [titulo, resumen, transcripcion] por registro.
    """
    ruta = Path(ruta_json)
    if not ruta.exists():
        print(f"Archivo no encontrado: {ruta}")
        sys.exit(1)

    print(f"Procesando dataset: {ruta} ...")

    with ruta.open("r", encoding="utf-8") as f:
        for i, registro in enumerate(ijson.items(f, "item"), start=1):
            title = registro.get("title", "")
            summary = registro.get("summary", "")
            transcript = registro.get("utt") or registro.get("transcript") or ""
            yield [title, summary, transcript]

            if i % 10000 == 0:
                print(f"Procesadas {i:,} entrevistas...")

    print("Lectura del dataset completada.")
