from flask import Flask
from flask_restful import Resource, Api
# resource represents whatever our Api handles. 
# if our Api gets and posts "students" then our Resource will be "students"
# create a class that inherits resource so it gets all its properties


app = Flask(__name__)
api = Api(app) # create an api for our flask app so we can easily handle our resources


# define our resource(s): student
# then define what you can do with your resources: student -> get
class Student(Resource): 			# create a "copy" of the resource class
	def get(self, name):			# overload the get method to take in a name
		return {'student': name}	# return a dictionary student w/ a name

		
# add the resource to the api
api.add_resource(Student, '/student/<string:name>')

app.run(debug=True, port=5000)

# this code replaces:
# 	@app.route('/student/<string:name>')
#	def get_student(name):
#		return jsonify({'student':name})