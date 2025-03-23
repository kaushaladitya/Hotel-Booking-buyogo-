from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from dotenv import load_dotenv
from os import environ
from dataclasses import dataclass
import psycopg2

metadata = MetaData()
Base = declarative_base()

load_dotenv(dotenv_path=".env", override=True)
@dataclass
class DBEngine:
    load_dotenv(dotenv_path=".env", override=True)
    host_name: str = environ.get("hostIP")
    port: str = environ.get("port")
    username: str = environ.get("username")
    password: str = environ.get("password")
    database: str = environ.get("database")
    dialect: str = "postgresql"
    print(f'user==')
    @property
    def url(self):
        """Constructs and returns the database URL."""
        print((f'{self.dialect}://{self.username}:{self.password}@'
                f'{self.host_name}:{self.port}/{self.database}'))
        return (f'{self.dialect}://{self.username}:{self.password}@'
                f'{self.host_name}:{self.port}/{self.database}')

    @property
    def engine(self):
        """Creates and returns the SQLAlchemy engine."""
        return create_engine(self.url.replace("+asyncpg", ""))

DB_PARAMS = {
    'dbname': environ.get("DB_NAME", "hotel_management"),
    'user': environ.get("DB_USER", "postgres"),
    'password': environ.get("DB_PASSWORD", "admin"),
    'host': environ.get("DB_HOST", "127.0.0.1"),
    'port': environ.get("DB_PORT", "5432")
}

def get_db_connection():
    """
    Returns a synchronous psycopg2 connection to the database.
    """
    conn = psycopg2.connect(**DB_PARAMS)
    return conn

db_engine = DBEngine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine.engine)
DATABASE_URL = db_engine.url
database = Database(DATABASE_URL)
engine = db_engine.engine

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()