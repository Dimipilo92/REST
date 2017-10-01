def who_do_you_know():
	people = input("Bitch, who do you know?").split(",")
	return [person.strip() for person in people]

def ask_user():
	person_to find = input("Who you tryna find?")
	if person_to_find in who_do_you_know():
		print("Yeah, you know that person.")
		
ask_user();