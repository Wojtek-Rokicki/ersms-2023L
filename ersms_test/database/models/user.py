from sqlalchemy import Column, Integer, String

from ersms_test.database.models.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(63), unique=True)
