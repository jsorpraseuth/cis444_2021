from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from psycopg2 import sql
from tools.token_tools import create_token

from tools.logging import logger

import bcrypt

def handle_request():
	logger.debug("SignUp Handle Request")
	db = g.db
	cur = db.cursor()
	form = request.form
	
	password_from_user_form = request.form['password']
	user = {
		"sub" : request.form['username'] # sub is used by pyJwt as the owner of the token
	}
	
	# clean query to desired format
	query = sql.SQL("select {field} from {table} where {key} = %s;").format(
		field = sql.Identifier('username'),
		table = sql.Identifier('users'),
		key = sql.Identifer('username'))
	)
		
	# check if user exists
	cur.execute(query, (user['sub']))
	row = cur.fetchone()
	
	# if username is available, create credentials
	if row is None:
		# encrypt the password
		encrypted_pass = bcrypt.hashpw(bytes(password_from_user_form), 'utf-8'), bcrypt.gensalt(11))
		# clean insert
		query = sql.SQL("insert into {table} ({fieldOne}, {fieldTwo}) values (%s, %s);").format(
			table = sql.Identifer('users'),
			fieldOne = sql.Identifier('username')
			fieldTwo = sql.Identifier('password')
		)
		
		cur.execute(query, (user['sub'], encrypted_pass.decode('utf-8')))
		# important commit created user to db
		db.commit()
		
		print('User "' + form['username'] + '" created successfully.')
		return json_response(data = {"message" : "User account created successfully."}, token = create_token(user), authenticated = True)
	else:
		print('Error: "' + form['username'] + '" already in use.')
		return json_response(data = {"message" : "Username is already in use."}, status = 404, authenticated = False)

