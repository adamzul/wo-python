from application.db import get_db

def get_all():
	db = get_db()
	db.execute(
		"SELECT * "
		"FROM role"
	)

	return db.fetchall()
