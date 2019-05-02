import functools

from flask import (
		Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import hashlib 

from flaskr.db import get_db

from application.models.user import User
from application.models.base import Session_db, engine, Base


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None

		if not username:
			error = 'Username is required.'
		elif not password:
			error = 'Password is required.'
		elif db.execute(
			'SELECT id FROM user WHERE username = ?', (username,)
		).fetchone() is not None:
			error = 'User {} is already registered.'.format(username)

		if error is None:
			db.execute(
				'INSERT INTO user (username, password) VALUES (?, ?)',
				(username, generate_password_hash(password))
			)
			db.commit()
			return redirect(url_for('auth.login'))

		flash(error)

	return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = hashlib.sha256(request.form['password'].encode()) 
		password = password.hexdigest()
		db = get_db()
		error = None
		Base.metadata.create_all(engine)
		session_db = Session_db()
		user = session_db.query(User).filter_by(username = username, password = password).first()

		if user is None:
			error = 'Incorrect username.'
		# elif not check_password_hash(user['password'], password):
			error = 'Incorrect password.'

		if error is None:
			session.clear()	
			session['user_id'] = user.id
			return redirect(url_for('index'))

		flash(error)

	return render_template('auth/auth.login.html')

@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		Base.metadata.create_all(engine)
		session_db = Session_db()
		g.user = session_db.query(User).filter_by(id = user_id).first()
		# g.user = get_db().execute(
		# 	'SELECT * FROM user WHERE id = ?', (user_id,)
		# ).fetchone()

@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))

def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))

		return view(**kwargs)

	return wrapped_view