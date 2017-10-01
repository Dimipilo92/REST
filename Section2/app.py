from flask import Flask # from the flask module, import the class, Flask

app = Flask(__name__) # create a flask object with a unique name.

# tell the app what "requests" it should understand
@app.route('/') # 'http://www.google.com/' <- recognize the root directory
def home():		# name does not matter. must return something to the browser
	return "Hello, world!" # will return hello world to the browser.

app.run(debug=True, port=5000) 
# tell the pc what port to recieve and return requests from and to
# some port might be using 5000. If so, just change it.