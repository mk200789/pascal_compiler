import sys

class Scanner(object):
	def __init__(self, cur_row, cur_col, string_mode):
		self.cur_row = cur_row
		self.cur_col = cur_col
		self.string_mode = string_mode

	def scan(self, input):
		output = open(input, 'r').read().splitlines()
		for line in output:
			self.cur_row +=1
			self.cur_col +=1
			for a in line:
				self.cur_col +=1

	#learning purpose
	def show(self):
		print self.cur_row




#######################################################

def scan(input):
	string_c= 0
	string_rec = ''
	string_mode = False
	identifier_mode = False

	#TOKEN
	keyword={
		'STRING'  : 'TK_STRING',
		'PROGRAM' : 'TK_PROGRAM'
	}

	#keep track of current row
	cur_row = 1
	#keep track of current column
	cur_col = 1

	output = open(input, 'r').read().splitlines()
	for line in output:
		#print "current row scanned:" +str(cur_row)+ ":" +line
		cur_row+=1
		cur_col =1
		for a in line:
			#print "currrent column scanned:"+str(cur_col)+":" +a
			if a == '"':
				string_c +=1
				string_mode = True

			# if in string mode append characters
			if string_mode:
				string_rec += str(a)

				if string_c == 2 :
					print "Row " + str(cur_row) +": "+ string_rec + " is a string."
					string_c=0
					string_rec=''

				if string_c == 0:
					string_mode = False
			cur_col+=1


if __name__ == '__main__':
	if len(sys.argv)!= 2:
		exit(1)

	#Open file
	filename = sys.argv[1]
	#Read file
	scan(filename)

	a = Scanner(1,1,False)
	a.show()
