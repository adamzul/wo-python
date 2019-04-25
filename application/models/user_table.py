from application.db import get_db

def get_all():
	db = get_db()
	db.execute(
		"SELECT a.id, a.username, b.role, c.divisi, a.nama "
		"FROM user a "
		"JOIN role b ON a.role = b.id "
		"JOIN divisi c ON a.divisi = c.id "
	)

	return db.fetchall()
