import psycopg2

def get_db():
	return psycopg2.connect(host="localhost", dbname="books", user="root", password="root")