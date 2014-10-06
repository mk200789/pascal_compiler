import sys

class Scanner(object):
    def __init__(self, cur_row, cur_col, string_mode, string_rec, count, cur_state, numeric_mode, real_mode, tokens):
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
        #returns a list of tokens
        self.tokens = tokens

    def scan(self, input):
        output = open(input, 'r').read().splitlines()
        for line in output:
            #print "current row scanned:" +str(self.cur_row)+ ":" +line
            self.cur_row +=1
            self.cur_col =1
            for a in line:
            #if a double quotation is seen
                #print "currrent column scanned:"+str(self.cur_col)+":" +a
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
        print self.tokens


    def build_string(self, a):
        if self.count == 2:
            self.string_rec += a
            print "Row " + str(self.cur_row-1) +" : "+ str(self.string_rec) + " is a string. "
            self.tokens.append(('TK_STRING', self.string_rec, self.cur_row-1, self.cur_col - 1))
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

        #if character is a space or symbol, build a new token
        if ord(a) > 57 or ord(a) <= 32:
            self.numeric_mode = False
            if self.real_mode:
                print "Row " + str(self.cur_row-1) +" : "+ str(self.string_rec) + " is a real number."
                self.tokens.append(('TK_REAL', self.string_rec, self.cur_row-1, self.cur_col - 1))
                self.real_mode = False
                self.string_rec = ''
                return
            else:
                print "Row " + str(self.cur_row-1) +" : "+ str(self.string_rec) + " is a number."
                self.tokens.append(( 'TK_INTEGER', self.string_rec, self.cur_row-1, self.cur_col - 1 ))
                self.string_rec = ''
                return

        if ord(a) == 46:
            #a real number if a dot is scene
            self.real_mode = True
            self.string_rec += a
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

	a = Scanner(1,1,False,'', 0, '', False, False,[])
	a.scan(filename)
    

