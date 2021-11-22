from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from psycopg2 import sql
from tools.token_tools import create_token

from tools.logging import logger

import simplejson as json

def handle_request():
	logger.debug("Buy Book Handle Request")
	
	cur = g.db.cursor()
	form = request.form
	book_id = request.form.get('book_id')
	user_id = request.form.get('user_id')
	
	decoded = jwt.decode(form["jwt"], SECRET, algorithms=["HS256"])
	try:
		# clean up query
		query = sql.SQL("insert into {table} ({fieldOne}, {fieldTwo}, {fieldThree}) values (%s, %s, current_timestamp);").format(
			table = sql.Identifier('purchases'),
			fieldOne = sql.Identifier('user_id'),
			fieldTwo = sql.Identifier('book_id'),
			fieldThree = sql.Identifier('purchased_on')
		)
		
		cur.execute(query, user_id, book_id)
		db.commit();
		print("Purchased saved into database.")
		
		return json_response(message = "Book purchased successfully.", token = create_token(g.jwt_data), authenticated = True)
	except:
		return json_response(message = "Error while writing to database.", status = 500, create_token(user), authenticated = True)