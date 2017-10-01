import sqlite3

from flask_restful import Resource, reqparse

class User:
	def __init__(self, _id, username, password):
		self.id = _id
		# id is a python keyword
		self.username = username
		self.password = password
	
	# find username from database by username
		# find the username from the database and create a user from that data.
	
	
	@classmethod
	def find_by_username(cls, username):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = "SELECT * FROM users WHERE username=?" # select all rows in the table users where 
		result = cursor.execute(query, (username,)) # execute the query on just the username (The username must be a tuple
		row = result.fetchone() # get the first row otherwise it returns None
		if row:
			user = User(row[0], row[1], row[2])
		else:
			user = None
		
		connection.close()
		return user
		
	@classmethod
	def find_by_id(cls, _id):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		
		query = "SELECT * FROM users WHERE id=?"
		result = cursor.execute(query,(_id,))
		row = result.fetchone()
		if row:
			user = User(row[0], row[1], row[2])
		else:
			user = None
			
		connection.close()
		return user
	
class UserRegister(Resource):
	
	parser = reqparse.RequestParser()
	parser.add_argument('username',
		required=True,
		type=str,
		help="This field cannot be left blank!"
	)
	
	parser.add_argument('password',
		required=True,
		type=str,
		help="This field cannot be left blank!"
	)
	
	def post(self):
		
		data = UserRegister.parser.parse_args()
		
		if User.find_by_username(data['username']):
			return {"message": "User already exists."}, 400
		
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		
		# must be NULL in order to use the auto-increment. Meaning you only need to pass 2 arguments
		query = "INSERT INTO users VALUES (NULL, ?, ?)"
		cursor.execute(query, (data['username'], data['password']))
		
		connection.commit()
		connection.close()
		
		return {"message": "User created successfully."}, 201