import sys

def scan(input):
	for a in input:
		print a


if __name__ == '__main__':
	scan("Hello World")
	if len(sys.argv)!= 2:
		exit(1)

	#Open file
	filename = sys.argv[1]
	#Read file
	output = open(filename).read()
	#print file
	print output