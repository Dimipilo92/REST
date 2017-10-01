from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
# resource represents whatever our Api handles. 
# if our Api gets and posts "students" then our Resource will be "students"
# create a class that inherits resource so it gets all its properties

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app) # create an api for our flask app so we can easily handle our resources

jwt = JWT(app, authenticate, identity)
# JWT will create a new endpoint '/auth'
# The authenticate function is used when a user requests access to a key.
# The identity function is used when a user requests to do an action that requires a key.
# User logs in -> given a key -> authenticate
# User wants to view a friend -> requires a key -> identity (verifying login)

items = []

# 200 OK
# 201 Created
# 400 Bad Request - Request should not have been made. (Should have checked before trying to create)
# 401 Unauthorized
# 404 File not Found

# define our resource(s): student
# then define what you can do with your resources: student -> get
class Item(Resource): 			# create a "copy" of the resource class
	
	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type=float, # price is read as a float
		required=True, # no request comes through without price
		help="This field cannot be left blank!"
	)
	
	@jwt_required()
	def get(self, name):			# overload the get method to take in a name
		
		item = next(filter(lambda item: item['name'] == name,items), None)
		# filter(function, iterable) function returns filter object
		# list(iterable) will create a list from all the objects in the filter item
		# next(iterable, default) will return the first item returned by filter
		# if there are no items in filter, and a default value is not set, next() will break
		
		return {'item': item}, 200 if item is not None else 404
		# in java:
		#	return (item != Null)? 200 : 404
	
	def post(self, name):
	
		
		# data = request.get_json()
		# force=True: you don't need content type header, it will autoformat (can be dangerous)
		# silent=True: returns None, instead of an error, if formatting is off
		
		
		if next(filter(lambda item: item['name'] == name, items), None):
			return{'message': "An item with name '{}' already exists.".format(name)}, 400
		
		data = Item.parser.parse_args() # puts valid arguments in data, other arguments are discareded
		
		item = {'name': name, 'price': data['price']}
		items.append(item)
		return item, 201
		
	def delete(self, name):
		# check to see if item is in the list
		global items
		items = list(filter(lambda item: item['name'] != name, items))
		return {'message': 'Item deleted'}
			
				
	def put(self, name):
		data = Item.parser.parse_args() # puts valid arguments in data, other arguments are discareded
		item = next(filter(lambda item: item['name'] == name, items), None)
		if item is None:
			item = {'name': name, 'price': data['price']}
			items.append(item)
		else:
			item.update(data)
		return item
		
		
class ItemList(Resource):
	def get(self):
		return {'items':items}
		
# add the resource to the api
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items/')

app.run(debug=True, port=5000)

# this code replaces:
# 	@app.route('/student/<string:name>')
#	def get_student(name):
#		return jsonify({'student':name})