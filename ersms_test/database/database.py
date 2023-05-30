from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from ersms_test.settings import Settings, get_config

settings: Settings = get_config()
metadata: MetaData = MetaData()
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_size=1, max_overflow=1)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
)

db_session = scoped_session(SessionLocal)
