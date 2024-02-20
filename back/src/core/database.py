from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import sqlalchemy_settings

engine = create_engine(
    sqlalchemy_settings.sqlalchemy_database_url.format(
        DATABASE=sqlalchemy_settings.database,
    ),
    pool_size=sqlalchemy_settings.sqlalchemy_pool_size,
    pool_recycle=sqlalchemy_settings.sqlalchemy_pool_recycle,
    pool_timeout=sqlalchemy_settings.sqlalchemy_pool_timeout,
    echo=sqlalchemy_settings.sqlalchemy_echo,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_database_session():
    """ sqlalchemy Session generator """
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
