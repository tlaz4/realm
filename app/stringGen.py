import string, random

# generate a random string of alpha charatcers
def genString():
	return "".join([random.choice(string.ascii_lowercase) for i in range(4)])
