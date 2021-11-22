from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from psycopg2 import sql
from tools.token_tools import create_token

from tools.logging import logger

import simplejson as json

def handle_request():
	logger.debug("Get Books Handle Request")
	cur = g.db.cursor()
	
	query = sql.SQL("select * from {table};").format(
		table = sql.Identifier('books')
	)
	
	cur.execute(query)
	db_books = cur.fetchall()
	
	return json_response(token = create_token(g.jwt_data), books = db_books)