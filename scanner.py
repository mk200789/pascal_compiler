import sys


def scan(input):
	#keep track of current row
	cur_row = 1
	#keep track of current column
	cur_col = 1

	output = open(input, 'r').read().splitlines()
	for line in output:
		print "current row scanned:" +str(cur_row)+ ":" +line
		cur_row+=1
		cur_col =1
		for a in line:
			print "currrent column scanned:"+str(cur_col)+":" +a
			cur_col+=1
		
	


if __name__ == '__main__':
	if len(sys.argv)!= 2:
		exit(1)

	#Open file
	filename = sys.argv[1]
	#Read file
	scan(filename)


