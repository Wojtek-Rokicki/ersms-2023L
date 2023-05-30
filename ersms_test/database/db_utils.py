from contextlib import contextmanager
from typing import Generator

from sqlalchemy.orm import Session

from .database import db_session


@contextmanager
def db_session_get() -> Generator[Session, None, None]:
    try:
        yield db_session
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e
