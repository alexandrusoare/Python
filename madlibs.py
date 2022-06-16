# string concatenation simple project

actor = "Leonardo Dicaprio" #some string variable

print("The actor is " + actor)
print("The actor is {}".format(actor))
print(f"The actor is {actor}")

adj = input("Adjective: ")
verb1 = input("Verb: ")
verb2 = input("Verb: ")
famous_person = input("Famous person: ")



madlib = f"Computer programming is so {adj}! it makes me so excited all the time because \
I love to {verb1}. Stay hydrated and {verb2} like you are {famous_person}!"

print(madlib)