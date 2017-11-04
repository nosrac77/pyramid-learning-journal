from sqlalchemy import (
    Column,
    Unicode,
    Integer
)

from .meta import Base


class Entry(Base):
    """Create an instance of the Entry class, which is a model object used to
    fill Postgres database."""

    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    body = Column(Unicode)
    creation_date = Column(Unicode)

    def __repr__(self):
        return '<Entry: {}>.format(self.title)'
