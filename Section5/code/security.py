from user import User
from werkzeug.security import safe_str_cmp

# given a user name and password, select correct user and return that user (if the password matches)
def authenticate(username, password):
	user = User.find_by_username(username)
	# if user and user.password == password:
		# don't compare strings with strings. (String encoding issues)
	if user and safe_str_cmp(user.password, password):
		return user

# takes in a payload (contents of JWT), extract userID, and retrieve user
def identity(payload):
	user_id = payload['identity']
	return User.find_by_id(user_id)