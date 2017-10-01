from user import User
from werkzeug.security import safe_str_cmp

# MAKESHIFT DATABASE

# table of users
#	users = [
# 		{
#			'id': 1,
#			'username':'bob',
#			'password': 'asdf'
#		}
#	]

users = [
	User(1,'bob','asdf')
]

# dictionary that indexes each user by name
#	username_mapping = { 'bob': {
#			'id': 1,
#			'username': 'bob',
#			'password': 'asdf'
#		}
#	}

username_mapping = {u.username: u for u in users}

# dictionary that indexes each user by id
#	userid_mapping = { 1: {
#			'id': 1,
#			'username': 'bob',
#			'password': 'asdf'
#		}
#	}

userid_mapping = {u.id: u for u in users}

# given a user name and password, select correct user and return that user (if the password matches)
def authenticate(username, password):
	user = username_mapping.get(username, None)
	# if user and user.password == password:
		# don't compare strings with strings. (String encoding issues)
	if safe_str_cmp(user.password, password):
		return user

# takes in a payload (contents of JWT), extract userID, and retrieve user
def identity(payload):
	user_id = payload['identity']
	return userid_mapping.get(user_id, None)
	# get the username, if the user name is not there, return None