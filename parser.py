class Parser(object):
	def __init__(self, alist, cur_token, nodes=[], d_nodes=[], sym_table=[]):
		self.alist = alist
		self.cur_token = cur_token
		self.iterator = self.setup_iterator()
		self.d_nodes = d_nodes
		self.nodes = nodes
		self.sym_table = sym_table

	def parse(self):
		self.retrieve()
		print "nodes: "+str(self.nodes)
		print "dnodes: "+str(self.d_nodes)

	def setup_iterator(self):
		tokens = iter(self.alist)
		return tokens

	def get_token(self):
		self.cur_token = self.iterator.next()
		return

	def retrieve(self):
		self.get_token()
		#self.var_declaration()
		self.program()
		#self.expression()
		#self.write_statement()
		#self.assignment()		
		#for test purposes
		if self.cur_token[0] == 'TK_SEMICOLON':
			return

	def match(self, t):
		#print str(self.cur_token) + ":" +str(t)
		if (self.cur_token[0] == t):
			#if match, generate code/ store to list
			if (self.cur_token[1] == ')' or self.cur_token[1] == '('):
				pass
			else:
				self.nodes.append(self.cur_token[1])
			#get next token
			self.get_token()
			return True
		else:
			#error
			print "error"

	def error_msg(self, t):
		#function to throw error msg for token
		print "error, expected token: %s, and received token: %s" %(t, self.cur_token[0])


	###############################
	#							  #
	# Program 		  	 		  #
	#							  #
	###############################
	def program(self):
		if self.cur_token[0] == 'TK_PROGRAM':
			self.match('TK_PROGRAM')

	###############################
	#							  #
	# Var declaration	   		  #
	#							  #
	###############################
	#def var_declaration(self):
		#parse VAR
	#	if self.cur_token[0] == 'TK_VAR':
	#		self.match('TK_VAR')

	#	while (True):
	#		if self.cur_token[0] == 'TK_IDENTIFIER':
	#			self.match('TK_IDENTIFIER')
	#		elif self.cur_token[0] == 'TK_COMMA':
	#			self.match('TK_COMMA')
	#		elif self.cur_token[0] == 'TK_COLON':
	#			self.match('TK_COLON')
	#			break
	#	if self.cur_token[0] == 'TK_ID_INTEGER':
	#		match('TK_ID_INTEGER')


	###############################
	#							  #
	# Write Statement    		  #
	#							  #
	###############################

	def write_statement(self):
		if self.cur_token[0] == 'TK_WRITELN':
			self.match('TK_WRITELN')
			self.match('TK_OPEN_PARENTHESIS')
			self.expression()
			self.match('TK_CLOSE_PARENTHESIS')
			self.postfix('TK_WRITELN')

	###############################
	#							  #
	# Assignment		   		  #
	#							  #
	###############################
	def assignment(self):
		#handles := 
		if self.cur_token[0] == 'TK_ASSIGNMENT':
			print self.cur_token
			self.match('TK_ASSIGNMENT')
			self.expression()
		

	###############################
	#							  #
	# Grammar					  #
	#							  #
	###############################
	
	# E --> TE'
	def expression(self):
		self.term()
		self.expression_prime()

	# T --> FT'
	def term(self):
		self.factor()
		self.term_prime()

	# E' --> +T[+]E' | -T[-]E' | e
	def expression_prime(self):
		if self.cur_token[0] == 'TK_ADD':
			self.match('TK_ADD')
			self.term()
			self.postfix('TK_ADD')			
			self.expression_prime()
		elif self.cur_token[0] == 'TK_MINUS':
			self.match('TK_MINUS')
			self.term()
			self.postfix('TK_MINUS')
			self.expression_prime()
		else:
			pass

	# T' --> *F[*]T' | /F[/]T' | modFT'|e
	def term_prime(self):
		if self.cur_token[0] == 'TK_MULT':
			self.match('TK_MULT')
			self.factor()
			self.postfix('TK_MULT')
			self.term_prime()
		elif self.cur_token[0] == 'TK_DIV':
			self.match('TK_DIV')
			self.factor()
			self.postfix('TK_DIV')
			self.term_prime()
		elif self.cur_token[0] == 'TK_MOD':
			self.match('TK_MOD')
			self.factor()
			self.postfix('TK_MOD')
			self.term_prime()
		else:
			pass

	# F --> id
	def factor(self):
		if self.cur_token[0] == 'TK_IDENTIFIER':
			self.postfix(self.cur_token)
			self.match('TK_IDENTIFIER')

		if self.cur_token[0] == 'TK_INTEGER':
			self.postfix(self.cur_token)
			self.match('TK_INTEGER')

	def postfix(self, t):
		#print "current_token: "+ str(self.cur_token) +" or t:" + str(t)

		if t == 'TK_ADD':
			self.d_nodes.append({'value':'+', 'type' :t})
		elif t == 'TK_MINUS':
			self.d_nodes.append({'value':'-', 'type' :t})
		elif t == 'TK_MULT':
			self.d_nodes.append({'value':'*', 'type' :t})
		elif t == 'TK_DIV':
			self.d_nodes.append({'value':'/', 'type' :t})
		elif t == 'TK_MOD':
			self.d_nodes.append({'value':'mod', 'type' :t})
		elif t[0] == 'TK_IDENTIFIER':
			self.d_nodes.append({'value':self.cur_token[1], 'type' :self.cur_token[0]})
		elif t[0] == 'TK_INTEGER':
			self.d_nodes.append({'value':self.cur_token[1], 'type' :self.cur_token[0]})		
		elif t == 'TK_WRITELN':
			self.d_nodes.append({'value': 'writeln', 'type': t})
		else:
			pass


