from flask import (
		Blueprint, flash, g, redirect, render_template, request, url_for
)

import json
from werkzeug.exceptions import abort

from application.auth import login_required
from application.db import get_db

# import application.models.user_table as user_table 
# import application.models.role_table as role_table 
from sqlalchemy import create_engine

from datetime import date
import hashlib 

from application.models.user import User
from application.models.role import Role
from application.models.divisi import Divisi
from application.models.base import Session_db, engine, Base

from pprint import pprint
from inspect import getmembers
class User_BP():
	bp = Blueprint('user', __name__)
	table_field = ['id', "getattr(role, id)", 'username', 'divisi', 'nama']

	# def __init__(self):
	# 	self.bp = Blueprint('user', __name__)

	@bp.route('/')
	@login_required
	def index():
		Base.metadata.create_all(engine)
		session = Session_db()
		role = session.query(Role).all()
		divisi = session.query(Divisi).all()
		return render_template('user/user.index.html', role = role, divisi = divisi)

	@bp.route('/get_data', methods=['POST'])
	def get_data():
		# engine = create_engine('mysql+pymysql://root:@localhost/wo')
		# mysql_data = user_table.get_all()
		Base.metadata.create_all(engine)
		session = Session_db()
		mysql_data = session.query(User).join(Role, Divisi).all()
		data = []
		for x in mysql_data:
			row = []
			# row.append(x.username)
			# for attr, value in mysql_data.__dict__.items():
			# 	print(attr, value)
			# for y in table_field:
				# row.append(getattr(x, y))
			row.append(getattr(x, 'id'))
			row.append(getattr(x, 'username'))
			row.append(getattr(getattr(x, 'role'), 'role'))
			row.append(getattr(getattr(x, 'divisi'), 'divisi'))
			row.append(getattr(x, 'nama'))
			row.append(("""<a class="btn btn-sm btn-primary" href="javascript:void(0)" title="Edit" onclick="edit_data('"""+ str(getattr(x, 'id')) +"""')"><i class="glyphicon glyphicon-pencil"></i> Edit</a>
						<a class="btn btn-sm btn-danger" href="javascript:void(0)" title="Hapus" onclick="delete_data('"""+ str(getattr(x, 'id')) +"""')"><i class="glyphicon glyphicon-trash"></i> Delete</a>"""))
			temp = getattr(x, 'role')
			pprint(temp.__dict__)
			data.append(row)

		return json.dumps({"data":data, "recordsFiltered": len(data)})

	@bp.route('/edit/<id>', methods = ['GET'])
	@login_required
	def edit(id):
		Base.metadata.create_all(engine)
		session = Session_db()
		user = session.query(User).filter_by(id=id).first()
		# pprint(user.__dict__)
		data = user.__dict__
		data.pop('_sa_instance_state')
		data['waktu_insert'] = data['waktu_insert'].strftime("%Y-%m-%d %H:%M:%S")
		data['waktu_update'] = data['waktu_update'].strftime("%Y-%m-%d %H:%M:%S")
		pprint(data)
		return json.dumps(data)
		# return ""

	@bp.route('/create', methods=('GET', 'POST'))
	@login_required
	def create():
		if request.method == 'POST':
			Base.metadata.create_all(engine)
			session = Session_db()
			username = request.form['username']
			password =  hashlib.sha256(request.form['password'].encode()) 
			password = password.hexdigest()
			role = request.form['role']
			divisi = request.form['divisi']
			nama = request.form['nama']
			error = None

			temp = User(username, password, role, divisi, nama)

			session.add(temp)

			session.commit()
			session.close()
			# if not title:
			# 	error = 'Title is required.'

			# if error is not None:
			# 	flash(error)
			# else:
			# 	db = get_db()
			# 	db.execute(
			# 		'INSERT INTO post (title, body, author_id)'
			# 		' VALUES (?, ?, ?)',
			# 		(title, body, g.user['id'])
			# 	)
			# 	db.commit()
			return json.dumps({"status":True})


	def get_post(id, check_author=True):
		post = get_db().execute(
			'SELECT p.id, title, body, created, author_id, username'
			' FROM post p JOIN user u ON p.author_id = u.id'
			' WHERE p.id = ?',
			(id,)
		).fetchone()

		if post is None:
			abort(404, "Post id {0} doesn't exist.".format(id))

		if check_author and post['author_id'] != g.user['id']:
			abort(403)

		return post

	@bp.route('/update', methods = ['POST'])
	@login_required
	def update():
		# post = get_post(id)


		Base.metadata.create_all(engine)
		session = Session_db()
		id = request.form['id']

		user = session.query(User).filter_by(id=id).first()

		user.username = request.form['username']
		user.password = request.form['password']
		user.role_id = request.form['role']
		user.divisi_id = request.form['divisi']
		user.nama = request.form['nama']

		# error = None

		# # session.query().\
		# # 	filter(User.username == form.username.data).\
		# # 	update({"no_of_logins": (User.no_of_logins +1)})
		session.commit()
		
		return json.dumps({"status": True})


	@bp.route('/delete/<int:id>')
	@login_required
	def delete(id):
		Base.metadata.create_all(engine)
		session = Session_db()
		session.query(User).filter_by(id = id).delete()
		session.commit()
		return json.dumps({"status": True})