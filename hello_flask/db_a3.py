import psycopg2

def get_db():
	return psycopg2.connect(host="localhost", dbname="books", user="root", password="root")

def get_db_instance():  
    db = get_db()
    cur = db.cursor()
	
	return db, cur