if __name__ == '__main__':

	#Open file
	#alist = [('TK_INTEGER', '2', 1, 1), ('TK_ADD', '+', 1, 3), ('TK_INTEGER', '3', 1, 5), ('TK_SEMICOLON', ';', 1, 6)]
	#alist = [('TK_INTEGER', '2', 1, 1), ('TK_DIV', '/', 1, 3), ('TK_INTEGER', '3', 1, 5), ('TK_SEMICOLON', ';', 1, 6)]
	#alist = [('TK_INTEGER', '2', 1, 1), ('TK_MULT', '*', 1, 3), ('TK_INTEGER', '4', 1, 5), ('TK_MINUS', '-', 1, 7), ('TK_INTEGER', '6', 1, 9), ('TK_MULT', '*', 1, 11), ('TK_INTEGER', '3', 1, 7), ('TK_SEMICOLON', ';', 1, 6)]
	#alist = [('TK_WRITELN', 'writeln', 1, 7), ('TK_OPEN_PARENTHESIS', '(', 1, 8), ('TK_IDENTIFIER', 'b', 1, 9), ('TK_CLOSE_PARENTHESIS', ')', 1, 10), ('TK_SEMICOLON', ';', 1, 11)]
	#alist = [('TK_IDENTIFIER', 'a', 1, 1), ('TK_MOD', 'mod', 1, 3), ('TK_INTEGER', '3', 1, 5), ('TK_SEMICOLON', ';', 1, 6)]
	#alist = [('TK_WRITELN', 'writeln', 1, 7), ('TK_OPEN_PARENTHESIS', '(', 1, 8), ('TK_INTEGER', '1', 1, 9), ('TK_ADD', '+', 1, 10), ('TK_INTEGER', '1', 1, 11), ('TK_CLOSE_PARENTHESIS', ')', 1, 12), ('TK_SEMICOLON', ';', 1, 13)]
	#alist = [('TK_WRITELN', 'writeln', 1, 7), ('TK_OPEN_PARENTHESIS', '(', 1, 8), ('TK_IDENTIFIER', 'b', 1, 9), ('TK_CLOSE_PARENTHESIS', ')', 1, 12), ('TK_SEMICOLON', ';', 1, 13)]
	#alist = [('TK_IDENTIFIER', 'x', 1, 1), ('TK_ASSIGNMENT', ':=', 1, 4), ('TK_INTEGER', '2', 1, 6), ('TK_SEMICOLON', ';', 1, 7)]
	#alist = [('TK_VAR', 'var', 1, 3), ('TK_IDENTIFIER', 'x', 1, 4), ('TK_COLON', ':', 1, 6), ('TK_ID_INTEGER', 'integer', 1, 14), ('TK_SEMICOLON', ';', 1, 15)]
	alist = [('TK_PROGRAM', 'program', 1, 7), ('TK_IDENTIFIER', 'WORLDO', 1, 14), ('TK_SEMICOLON', ';', 1, 15), ('TK_VAR', 'var', 1, 20), ('TK_IDENTIFIER', 'x:', 1, 23), ('TK_ID_INTEGER', 'integer', 1, 31), ('TK_SEMICOLON', ';', 1, 32), ('TK_BEGIN', 'begin', 1, 39), ('TK_OPEN_PARENTHESIS', '(', 1, 48), ('TK_WRITELN', 'writeln', 1, 49), ('TK_STRING', "'helloworld'", 1, 62), ('TK_CLOSE_PARENTHESIS', ')', 1, 64), ('TK_SEMICOLON', ';', 1, 65), ('TK_END_CODE', 'end.', 1, 70)]

	#get_token(alist)
	a = Parser(alist, 0)
	a.parse()
