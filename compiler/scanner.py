import sys
from prettytable import PrettyTable

class Scanner(object):
    def __init__(self, cur_row, cur_col, string_mode, string_rec, numeric_mode, real_mode, tokens, cur_token, table, comment_mode):
        #keep track of current row
        self.cur_row = cur_row
        #keep track of current column
        self.cur_col = cur_col
        #check if in string mode
        self.string_mode = string_mode
        self.string_rec = string_rec
        self.numeric_mode = numeric_mode
        self.real_mode = real_mode
        #returns a list of tokens
        self.tokens = tokens
        self.cur_token = cur_token
        self.table = table
        self.comment_mode = comment_mode

    def scan(self, input):
        output = open(input, 'r').readlines()
        for line in output:
            #print "current row scanned:" +str(self.cur_row)#+ ":" +line
            for a in line:
            #if a double quotation is seen
                #print "currrent column scanned:"+str(self.cur_col)+" : " + a
                if self.comment_mode:
                    self.build_comment(a)
                    if ord(a) == 10:
                        self.cur_col = 0
                        self.cur_row +=1
                elif self.string_mode:
                    self.build_string(a)
                    if ord(a) == 10:
                        self.cur_col = 0
                        self.cur_row += 1
                elif self.numeric_mode:
                    self.build_number(a)                 
                    if ord(a) == 10:
                        self.cur_col = 0
                        self.cur_row += 1
                else:
                    self.build_state(a)
                    if ord(a) == 10: 
                        self.cur_col = 0
                        self.cur_row += 1               
                self.cur_col += 1
        print(self.print_table(1, ['NUMBER', 'TOKEN', 'COLUMN', 'VALUE', 'ROW'], [], self.table ))
        #print self.tokens
        return self.tokens

    def build_string(self, a):
        if ord(a) == 39:
            self.string_rec += a
            #print "Row " + str(self.cur_row) +" : "+ str(self.string_rec) + " is a string. "
            self.tokens.append(('TK_STRING', self.string_rec, self.cur_row, self.cur_col))
            self.table.append({'TOKEN' : 'TK_STRING', 'VALUE' : self.string_rec, 'ROW' : self.cur_row, 'COL' : self.cur_col})
            self.string_rec = ''
            self.string_mode = False
            return
        else:
            self.string_rec += a
            return

    def build_comment(self,a):
        if ord(a) == 41:
            if self.cur_token:
                self.string_rec += a
                self.tokens.append(('TK_COMMENT', self.string_rec, self.cur_row, self.cur_col))
                self.table.append({'TOKEN' : 'TK_COMMENT', 'VALUE' : self.string_rec, 'ROW' : self.cur_row, 'COL' : self.cur_col})                
                self.comment_mode = False
                self.cur_token =''
                self.string_rec=''
                return
        else:
            self.string_rec+=a

    def build_number(self, a):
        #Handles number, or real numbers.
        if a.isdigit():
            self.string_rec += a

        #if character is a space or symbol, build a new token
        if ord(a) > 57 or ord(a) <= 41:
            self.numeric_mode = False
            if self.real_mode:
                #print "Row " + str(self.cur_row) +" : "+ str(self.string_rec) + " is a real number."
                self.tokens.append(('TK_REAL', self.string_rec, self.cur_row, self.cur_col-1))
                self.table.append({'TOKEN' : 'TK_REAL', 'VALUE' : self.string_rec, 'ROW' : self.cur_row, 'COL' : self.cur_col-1})
                self.real_mode = False
            else:
                #print "Row " + str(self.cur_row) +" : "+ str(self.string_rec) + " is a number."
                self.tokens.append(( 'TK_INTEGER', self.string_rec, self.cur_row, self.cur_col-1))
                self.table.append({'TOKEN' : 'TK_INTEGER', 'VALUE' : self.string_rec, 'ROW' : self.cur_row, 'COL' : self.cur_col-1})

            #check current character
            if a in self.keyword:
                if self.cur_token:
                    self.cur_token =''
                self.tokens.append(( self.keyword[a], a, self.cur_row, self.cur_col))
                self.table.append({'TOKEN' : self.keyword[a], 'VALUE' : a, 'ROW' : self.cur_row, 'COL' : self.cur_col})

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
        #print str(self.string_rec) + " : " +a + " FIRST PRINT IN BUILD_STATE.    CURRENT TOKEN: "+ str(self.cur_token)
        #print "+is there token: "+ str(self.cur_token)
        if ord(a) <= 32:         
            if self.cur_token:
                if self.to_upper(self.string_rec) in self.keyword:
                    #print "SPACE STATE: THERE IS A TOKEN - STRING IS IN KEYWORD LIST " #+str(self.string_rec)
                    self.tokens.append((self.keyword[self.to_upper(self.string_rec)], self.string_rec, self.cur_row, self.cur_col-1))
                    self.table.append({'TOKEN' : self.keyword[self.to_upper(self.string_rec)], 'VALUE' : self.string_rec, 'ROW' : self.cur_row, 'COL' : self.cur_col-1})
                    self.cur_token =''
                    self.string_rec = ''
                    return
                if self.to_upper(self.string_rec) not in self.keyword:
                    #print "SPACE STATE: THERE IS A TOKEN - STRING ISN'T IN KEYWORD LIST "#+str(self.string_rec)
                    self.tokens.append((self.keyword[self.cur_token], self.string_rec, self.cur_row, self.cur_col-1))
                    self.table.append({'TOKEN' : self.keyword[self.cur_token], 'VALUE' : self.string_rec, 'ROW' : self.cur_row, 'COL' : self.cur_col-1})
                    #if self.string_rec == 'x':
                    #    print "SJJFJFJFJFJFJFJFS"
                    #    print self.tokens
                    self.cur_token =''
                    self.string_rec = ''
                    return                    

            if not self.cur_token:
                return        

        #string state, single quotation
        if ord(a) == 39:
            self.string_rec =''
            self.string_mode = True
            self.string_rec += a
            return

        #numeric state
        if a.isdigit() :
            self.numeric_mode = True
            self.string_rec += a
            return

        #dot state
        if ord(a)==46:
            if self.cur_token:
                self.string_rec +=a 
                self.tokens.append((self.keyword[self.to_upper(self.string_rec)], self.string_rec, self.cur_row, self.cur_col))
                self.table.append({'TOKEN' : self.keyword[self.to_upper(self.string_rec)], 'VALUE' : self.string_rec, 'ROW' : self.cur_row, 'COL' : self.cur_col})
                self.string_rec = ''
                self.cur_token=''
                return

        #semicolon state
        if ord(a) == 59 and not self.numeric_mode:
            if not self.cur_token:
                if self.string_rec:
                    self.tokens.append((self.keyword['IDENTIFIER'], self.string_rec, self.cur_row, self.cur_col-1))
                    self.table.append({'TOKEN' : self.keyword['IDENTIFIER'], 'VALUE' : self.string_rec, 'ROW' : self.cur_row, 'COL' : self.cur_col-1})
            else:
                if self.to_upper(self.string_rec) == 'END':
                    #print "END;"
                    self.string_rec +=a
                    self.tokens.append((self.keyword[self.to_upper(self.string_rec)], self.string_rec, self.cur_row, self.cur_col-1))
                    self.table.append({'TOKEN' : self.keyword[self.to_upper(self.string_rec)], 'VALUE' : self.string_rec, 'ROW' : self.cur_row, 'COL' : self.cur_col-1})
                else:
                    self.tokens.append((self.keyword[self.to_upper(self.cur_token)], self.string_rec, self.cur_row, self.cur_col-1))
                    self.table.append({'TOKEN' : self.keyword[self.to_upper(self.cur_token)], 'VALUE' : self.string_rec, 'ROW' : self.cur_row, 'COL' : self.cur_col-1})
            #print "INSIDE OF SEMICOLON"
            if self.to_upper(self.string_rec) != 'END;':
                self.tokens.append((self.keyword[a],a, self.cur_row, self.cur_col))
                self.table.append({'TOKEN' : self.keyword[a], 'VALUE' : a, 'ROW' : self.cur_row, 'COL' : self.cur_col})
            self.string_rec = ''
            self.cur_token =''
            return

        #colon
        if ord(a) == 58:
            if self.string_rec:
                # if there's a string before the colon, it's an identifier
                self.tokens.append((self.keyword['IDENTIFIER'], self.string_rec, self.cur_row, self.cur_col-2))
                self.table.append({'TOKEN' : self.keyword['IDENTIFIER'], 'VALUE' : self.string_rec, 'ROW' : self.cur_row, 'COL' : self.cur_col-2})          
            #set current token as COLON
            self.string_rec = a
            self.cur_token = a
            #print "INSIDE OF COLON"
            return

        #equal
        if ord(a) == 61:
            #self.string_rec +=a
            if not self.cur_token:
                if self.string_rec != '':
                    self.tokens.append((self.keyword['IDENTIFIER'], self.string_rec, self.cur_row, self.cur_col))
                    self.table.append({'TOKEN' : self.keyword['IDENTIFIER'], 'VALUE' : self.string_rec, 'ROW' : self.cur_row, 'COL' : self.cur_col})
                self.tokens.append((self.keyword['='], '=', self.cur_row, self.cur_col))
                self.table.append({'TOKEN' : self.keyword['='], 'VALUE' : '=', 'ROW' : self.cur_row, 'COL' : self.cur_col})
                self.string_rec = ''
                #print self.tokens
                return                
            if self.cur_token: #== 58:
            # := state
                self.string_rec +=a
                if self.string_rec in self.keyword:
                    self.tokens.append((self.keyword[self.string_rec], self.string_rec, self.cur_row, self.cur_col))
                    self.table.append({'TOKEN' : self.keyword[self.string_rec], 'VALUE' : self.string_rec, 'ROW' : self.cur_row, 'COL' : self.cur_col})
                    self.string_rec = ''
                    self.cur_token =''
                    return

        #plus / minus state
        if ord(a) == 43 or ord(a) == 45:
            self.tokens.append((self.keyword[a], a, self.cur_row, self.cur_col-1))
            self.table.append({'TOKEN' : self.keyword[a], 'VALUE' : a, 'ROW' : self.cur_row, 'COL' : self.cur_col-1})
            self.string_rec = ''
            return

        #open parenthesis
        if ord(a) == 40:
            if self.string_rec:
                #print "function" + str(self.string_rec)
                #if there's string in record prior the opening paranthesis, then string must match keyword list
                self.tokens.append((self.keyword[self.to_upper(self.string_rec)], self.string_rec, self.cur_row, self.cur_col-1))
                self.table.append({'TOKEN' : self.keyword[self.to_upper(self.string_rec)], 'VALUE' : self.string_rec, 'ROW' : self.cur_row, 'COL' : self.cur_col-1})
                self.tokens.append((self.keyword[a],a, self.cur_row, self.cur_col))
                self.table.append({'TOKEN' : self.keyword[a], 'VALUE' : a, 'ROW' : self.cur_row, 'COL' : self.cur_col})
                self.string_rec=''
                self.cur_token = a
                return
                
        #close paranthesis
        if ord(a) == 41:
            if self.cur_token:
                if self.string_rec:
                    #if there's string in record prior the closing paranthesis, then this string is an identifier
                    self.tokens.append((self.keyword['IDENTIFIER'], self.string_rec, self.cur_row, self.cur_col-1))
                    self.table.append({'TOKEN' : self.keyword['IDENTIFIER'], 'VALUE' : self.string_rec, 'ROW' : self.cur_row, 'COL' : self.cur_col-1})
                self.tokens.append((self.keyword[a], a, self.cur_row, self.cur_col))
                self.table.append({'TOKEN' : self.keyword[a], 'VALUE' : a, 'ROW' : self.cur_row, 'COL' : self.cur_col})
            self.string_rec=''
            self.cur_token =''
            return

        #####mult, comment
        if ord(a) == 42:
            #if paranthesis, then its a comment, set comment mode
            if self.cur_token:
                self.comment_mode = True
                self.string_rec += a
                return

        #comma
        if ord(a) == 44:
            #this is covered if the comma is right after the identifier
            if self.string_rec:
                self.tokens.append((self.keyword['IDENTIFIER'], self.string_rec, self.cur_row, self.cur_col-1))
                self.table.append({'TOKEN' : self.keyword['IDENTIFIER'], 'VALUE' : self.string_rec, 'ROW' : self.cur_row, 'COL' : self.cur_col-1})
                self.tokens.append((self.keyword[a], a, self.cur_row, self.cur_col))
                self.table.append({'TOKEN' : self.keyword[a], 'VALUE' : a, 'ROW' : self.cur_row, 'COL' : self.cur_col})
                self.string_rec =''
                self.cur_token =''
                return

        #less state / greater state
        if ord(a) == 60 or ord(a) == 62:
            self.string_rec = a
            self.cur_token = a
            return

        self.string_rec += a

        if self.to_upper(self.string_rec) != 'END':
            if self.to_upper(self.string_rec) not in self.keyword:
                self.cur_token = 'IDENTIFIER'
                return
            if self.to_upper(self.string_rec) in self.keyword:
                self.cur_token = self.string_rec
                return



    def to_upper(self, a):
        #returns lowercase strings
        return a.upper()

    #for debugging purpose
    def print_table(self, i, names, row, data):
        table = PrettyTable(names)
        #print names
        for datum in data:
            row.append(i)
            for k, v in datum.items():
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
        'CHAR'      : 'TK_CHAR'
        'REAL'      : 'TK_REAL',
        'INTEGER'   : 'TK_ID_INTEGER',
        'BOOLEAN'   : 'TK_BOOLEAN',
        'FLOAT'     : 'TK_FLOAT',
        'CHAR'      : 'TK_CHAR',
        'PROGRAM'   : 'TK_PROGRAM',
        'USES'      : 'TK_USES',
        'VAR'       : 'TK_VAR',
        'IDENTIFIER': 'TK_IDENTIFIER',
        'BEGIN'     : 'TK_BEGIN',
        'END.'      : 'TK_END_DOT',
        'END;'      : 'TK_END',
        ','         : 'TK_COMMA',
        'IF'        : 'TK_IF',
        'THEN'      : 'TK_THEN',
        'ELSE'      : 'TK_ELSE',
        'FOR'       : 'TK_FOR',
        'TO'        : 'TK_TO',
        'DO'        : 'TK_DO',
        'CASE'      : 'TK_CASE'
        'OF'        : 'TK_OF',
        'REPEAT'    : 'TK_REPEAT',
        'UNTIL'     : 'TK_UNTIL',
        'WHILE'     : 'TK_WHILE',
        ';'         : 'TK_SEMICOLON',            
        ':'         : 'TK_COLON',
        '='         : 'TK_EQUAL',
        '<'         : 'TK_LESS',
        '>'         : 'TK_GREATER',
        '<='        : 'TK_LESS_EQUAL',
        '>='        : 'TK_GREATER_EQUAL',
        ':='        : 'TK_ASSIGNMENT',
        '+'         : 'TK_ADD',
        '-'         : 'TK_MINUS',
        '*'         : 'TK_MULT',
        '/'         : 'TK_DIV',
        'DIV'       : 'TK_DIV_FLOAT',
        'MOD'       : 'TK_MOD',
        'AND'       : 'TK_AND',
        'OR'        : 'TK_OR',
        'NOT'       : 'TK_NOT',
        '('         : 'TK_OPEN_PARENTHESIS',
        ')'         : 'TK_CLOSE_PARENTHESIS',
        'WRITELN'   : 'TK_WRITELN',
        'READLN'    : 'TK_READLN'
    }          
    
