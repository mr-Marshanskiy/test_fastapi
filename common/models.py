import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime

from config.database import Base


class BaseIdModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class BaseCodeModel(Base):
    __abstract__ = True
    code = Column(String(31), primary_key=True)


class DateMixin(BaseIdModel):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
