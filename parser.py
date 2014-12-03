class Parser(object):
	def __init__(self, alist, cur_token, nodes=[], d_nodes=[], sym_table=[], address =0, lhs='', rhs =''):
		self.alist = alist
		self.cur_token = cur_token
		self.iterator = self.setup_iterator()
		self.d_nodes = d_nodes
		self.nodes = nodes
		self.sym_table = sym_table
		self.address = address
		self.lhs = lhs
		self.rhs = rhs

	def parse(self):
		self.retrieve()
		print "nodes: "+str(self.nodes)
		#print "dnodes: "+str(self.d_nodes)
		count = 1
		for row in self.d_nodes:
			print str(count)+ " :  "+str(row)
			count +=1
		print "sym_table: "+str(self.sym_table)

	def setup_iterator(self):
		tokens = iter(self.alist)
		return tokens

	def get_token(self):
		self.cur_token = self.iterator.next()
		return

	def retrieve(self):
		self.get_token()
		#self.expression()
		self.program()

	def match(self, t):
		#print "MATCH FUNCTION: "+ str(self.cur_token) + ":" +str(t)
		if (self.cur_token[0] == t):
			#if match, generate code/ store to list
			if (self.cur_token[1] == ')' or self.cur_token[1] == '('):
				pass
			else:
				self.nodes.append(self.cur_token[1])
			#get next token
			self.get_token()
			#print self.cur_token
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
	#<program> -->
	#				<declarations>
	#				<begin statement>
	#				<halt>
	def program(self):
		if self.cur_token[0] == 'TK_PROGRAM':
			print "MATCHED TK_PROGRAM"
			self.match('TK_PROGRAM')
			self.declarations()
			self.begin_statement()
			if self.cur_token[0] == 'TK_END_DOT':
				self.nodes.append(self.cur_token[1])

	###############################
	#							  #
	# Declarations	  	 		  #
	#							  #
	###############################
	#<declarations>	-->
	#					<var declaration>
	#					<label declaration>
	#					<procedure ..>
	#					<functions ..>
	def declarations(self):
		print "DECLARATION()"
		self.var_declaration()

	###############################
	#							  #
	# Var declaration	   		  #
	#							  #
	###############################
	#<var declaration> -->

	def var_declaration(self):
		#parse VAR
		print "VAR_DECLARATION(). current token :" + str(self.cur_token)
		if self.cur_token[0] == 'TK_VAR':
			#print "MATCHED TK_VAR"
			self.match('TK_VAR')
		else:
			self.begin_statement()
			return

		#print "var declaration"
		while (True):
			if self.cur_token[0] == 'TK_IDENTIFIER':
				#print "MATCHED TK_IDENTIFIER current token :" + str(self.cur_token)
				self.sym_table.append({'NAME': self.cur_token[1], 'ADDRESS': self.address, 'TYPE': 'none'})
				self.match('TK_IDENTIFIER')
				self.address += 4
			elif self.cur_token[0] == 'TK_COMMA':
				#print "MATCHED TK_COMMA current token :" + str(self.cur_token)
				self.match('TK_COMMA')
			elif self.cur_token[0] == 'TK_COLON':
				#print "MATCHED TK_COLON current token :" + str(self.cur_token)
				self.match('TK_COLON')
				break

		if self.cur_token[0] == 'TK_ID_INTEGER':
			#print "MATCHED TK_ID_INTEGER current token :" + str(self.cur_token)
			for v in self.sym_table:
				if v['TYPE'] == 'none':
					v['TYPE'] = 'integer'
			self.match('TK_ID_INTEGER')

		if self.cur_token[0] == 'TK_ID_STRING':
			#print "MATCHED TK_ID_STRING current token :" + str(self.cur_token)
			for v in self.sym_table:
				if v['TYPE'] == 'none':
					v['TYPE'] = 'string'
			self.match('TK_ID_STRING')

		if self.cur_token[0] == 'TK_SEMICOLON':
			#print "MATCHED TK_SEMICOLON current token :" + str(self.cur_token)
			self.match('TK_SEMICOLON')

		self.var_declaration()


	###############################
	#							  #
	# Begin statements			  #
	#							  #
	###############################
	#<begin-statement> -->
	#						begin <statements> end
	def begin_statement(self):
		if self.cur_token[0] == 'TK_BEGIN':
			print "MATCHED TK_BEGIN current token :" + str(self.cur_token)
			self.match('TK_BEGIN')
		self.statements()
		return


	###############################
	#							  #
	# Statements				  #
	#							  #
	###############################	
	#<statements> -->
	#					<while statement>
	#					<for statement>
	#					<goto statement>
	#					<repeat statement>
	#					<if statement>
	#					<case statement>
	#					<assignment statement>
	#					<proc call statement>
	def statements(self):
		print "statements()"
		while(True):		
			#print "while1"
			if self.cur_token[0] == 'TK_IDENTIFIER':
				self.lhs = self.cur_token
				print "MATCHED with current token: " + str(self.cur_token)
				self.match('TK_IDENTIFIER')
				self.expression()

			if self.cur_token[0] =='TK_ASSIGNMENT':
				print "MATCHED with current token: " + str(self.cur_token)
				self.match('TK_ASSIGNMENT')
				self.expression()
				self.d_nodes.append({'instruction': 'pop', 'value':self.lhs[1], 'type': self.lhs[0]})

			#print "while2"
			if self.cur_token[0] == 'TK_SEMICOLON':
				print "MATCHED with current token: " + str(self.cur_token)
				self.match('TK_SEMICOLON')
				self.var_declaration()

			#print "while3"
			if self.cur_token[0] == 'TK_END_DOT':
				#print "MATCHED with current token: " + str(self.cur_token)
				break

		return

	###############################
	#							  #
	# Write Statement    		  #
	#							  #
	###############################
	#<write statement> -->
	#						write (<expression>)

	def write_statement(self):
		if self.cur_token[0] == 'TK_WRITELN':
			self.match('TK_WRITELN')
			self.match('TK_OPEN_PARENTHESIS')
			self.expression()
			self.match('TK_CLOSE_PARENTHESIS')
			self.postfix('TK_WRITELN')


	###############################
	#							  #
	# Grammar					  #
	#							  #
	###############################
	
	# E --> TE'
	def expression(self):
		print "expressions"
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

	# F --> id | lit | ( E ) | -F | +F | not F
	def factor(self):
		print self.cur_token
		if self.cur_token[0] == 'TK_IDENTIFIER':
			self.postfix(self.cur_token)
			self.match('TK_IDENTIFIER')
			return

		if self.cur_token[0] == 'TK_INTEGER':
			self.postfix(self.cur_token)
			self.match('TK_INTEGER')
			return

		if self.cur_token[0] == 'TK_NOT':
			print "TK_NOT"
			self.match('TK_NOT')
			self.factor()
			self.postfix(self.cur_token)
			self.d_nodes.append({'instruction': 'not', 'value':'not', 'type':'TK_NOT'})
			return

	def postfix(self, t):
		#print "current_token: "+ str(self.cur_token) +" or t:" + str(t)

		if t == 'TK_ADD':
			self.d_nodes.append({'instruction': 'add','value':'+', 'type' :t})
		elif t == 'TK_MINUS':
			self.d_nodes.append({'instruction': 'minus','value':'-', 'type' :t})
		elif t == 'TK_MULT':
			self.d_nodes.append({'instruction': 'mult','value':'*', 'type' :t})
		elif t == 'TK_DIV':
			self.d_nodes.append({'instruction': 'div','value':'/', 'type' :t})
		elif t == 'TK_MOD':
			self.d_nodes.append({'instruction': 'mod','value':'mod', 'type' :t})
		elif t[0] == 'TK_IDENTIFIER':
			self.d_nodes.append({'instruction': 'push','value':self.cur_token[1], 'type' :self.cur_token[0]})
		elif t[0] == 'TK_INTEGER':
			self.d_nodes.append({'instruction': 'push','value':self.cur_token[1], 'type' :self.cur_token[0]})		
		elif t == 'TK_WRITELN':
			self.d_nodes.append({'value': 'writeln', 'type': t})
		else:
			pass


