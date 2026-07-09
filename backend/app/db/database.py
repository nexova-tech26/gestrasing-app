"""
database.py
===========
Configuración central de la base de datos para la API Gestrasing.

Este módulo establece la conexión con MySQL mediante SQLAlchemy,
exponiendo los tres objetos esenciales que el resto de la aplicación
consume:

- ``engine``       — Motor de conexión a la base de datos.
- ``SessionLocal`` — Fábrica de sesiones para operaciones CRUD.
- ``Base``         — Clase base para definir los modelos ORM.

Variables de entorno requeridas (.env):
    DB_USER:     Usuario de la base de datos.
    DB_PASSWORD: Contraseña del usuario.
    DB_HOST:     Host o IP del servidor MySQL.
    DB_PORT:     Puerto de conexión (por defecto MySQL usa 3306).
    DB_NAME:     Nombre de la base de datos.

Uso típico en un endpoint::

    from database import SessionLocal

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# ---------------------------------------------------------------------------
# Carga de variables de entorno
# ---------------------------------------------------------------------------

# Carga las variables definidas en el archivo .env al entorno del proceso.
# Debe ejecutarse antes de cualquier llamada a os.getenv().
load_dotenv()


# ---------------------------------------------------------------------------
# Credenciales y parámetros de conexión
# ---------------------------------------------------------------------------

# Cada variable se lee del entorno para evitar credenciales en el código fuente.
# Si alguna es None, SQLAlchemy lanzará un error descriptivo al conectar.
DB_USER: str | None = os.getenv("DB_USER")
DB_PASSWORD: str | None = os.getenv("DB_PASSWORD")
DB_HOST: str | None = os.getenv("DB_HOST")
DB_PORT: str | None = os.getenv("DB_PORT")       # MySQL por defecto: 3306
DB_NAME: str | None = os.getenv("DB_NAME")


# ---------------------------------------------------------------------------
# URL de conexión
# ---------------------------------------------------------------------------

# Formato estándar de SQLAlchemy para MySQL con el driver PyMySQL:
# mysql+pymysql://<usuario>:<contraseña>@<host>:<puerto>/<base_de_datos>
#
# PyMySQL es un driver puro de Python; no requiere instalación de cliente MySQL.
# Alternativa con driver nativo: mysql+mysqlconnector://...
SQLALCHEMY_DATABASE_URL: str = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# ---------------------------------------------------------------------------
# Motor de base de datos (Engine)
# ---------------------------------------------------------------------------

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # echo=True,  # Descomentar en desarrollo para imprimir SQL generado en consola.
    # pool_pre_ping=True,  # Recomendado en producción: valida la conexión antes de usarla.
)
"""Engine: Motor principal de SQLAlchemy.

Gestiona el pool de conexiones y traduce las operaciones ORM a SQL.
Es un objeto pesado — debe crearse una sola vez por proceso.
"""


# ---------------------------------------------------------------------------
# Fábrica de sesiones (SessionLocal)
# ---------------------------------------------------------------------------

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,   # Las transacciones deben confirmarse explícitamente con .commit().
    autoflush=False,    # Los cambios no se envían a la BD hasta llamar a .flush() o .commit().
)
"""sessionmaker: Fábrica que genera nuevas sesiones de base de datos.

Cada sesión representa una unidad de trabajo (transaction).
Se recomienda crear una sesión por request y cerrarla al finalizar:

    db = SessionLocal()
    try:
        # operaciones...
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
"""


# ---------------------------------------------------------------------------
# Clase base para modelos ORM
# ---------------------------------------------------------------------------

Base = declarative_base()
"""DeclarativeMeta: Clase base de la que heredan todos los modelos ORM.

Centraliza el registro de tablas y permite operaciones globales como::

    Base.metadata.create_all(bind=engine)  # Crea todas las tablas definidas.
    Base.metadata.drop_all(bind=engine)    # Elimina todas las tablas (¡cuidado en producción!).

Ejemplo de modelo::

    from database import Base

    class Usuario(Base):
        __tablename__ = "usuarios"

        id = Column(Integer, primary_key=True, index=True)
        nombre = Column(String(100), nullable=False)
"""