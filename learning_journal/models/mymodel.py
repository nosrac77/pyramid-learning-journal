from sqlalchemy import (
    Column,
    String,
    Integer
)

from .meta import Base


class Entry(Base):
    """Create an instance of the Entry class, which is a model object used to
    fill Postgres database."""

    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(String(convert_unicode=True))
    body = Column(String(convert_unicode=True))
    creation_date = Column(String(convert_unicode=True))

    def __repr__(self):
        return '<Entry: {}>.format(self.title)'
