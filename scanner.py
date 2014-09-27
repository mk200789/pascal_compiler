import sys

def scan(input):
	output = open(input).read()
	
	for a in output:
		print a


if __name__ == '__main__':
	if len(sys.argv)!= 2:
		exit(1)

	#Open file
	filename = sys.argv[1]
	#Read file
	scan(filename)
