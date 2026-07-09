# backend/app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexión (SQLite creará un archivo llamado gestrasing.db en la raíz del backend)
SQLALCHEMY_DATABASE_URL = "sqlite:///./gestrasing.db"

# Configuramos el motor. El parámetro check_same_thread es necesario solo para SQLite en FastAPI.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Creamos la fábrica de sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la que heredarán todos nuestros modelos de base de datos
Base = declarative_base()

def get_db():
    """
    Dependencia (Dependency Injection) para gestionar el ciclo de vida de la base de datos.
    Abre una conexión cuando llega una petición y la cierra cuando termina.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()