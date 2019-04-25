from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship, backref

from application.models.base import Base

class Divisi(Base):
	__tablename__ = 'divisi'
	id=Column(Integer, primary_key=True)
	divisi=Column('divisi', String(30))
	waktu_insert=Column('waktu_insert', DateTime)
	waktu_insert=Column('waktu_insert', DateTime)

	user = relationship("User")
