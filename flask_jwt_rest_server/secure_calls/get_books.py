from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from psycopg2 import sql
from tools.token_tools import create_token

from tools.logging import logger

import simplejson as json

def handle_request():
	logger.debug("Get Books Handle Request")
	cur = g.db.cursor()	

	query = sql.SQL("select * from {table} where not exists (select from {table2} where books.book_id = purchases.book_id and username = test);").format(
		table = sql.Identifier('books'),
		table2 = sql.Identifier('purchases')
	)
	
	cur.execute(query)
	print("Grabbed books from database that were not purchased by user.")
	db_books = cur.fetchall()
	
	return json_response(token = create_token(g.jwt_data), books = db_books)