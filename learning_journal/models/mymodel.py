from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    Text,
    DateTime
)

from .meta import Base
from datetime import datetime


class Journal(Base):
    __tablename__ = 'journals'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    creation_date = Column(DateTime)
    body = Column(Text)

    def __init__(self, *args, **kwargs):
        """Modify instance of Journal class."""
        super(Journal, self).__init__(*args, **kwargs):
            self.creation_date = datetime.now()


# Index('my_index', MyModel.name, unique=True, mysql_length=255)
