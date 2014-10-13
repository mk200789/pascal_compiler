import sys
from prettytable import PrettyTable

class Scanner(object):
    def __init__(self, cur_row, cur_col, string_mode, string_rec, count, cur_state, numeric_mode, real_mode, tokens, cur_token, table):
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
        #set state of current token in build_state(a)
        self.cur_token = cur_token
        self.table = table

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
                    self.build_string(a)
                elif self.numeric_mode:
                    self.build_number(a)
                else:
                    self.build_state(a)
                self.cur_col += 1
        print(self.print_table(1, ['NUMBER', 'TOKEN', 'COLUMN', 'VALUE', 'ROW'], [], self.table ))                
        print self.tokens

    def build_string(self, a):
        if ord(a) == 39:
            self.string_rec += a
            #print "Row " + str(self.cur_row-1) +" : "+ str(self.string_rec) + " is a string. "
            self.tokens.append(('TK_STRING', self.string_rec, self.cur_row-1, self.cur_col))
            self.table.append({'TOKEN' : 'TK_STRING', 'VALUE' : self.string_rec, 'ROW' : self.cur_row-1, 'COL' : self.cur_col})
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
                #print "Row " + str(self.cur_row-1) +" : "+ str(self.string_rec) + " is a real number."
                self.tokens.append(('TK_REAL', self.string_rec, self.cur_row-1, self.cur_col))
                self.table.append({'TOKEN' : 'TK_REAL', 'VALUE' : self.string_rec, 'ROW' : self.cur_row-1, 'COL' : self.cur_col})
                self.real_mode = False
                self.string_rec = ''
                return
            else:
                #print "Row " + str(self.cur_row-1) +" : "+ str(self.string_rec) + " is a number."
                self.tokens.append(( 'TK_INTEGER', self.string_rec, self.cur_row-1, self.cur_col))
                self.table.append({'TOKEN' : 'TK_INTEGER', 'VALUE' : self.string_rec, 'ROW' : self.cur_row-1, 'COL' : self.cur_col})
                self.string_rec = ''
                return

        if ord(a) == 46:
            #a real number if a dot is scene
            self.real_mode = True
            self.string_rec += a
            return

    def build_state(self, a):
        #state machine to keep track of current state
        #space state
        print self.string_rec
        if ord(a) <= 32:
            if self.to_upper(self.string_rec) in self.keyword:
                print self.keyword[self.to_upper(self.string_rec)]
                self.tokens.append((self.keyword[self.to_upper(self.string_rec)], self.string_rec, self.cur_row-1, self.cur_col))
                self.table.append({'TOKEN' : self.keyword[self.to_upper(self.string_rec)], 'VALUE' : self.string_rec, 'ROW' : self.cur_row-1, 'COL' : self.cur_col})

                if self.to_upper(self.string_rec) == 'VAR':
                    self.cur_token = 'IDENTIFIER'
                    #print str(self.cur_token) + " hi"
                else:
                    self.string_rec = ''
                    self.cur_token =''
                    return
            elif self.to_upper(self.string_rec) not in self.keyword:
                if self.cur_token:
                    #print str(self.cur_token) + "APPLE"
                    self.tokens.append((self.keyword[self.cur_token], self.string_rec, self.cur_row-1, self.cur_col))
                    self.table.append({'TOKEN' : self.keyword[self.cur_token], 'VALUE' : self.string_rec, 'ROW' : self.cur_row-1, 'COL' : self.cur_col})
                    self.cur_token = ''
            self.string_rec = ''
            return

        #string state, single quotation
        if ord(a) == 39:
            self.string_rec =''
            self.string_mode = True
            self.string_rec += a
            self.count +=1
            return

        #numeric state
        if a.isdigit() and not self.cur_token:
            self.numeric_mode = True
            self.string_rec += a
            return

        #semicolon state
        if ord(a) == 59 and not self.numeric_mode:
            if self.string_rec:
                if self.to_upper(self.string_rec) in self.keyword:
                    print self.keyword[self.to_upper(self.string_rec)]
                    self.tokens.append((self.keyword[self.to_upper(self.string_rec)], self.string_rec, self.cur_row-1, self.cur_col-1))
                    self.table.append({'TOKEN' : self.keyword[self.to_upper(self.string_rec)], 'VALUE' : self.string_rec, 'ROW' : self.cur_row-1, 'COL' : self.cur_col-1})
            self.tokens.append((self.keyword[a],a, self.cur_row-1, self.cur_col))
            self.table.append({'TOKEN' : self.keyword[a], 'VALUE' : a, 'ROW' : self.cur_row-1, 'COL' : self.cur_col})
            self.string_rec =''
            return

        #colon
        if ord(a) == 58:
            #set current token as COLON
            self.string_rec = a
            #print str(self.string_rec)+"zoomba"
            self.cur_token = a
            return

        #equal
        if ord(a) == 61:
            self.string_rec +=a
            #print str(self.string_rec) + "dfdkfjkd"
            if ord(self.cur_token) == 58:
            # := state
                if self.string_rec in self.keyword:
                    self.tokens.append((self.keyword[self.string_rec], self.string_rec, self.cur_row-1, self.cur_col))
                    self.table.append({'TOKEN' : self.keyword[self.string_rec], 'VALUE' : self.string_rec, 'ROW' : self.cur_row-1, 'COL' : self.cur_col})
                    self.string_rec = ''
                    self.cur_token =''
                    return

        #plus
        if ord(a) == 43:
            self.tokens.append((self.keyword[a], a, self.cur_row-1, self.cur_col))
            self.table.append({'TOKEN' : self.keyword[a], 'VALUE' : a, 'ROW' : self.cur_row-1, 'COL' : self.cur_col})
            self.string_rec = ''
            return

        #minus
        if ord(a) == 45:
            self.tokens.append((self.keyword[a], a, self.cur_row-1, self.cur_col))
            self.table.append({'TOKEN' : self.keyword[a], 'VALUE' : a, 'ROW' : self.cur_row-1, 'COL' : self.cur_col})
            self.string_rec = ''
            return

        #dot
        if ord(a) == 46:
            if self.to_upper(self.string_rec) in self.keyword:
                self.tokens.append((self.keyword[self.to_upper(self.string_rec)], self.string_rec, self.cur_row-1, self.cur_col))
                self.table.append({'TOKEN' : self.keyword[self.to_upper(self.string_rec)], 'VALUE' : self.string_rec, 'ROW' : self.cur_row-1, 'COL' : self.cur_col})
                self.string_rec = ''
                return

        #open parenthesis
        if ord(a) == 40:
            if self.string_rec:
                if self.to_upper(self.string_rec) in self.keyword:
                    self.tokens.append((self.keyword[self.to_upper(self.string_rec)], self.string_rec, self.cur_row-1, self.cur_col))
                    self.table.append({'TOKEN' : self.keyword[self.to_upper(self.string_rec)], 'VALUE' : self.string_rec, 'ROW' : self.cur_row-1, 'COL' : self.cur_col})
                    self.string_rec = ''
            else:
                if self.to_upper(self.string_rec) in self.keyword:
                    self.tokens.append((self.keyword[self.to_upper(self.string_rec)], self.string_rec, self.cur_row-1, self.cur_col))
                    self.table.append({'TOKEN' : self.keyword[self.to_upper(self.string_rec)], 'VALUE' : self.string_rec, 'ROW' : self.cur_row-1, 'COL' : self.cur_col})
                    self.string_rec = a
                return               
        self.string_rec += a



    def to_upper(self, a):
        #returns lowercase strings
        return a.upper()

    #learning purpose
    def show(self):
        #print self.tokens
        print self.cur_row

    #for debugging purpose
    def print_table(self, i, names, row, data):
        table = PrettyTable(names)
        #print names
        for datum in data:
            row.append(i)
            for k, v in datum.items():
                #print str(k) + "boob"
                if str(k) == 'TOKEN':
                    row.append(v)
                if str(k) == 'VALUE':                    
                    row.append(v)
                if str(k) == 'ROW':
                    row.append(v)                    
                if str(k) == 'COL':
                    row.append(v)
            table.add_row(row)
            del row[:]
            i += 1
        return table        

##write funcion take in table name and keyname and return value

    keyword={
        'STRING'    : 'TK_ID_STRING',
        'REAL'      : 'TK_REAL',
        'INTEGER'   : 'TK_ID_INTEGER',
        'PROGRAM'   : 'TK_PROGRAM',
        'VAR'       : 'TK_VAR',
        'IDENTIFIER': 'TK_IDENTIFIER',
        'BEGIN'     : 'TK_BEGIN',
        'END'       : 'TK_END',
        ';'         : 'TK_SEMICOLON',            
        ':'         : 'TK_COLON',
        '='         : 'TK_EQUAL',
        ':='        : 'TK_ASSIGNMENT',
        '+'         : 'TK_ADD',
        '-'         : 'TK_MINUS',
        '('         : 'TK_OPEN_PARENTHESIS',
        ')'         : 'TK_CLOSE_PARENTHESIS',
        'WRITELN'   : 'TK_WRITELN'
    }          
          


if __name__ == '__main__':
    if len(sys.argv)!= 2:
        exit(1)

    #Open file
    filename = sys.argv[1]

    a = Scanner(1,1,False,'', 0, '', False, False,[],'',[])
    a.scan(filename)
    

