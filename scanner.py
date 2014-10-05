import sys

class Scanner(object):
    def __init__(self, cur_row, cur_col, string_mode, string_rec, count, cur_state, numeric_mode, real_mode):
        #keep track of current row
        self.cur_row = cur_row
        #keep track of current column
        self.cur_col = cur_col
        #check if in string mode
        self.string_mode = string_mode
        self.string_rec = string_rec
        #keep track of quotation
        self.count = count
        self.cur_state = cur_state
        self.numeric_mode = numeric_mode
        self.real_mode = real_mode

    def scan(self, input):
        output = open(input, 'r').read().splitlines()
        for line in output:
            self.cur_row +=1
            self.cur_col =1
            for a in line:
            #if a double quotation is seen
                if self.string_mode:
                    if ord(a) == 34:
                        self.count += 1
                    self.build_string(a)
                    self.cur_col += 1
                elif self.numeric_mode:
                    self.build_number(a)
                else:
                    self.build_state(a)
                    self.cur_col += 1


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

    def build_number(self, a):
        #Handles number, or real numbers.
        if a.isdigit():
            self.string_rec += a
        
        if not(a.isdigit()) and ord(a)!= 59:
            self.numeric_mode = False
            if self.real_mode:
                #print self.string_rec
                self.string_rec += a
                return
           

        if ord(a) == 46:
            # a real number
            self.real_mode = True
            self.string_rec += a
            return


        if ord(a) == 59:
            if self.real_mode:
                print "Row " + str(self.cur_row-1) +" : "+ str(self.string_rec) + " is a real number."
                self.real_mode = False
            elif self.numeric_mode:
                print "Row " + str(self.cur_row-1) +" : "+ str(self.string_rec) + " is a number."
                self.numeric_mode = False
            self.string_rec = ''
            return            

    def build_state(self, a):
        #state machine to keep track of current state
        #string state
        if ord(a) == 34:
            self.string_mode = True
            self.string_rec += a
            self.count +=1
            return
        #numeric state
        elif a.isdigit():
            self.numeric_mode = True
            self.string_rec += a
            return


	#learning purpose
	def show(self):
        #print self.tokens
		print self.cur_row
    
    keyword={
        'STRING'    : 'TK_STRING',
        'REAL'      : 'TK_REAL',
        'INTEGER'   : 'TK_INTEGER',
        'PROGRAM'   : 'TK_PROGRAM'
    }        


if __name__ == '__main__':
	if len(sys.argv)!= 2:
		exit(1)

	#Open file
	filename = sys.argv[1]

	a = Scanner(1,1,False,'', 0, '', False, False)
	a.scan(filename)
    

