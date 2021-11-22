from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
	logger.debug("Login Handle Request")
	db = g.db
	cur = db.cursor()
	form = request.form

    password_from_user_form = request.form['password']
    user = {
            "sub" : request.form['username'] # sub is used by pyJwt as the owner of the token
            }

	# clean query to desired format
	query = sql.SQL("select * from {table} where {key} = %s;").format(
		table = sql.Indentifer('users'),
		key = sql.Indentifer('username')
	)
	
	# check if user exists
	cur.execute(query, (user['sub']))
	row = cur.fetchone()
    if not row:
        print("Username '" + form["username"] + "' is invalid.")
		return json_response(data = {"message" : "Username '" + form["username"] + "' does not exist."}, status = 404, authenticated = False)
	# username exists, check password
	else:
		cur.execute(query, (user['sub']))
		# get password from db
		user_hashed_password = cur.fetchone()[2]
		
		if bcrypt.checkpw(bytes(password_from_user_form, "utf-8"), bytes(user_hashed_password, "utf-8")) == True:
			print("Login by '" + form["username"] + "' authorized.")
			# update last login by user
			query = sql.SQL("update {table} set last_login = current_timestamp where {key} = %s;").format(
				table = sql.Indentifer('users'),
				key = sql.Indentifer('username')
			)
			
			cur.execute(query, (user['sub']))
			db.commit();
			
			# user login authenticated, create token for user
			return json_response( token = create_token(user) , authenticated = True)
		else:
			print("Incorrect password.")
			return json_response(data = {"message" : "Incorrect password."}, status = 404, authenticated = False)
