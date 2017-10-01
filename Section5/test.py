# replace by create_tables

import sqlite3

connection = sqlite3.connect('data.db') # connection string/uri for our database ( a path to the database)

cursor = connection.cursor() # get a cursor for a database. a cursor is like a pointer. Points to data and executes queries on what it's pointing to
# table cannot already exist

# this is the definition of our schema; the table is called users
create_table = "CREATE TABLE users (id int, username text, password text)" 
cursor.execute(create_table)

user = (1, 'jose', 'asdf')
insert_query = "INSERT INTO users VALUES(?,?,?)"
# insert into table [users] with the values [?,?, and ?] into the respective places [id, username, password]
cursor.execute(insert_query, user) # insert the user into the table

users = [
	(2, 'rolf', 'asdf'),
	(3, 'anne', 'xyz')

]

cursor.executemany(insert_query, users) #execute insert_query on the list of users

select_query = "SELECT * FROM users"
# select all columns from each row in users table

# create an iterable from the database
for row in cursor.execute(select_query):
	print (row)

connection.commit() # save the changes

connection.close() # good practice. not waiting for more data, not consuming resources