if __name__ == '__main__':
	
	#alist = [('TK_PROGRAM', 'program', 1, 7), ('TK_IDENTIFIER', 'helloW', 1, 14), ('TK_SEMICOLON', ';', 1, 15), ('TK_VAR', 'var', 3, 3), ('TK_IDENTIFIER', 'x', 3, 4), ('TK_COLON', ':', 3, 6), ('TK_ID_INTEGER', 'integer', 3, 14), ('TK_SEMICOLON', ';', 3, 15), ('TK_VAR', 'var', 4, 3), ('TK_IDENTIFIER', 'a', 4, 5), ('TK_COMMA', ',', 4, 6), ('TK_IDENTIFIER', 'b', 4, 8), ('TK_COMMA', ',', 4, 9), ('TK_IDENTIFIER', 'c', 4, 10), ('TK_COLON', ':', 4, 12), ('TK_ID_INTEGER', 'integer', 4, 20), ('TK_SEMICOLON', ';', 4, 21), ('TK_BEGIN', 'begin', 5, 5), ('TK_IDENTIFIER', 'x', 6, 1), ('TK_ADD', '+', 6, 2), ('TK_INTEGER', '4', 6, 5), ('TK_SEMICOLON', ';', 6, 6), ('TK_END_DOT', 'end.', 7, 4)]
	alist = [('TK_PROGRAM', 'program', 1, 7), ('TK_IDENTIFIER', 'helloW', 1, 14), ('TK_SEMICOLON', ';', 1, 15), ('TK_VAR', 'var', 3, 3), ('TK_IDENTIFIER', 'x', 3, 4), ('TK_COLON', ':', 3, 6), ('TK_ID_INTEGER', 'integer', 3, 14), ('TK_SEMICOLON', ';', 3, 15), ('TK_VAR', 'var', 4, 3), ('TK_IDENTIFIER', 'a', 4, 5), ('TK_COMMA', ',', 4, 6), ('TK_IDENTIFIER', 'b', 4, 8), ('TK_COMMA', ',', 4, 9), ('TK_IDENTIFIER', 'c', 4, 10), ('TK_COLON', ':', 4, 12), ('TK_ID_INTEGER', 'integer', 4, 20), ('TK_SEMICOLON', ';', 4, 21), ('TK_BEGIN', 'begin', 5, 5), ('TK_IDENTIFIER', 'x', 6, 1), ('TK_ASSIGNMENT', ':=', 6, 4), ('TK_NOT', 'not', 6, 8), ('TK_IDENTIFIER', 'b', 6, 10), ('TK_SEMICOLON', ';', 6, 11), ('TK_END_DOT', 'end.', 7, 4)]
	#alist = [('TK_PROGRAM', 'program', 1, 7), ('TK_IDENTIFIER', 'helloW', 1, 14), ('TK_SEMICOLON', ';', 1, 15), ('TK_VAR', 'var', 3, 3), ('TK_IDENTIFIER', 'x', 3, 4), ('TK_COLON', ':', 3, 6), ('TK_ID_INTEGER', 'integer', 3, 14), ('TK_SEMICOLON', ';', 3, 15), ('TK_VAR', 'var', 4, 3), ('TK_IDENTIFIER', 'a', 4, 5), ('TK_COMMA', ',', 4, 6), ('TK_IDENTIFIER', 'b', 4, 8), ('TK_COMMA', ',', 4, 9), ('TK_IDENTIFIER', 'c', 4, 10), ('TK_COLON', ':', 4, 12), ('TK_ID_INTEGER', 'integer', 4, 20), ('TK_SEMICOLON', ';', 4, 21), ('TK_BEGIN', 'begin', 5, 5), ('TK_IDENTIFIER', 'x', 6, 1), ('TK_ASSIGNMENT', ':=', 6, 4), ('TK_IDENTIFIER', 'a', 6, 6), ('TK_MULT', '*', 6, 7), ('TK_IDENTIFIER', 'b', 6, 10), ('TK_SEMICOLON', ';', 6, 11), ('TK_END_DOT', 'end.', 7, 4)]

	#get_token(alist)
	a = Parser(alist, 0)
	a.parse()
