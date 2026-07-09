import os
import time

db_file = "gestrasing.db"

if os.path.exists(db_file):
    try:
        os.remove(db_file)
        print(f"✅ {db_file} eliminado con éxito.")
    except PermissionError:
        print(f"❌ No se pudo borrar {db_file}. Está bloqueado por otro programa.")
else:
    print("ℹ️ El archivo no existe, la pista está limpia.")