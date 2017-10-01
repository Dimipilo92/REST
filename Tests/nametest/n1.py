from n2 import print_name

print (__name__) 	# prints '__main__'
print_name			# prints '__n2__'

# essentially what this means is that if the file is NOT imported, then __name__ = __main__
# so this is useful to check to see if the file is being run as a script or as a module
# if __name__ == __main__: