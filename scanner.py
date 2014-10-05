import sys

class Scanner(object):
    def __init__(self, cur_row, cur_col, string_mode, string_rec, count):
        #keep track of current row
        self.cur_row = cur_row
        #keep track of current column
        self.cur_col = cur_col
        #check if in string mode
        self.string_mode = string_mode
        self.string_rec = string_rec
        self.count = count

    def scan(self, input):
        output = open(input, 'r').read().splitlines()
        for line in output:
            self.cur_row +=1
            self.cur_col =1
            for a in line:
            #if a double quotation is seen
                if ord(a) == 34:
                    self.count +=1
                    self.string_mode = True

                if self.string_mode == True:
                    self.build_string(a)

                self.cur_col +=1

    def build_string(self, a):
        if self.count == 2:
            self.string_rec += a
            print "Row " + str(self.cur_row-1) +" : "+ str(self.string_rec) + " is a string."
            self.string_rec = ''
            self.count = 0
            self.string_mode = False
            return
        else:
            self.string_rec += a
            return


	#learning purpose
	def show(self):
		print self.cur_row

    
    keyword={
        'STRING'  : 'TK_STRING',
        'PROGRAM' : 'TK_PROGRAM'
    }        






if __name__ == '__main__':
	if len(sys.argv)!= 2:
		exit(1)

	#Open file
	filename = sys.argv[1]

	a = Scanner(1,1,False,'', 0)
	a.scan(filename)
