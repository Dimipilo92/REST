from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
# resource represents whatever our Api handles. 
# if our Api gets and posts "students" then our Resource will be "students"
# create a class that inherits resource so it gets all its properties

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app) # create an api for our flask app so we can easily handle our resources

jwt = JWT(app, authenticate, identity)
# JWT will create a new endpoint '/auth'
# The authenticate function is used when a user requests access to a key.
# The identity function is used when a user requests to do an action that requires a key.
# User logs in -> given a key -> authenticate
# User wants to view a friend -> requires a key -> identity (verifying login)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items/')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':	# start the app only if this server not being imported
	app.run(debug=True, port=5000)
	
# maybe you just want to get the application.