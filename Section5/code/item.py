import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Item(Resource): 			# create a "copy" of the resource class
	
	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type=float, # price is read as a float
		required=True, # no request comes through without price
		help="This field cannot be left blank!"
	)
	
	# originally this was in the get method, however you cannot call the get method without a jwt_token, so to reuse this code, it was taken out of get.
	@classmethod
	def find_by_name(cls, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		
		query = "SELECT * FROM items WHERE name =?"
		result = cursor.execute(query, (name,))
		row = result.fetchone()
		
		connection.close()
		
		if row:
			return {'item': {'name':row[0], 'price':row[1]}}
	
	@classmethod
	def insert(cls, item):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		
		query = "INSERT INTO items VALUES (?, ?)"
		cursor.execute(query,(item['name'], item['price']))
		
		connection.commit()
		connection.close()
	
	@classmethod
	def update(cls, item):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		
		query = "UPDATE items SET price=? WHERE name=?"
		cursor.execute(query, (item['price'], item['name']))
		
		connection.commit()
		connection.close()
		
	
	@jwt_required()
	def get(self, name):			# overload the get method to take in a name
	
		try:
			item = self.find_by_name(name)
		except: # if the search failed to run
			return {"message": "An error occured retrieving the item."}, 500
		
		if item:
			return item
		return {'message': 'Item not found'}, 404

	def post(self, name):
		if Item.find_by_name(name):
			return{'message': "An item with name '{}' already exists.".format(name)}, 400
		
		data = Item.parser.parse_args() # puts valid arguments in data, other arguments are discareded
		item = {'name':name, 'price':data['price']}
		
		try:
			self.insert(item)
		except:
			return {"message": "An error occured inserting the item."}, 500
		
		return item, 201
		
	def delete(self, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		
		query = "DELETE FROM items WHERE name=?"
		cursor.execute(query, (name,))
		
		connection.commit()
		connection.close()
		
		return {'message': 'Item deleted'}
			
				
	def put(self, name):
		data = Item.parser.parse_args() # puts valid arguments in data, other arguments are discareded
		# item = next(filter(lambda item: item['name'] == name, items), None)
		item = self.find_by_name(name)
		updated_item = {'name': name, 'price': data['price']}
		
		if item is None:
			try:
				self.insert(updated_item)
			except:
				return {"message": "An error occured inserting the item."}, 500
		else:
			try:
				self.update(updated_item)
			except:
				return {"message": "An error occured updating the item."}, 500
		return updated_item
		
		
class ItemList(Resource):
	def get(self):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		
		query = "SELECT * FROM items"
		results = cursor.execute(query)
		items = []
		for row in results:
			items.append({'name':row[0], 'price':row[1]})
		
		connection.close()
		
		return {'items':items}
		
# add the resource to the api
