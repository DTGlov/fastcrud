from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from .database import Base
from sqlalchemy.sql.expression import null


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    author = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
