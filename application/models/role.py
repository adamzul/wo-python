from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship, backref

from application.models.base import Base

class Role(Base):
	__tablename__ = 'role'
	id=Column(Integer, primary_key=True)
	role=Column('role', String(30))
	waktu_insert=Column('waktu_insert', DateTime)
	waktu_insert=Column('waktu_insert', DateTime)

	# user = relationship("User")