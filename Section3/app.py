from flask import Flask, jsonify, request, render_template
# from the flask module:
# Flask is the main flask class
# jsonify is a method that turns dictionaries into JSON
# request processes http request data
# render_template works with the templating engine

app = Flask(__name__) # create a flask object with a unique name.

# 	tell the app what "requests" it should understand
#	@app.route('/') # 'http://www.google.com/' <- recognize the root directory
#	def home():		# name does not matter. must return something to the browser
#		return "Hello, world!" # will return hello world to the browser.

# MAKESHIFT DATABASE

stores = [
	{
		'name': 'My Wonderful Store',
		'items': [
			{
			'name': 'My Item',
			'price': 15.99
			}
		]
	}
]
	
# REQUEST LIST
	
# POST - used to recieve data
# GET - used to send data back

@app.route('/')
def home():
	return render_template('index.html'); 
	# returns the html of index.html
	# will automatically looks in templates directory

# POST /store, data: {name:} - create a store with a given name
@app.route('/store', methods=['POST'])
def create_store():
	request_data = request.get_json() # 'request' accesses the json from the store
	new_store = {
		'name': request_data['name'],
		'items': []
	}
	stores.append(new_store)
	return jsonify(new_store)
	
# GET /store/<string:name> - return a store with a give name
@app.route('/store/<string:store_name>') # '<string:store_name>' is flask specific syntax, the variable name corresponds to the param of the following function
def get_store(store_name):
	for store in stores:
		if store['name'] == store_name:
			return jsonify(store)
	return "Store does not exist"
	
# GET /store - return a list of all stores
@app.route('/store')
def get_store_list():
	return jsonify({'stores':stores}) # turns our list of stores into a dictionary so it can be jsonified
	
# POST /store/<string:name>/item , data: {name:, price:} - create an item at the given store, with the given name and price
@app.route('/store/<string:store_name>/item', methods=['POST'])
def create_item(store_name):
	request_data = request.get_json()
	for store in stores:
		if store['name'] == store_name:
			new_item = {
				'name':request_data['name'],
				'price':request_data['price']
			}
			store['items'].append(new_item)
			return jsonify(store)
	return "Store does not exist"
	
# GET /store/<string:name>/item - return a list of items for the store with a given name
@app.route('/store/<string:store_name>/item')
def get_item_list(store_name):
	for store in stores:
		if store['name'] == store_name:
			return jsonify({'items': store['items']})
	return "Store does not exist"


app.run(debug=True, port=5000) 
# tell the pc what port to recieve and return requests from and to
# some port might be using 5000. If so, just change it.
# running in debug mode will auto update code changes