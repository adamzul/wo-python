import datetime 

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
# 
from application.models.base import Base

class User(Base):
	__tablename__ = 'user'
	id=Column(Integer, primary_key=True)
	username=Column('username', String(30))
	password=Column('password', String(30))
	role_id=Column('role', Integer, ForeignKey('role.id'))
	divisi_id=Column('divisi', Integer, ForeignKey('divisi.id'))
	nama=Column('nama', String(30))
	waktu_insert=Column('waktu_insert', DateTime)
	waktu_update=Column('waktu_update', DateTime)

	role=relationship("Role", foreign_keys=[role_id])
	divisi=relationship("Divisi", foreign_keys=[divisi_id])


	def __init__(self, username, password, role, divisi, nama):
		self.username = username
		self.password = password
		self.role_id = role
		self.divisi_id = divisi
		self.nama = nama
		self.waktu_insert = datetime.datetime.now()
		self.waktu_update = datetime.datetime.now()