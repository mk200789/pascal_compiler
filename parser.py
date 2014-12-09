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
		self.ip = 0
		self.op = False

		self.temp = False

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
		print "MATCH FUNCTION: "+ str(self.cur_token) + ":" +str(t)
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
			#print "MATCHED TK_PROGRAM"
			self.match('TK_PROGRAM')
			self.declarations()
			self.begin_statement()
			#if self.cur_token[0] == 'TK_END_DOT':
			#	self.nodes.append(self.cur_token[1])

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
		#print "DECLARATION()"
		self.var_declaration()
		return

	###############################
	#							  #
	# Var declaration	   		  #
	#							  #
	###############################
	#<var declaration> -->

	def var_declaration(self):
		#parse VAR
		#print "VAR_DECLARATION(). current token :" + str(self.cur_token)
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
			#print "MATCHED TK_BEGIN current token :" + str(self.cur_token)
			self.match('TK_BEGIN')
		if self.cur_token[0] == 'TK_END_DOT':
			if not self.temp:
				self.d_nodes.append({'instruction': 'ophalt', 'ip': self.ip, 'value': self.cur_token[1]})
				self.temp = True
			return
		else:
			self.statements()


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
		#print "statements()"
		while(True):		
			#print "while1"
			if self.cur_token[0] == 'TK_IDENTIFIER':
				self.lhs = self.cur_token
				#print "MATCHED with current token: " + str(self.cur_token)
				self.match('TK_IDENTIFIER')
				self.expression()

			#<repeat statement> --> repeat <statement> until <condition>
			if self.cur_token[0] == 'TK_REPEAT':
				self.repeat_loop()

			#<while statement> --> while <condition> do <statement>
			if self.cur_token[0] == 'TK_WHILE':
				self.while_loop()

			#<write statement> --> write (<expression>)			
			if self.cur_token[0] == 'TK_WRITELN':
				self.write_statement()	

			if self.cur_token[0] == 'TK_IF':
				self.if_statement()


			if self.cur_token[0] =='TK_ASSIGNMENT':
				#print "MATCHED with current token: " + str(self.cur_token)
				self.match('TK_ASSIGNMENT')
				self.expression()
				#self.d_nodes.append({'instruction': 'pop', 'value':self.lhs[1], 'type': self.lhs[0]})
				self.op = True

			#print "while2"
			if self.cur_token[0] == 'TK_SEMICOLON':
				#print "MATCHED with current token: " + str(self.cur_token)
				self.match('TK_SEMICOLON')
				#self.var_declaration()
				if self.op:
					print "{ instruction: 'pop', value:  "+ str(self.lhs[1])+", ip: "+ str(self.ip)+"}"
					print self.cur_token
					self.d_nodes.append({'instruction': 'pop', 'value':self.lhs[1], 'ip': self.ip})
					self.ip += 1
					self.op = False
				self.var_declaration()
			
			if self.cur_token[0] == 'TK_UNTIL':
				#print self.d_nodes
				return

			if self.cur_token[0] == 'TK_ELSE':
				return

			#print "while3"
			if self.cur_token[0] == 'TK_END_DOT' or self.cur_token[0] == 'TK_END':
				#print "MATCHED with current token: " + str(self.cur_token)
				break

		return

	def rel_operators(self):
		#print "relational operators"
		if self.cur_token[0] == 'TK_EQUAL':
			self.match('TK_EQUAL')
			self.expression()
			self.postfix('TK_EQUAL')
		elif self.cur_token[0] == 'TK_LESS':
			self.match('TK_LESS')
			self.expression()
			self.postfix('TK_LESS')
		else:
			self.expression()

	def repeat_loop(self):
		self.match('TK_REPEAT')
		self.statements()
		self.match('TK_UNTIL')
		self.expression()
		self.rel_operators()
		self.d_nodes.append({'instruction': 'jFalse', 'ip': self.ip, 'value': self.ip })
		self.ip +=1

	def while_loop(self):
		self.match('TK_WHILE')
		target = self.ip
		self.expression()
		self.rel_operators()
		self.match('TK_DO')
		self.d_nodes.append({'instruction': 'jFalse', 'ip': self.ip, 'value': target})
		hole = self.ip
		self.ip += 1
		self.begin_statement()
		#self.statements()
		self.d_nodes.append({'instruction': 'jmp', 'ip':self.ip, 'value': target})
		self.ip += 1
		print "IPPATCH" + str(self.ip)
		self.d_nodes[hole]['value'] = self.ip

	def if_statement(self):
		print "if statement"
		self.match('TK_IF')
		self.match('TK_OPEN_PARENTHESIS')
		#ip hole for condition true
		hole1 = self.ip
		self.expression()
		self.rel_operators()
		self.cur_token
		self.match('TK_CLOSE_PARENTHESIS')
		self.match ('TK_THEN')
		self.statements()
		print "cur ip"+ str(self.ip)
		self.d_nodes.append({'instruction': 'jFalse', 'ip': self.ip, 'value': 0})
		self.ip += 1
		print "BYEBYE"

		if self.cur_token[0] == 'TK_ELSE':
			print "TK_ELSE MAN"
			self.match('TK_ELSE')
			hole2 = self.ip 
			self.statements()
			self.d_nodes.append({'instruction': 'jmp', 'ip': self.ip, 'value': 0})
			self.ip += 1
			self.d_nodes[hole1]['value'] = self.ip
			self.d_nodes[hole2]['value'] = self.ip
		

	def write_statement(self):
		if self.cur_token[0] == 'TK_WRITELN':
			self.match('TK_WRITELN')
			self.match('TK_OPEN_PARENTHESIS')
			print "curip writestatement" +str(self.ip)
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
		#print "expressions"
		print self.cur_token
		self.term()
		self.expression_prime()

	# T --> FT'
	def term(self):
		#print "term"
		self.factor()
		self.term_prime()

	# E' --> +T[+]E' | -T[-]E' | e
	def expression_prime(self):
		#print "expression prime"
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
		#print "term prime"
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
		elif self.cur_token[0] == 'TK_EQUAL':
			self.match('TK_EQUAL')
			self.postfix('TK_EQUAL')
			self.term_prime()
		else:
			pass

	# F --> id | lit | ( E ) | -F | +F | not F
	def factor(self):
		#print self.cur_token
		if self.cur_token[0] == 'TK_IDENTIFIER':
			self.postfix(self.cur_token)
			self.match('TK_IDENTIFIER')
			return

		if self.cur_token[0] == 'TK_STRING':
			self.postfix(self.cur_token)
			self.match('TK_STRING')
			return

		if self.cur_token[0] == 'TK_INTEGER':
			self.postfix(self.cur_token)
			self.match('TK_INTEGER')
			return

		if self.cur_token[0] == 'TK_NOT':
			self.match('TK_NOT')
			self.factor()
			self.postfix(self.cur_token)
			self.d_nodes.append({'instruction': 'not', 'value':'not', 'type':'TK_NOT'})
			return

	def postfix(self, t):
		#print "current_token: "+ str(self.cur_token) +" or t:" + str(t)

		if t == 'TK_ADD':
			self.d_nodes.append({'instruction': 'add','value':'+', 'type' :t, 'ip': self.ip})
		elif t == 'TK_MINUS':
			self.d_nodes.append({'instruction': 'minus','value':'-', 'type' :t, 'ip': self.ip})
		elif t == 'TK_MULT':
			self.d_nodes.append({'instruction': 'mult','value':'*', 'type' :t, 'ip':self.ip})
		elif t == 'TK_DIV':
			self.d_nodes.append({'instruction': 'div','value':'/', 'type' :t, 'ip':self.ip})
		elif t == 'TK_MOD':
			self.d_nodes.append({'instruction': 'mod','value':'mod', 'type' :t, 'ip':self.ip})
		elif t == 'TK_EQUAL':
			self.d_nodes.append({'instruction': 'pop', 'value':'equals', 'type': t, 'ip':self.ip})
		elif t == 'TK_LESS':
			self.d_nodes.append({'instruction': 'less', 'value': 'less', 'type': t, 'ip':self.ip})
		elif t[0] == 'TK_IDENTIFIER':
			self.d_nodes.append({'instruction': 'push','value':self.cur_token[1], 'type' :self.cur_token[0], 'ip':self.ip})
		elif t[0] == 'TK_STRING':
			self.d_nodes.append({'instruction': 'push', 'value':self.cur_token[1], 'type':self.cur_token[0], 'ip': self.ip})
		elif t[0] == 'TK_INTEGER':
			self.d_nodes.append({'instruction': 'push','value':self.cur_token[1], 'type' :self.cur_token[0], 'ip':self.ip})		
		elif t == 'TK_WRITELN':
			self.d_nodes.append({'instruction': 'writeln', 'value': 'writeln' ,'type': t, 'ip':self.ip})
		else:
			pass
		self.ip +=1


if __name__ == '__main__':
	
	#simple add program
	#alist =[('TK_PROGRAM', 'program', 1, 7), ('TK_IDENTIFIER', 'add', 1, 11), ('TK_SEMICOLON', ';', 1, 12), ('TK_BEGIN', 'begin', 2, 5), ('TK_IDENTIFIER', 'x', 3, 1), ('TK_ASSIGNMENT', ':=', 3, 4), ('TK_IDENTIFIER', 'x', 3, 6), ('TK_ADD', '+', 3, 7), ('TK_INTEGER', '4', 3, 10), ('TK_SEMICOLON', ';', 3, 11), ('TK_END_DOT', 'end.', 4, 4)]
	#repeat loop 
	#alist = [('TK_PROGRAM', 'program', 1, 7), ('TK_IDENTIFIER', 'repeatUntilLoop', 1, 23), ('TK_SEMICOLON', ';', 1, 24), ('TK_VAR', 'var', 2, 3), ('TK_IDENTIFIER', 'a', 2, 4), ('TK_COLON', ':', 2, 6), ('TK_ID_INTEGER', 'integer', 2, 14), ('TK_SEMICOLON', ';', 2, 15), ('TK_BEGIN', 'begin', 3, 5), ('TK_IDENTIFIER', 'a', 4, 4), ('TK_ASSIGNMENT', ':=', 4, 7), ('TK_INTEGER', '10', 4, 10), ('TK_SEMICOLON', ';', 4, 11), ('TK_REPEAT', 'repeat', 5, 9), ('TK_WRITELN', 'writeln', 6, 13), ('TK_OPEN_PARENTHESIS', '(', 6, 14), ('TK_IDENTIFIER', 'a', 6, 15), ('TK_CLOSE_PARENTHESIS', ')', 6, 16), ('TK_SEMICOLON', ';', 6, 17), ('TK_IDENTIFIER', 'a', 7, 7), ('TK_ASSIGNMENT', ':=', 7, 10), ('TK_IDENTIFIER', 'a', 7, 12), ('TK_ADD', '+', 7, 13), ('TK_INTEGER', '1', 7, 16), ('TK_SEMICOLON', ';', 7, 17), ('TK_UNTIL', 'until', 8, 8), ('TK_IDENTIFIER', 'a', 8, 10), ('TK_EQUAL', '=', 8, 12), ('TK_INTEGER', '20', 8, 15), ('TK_SEMICOLON', ';', 8, 16), ('TK_END_DOT', 'end.', 9, 4)]
	#while do loop
	#alist = [('TK_PROGRAM', 'program', 1, 7), ('TK_IDENTIFIER', 'whileLoop', 1, 17), ('TK_SEMICOLON', ';', 1, 18), ('TK_VAR', 'var', 2, 3), ('TK_IDENTIFIER', 'a', 2, 5), ('TK_COMMA', ',', 2, 6), ('TK_IDENTIFIER', 'b', 2, 7), ('TK_COLON', ':', 2, 9), ('TK_ID_INTEGER', 'integer', 2, 17), ('TK_SEMICOLON', ';', 2, 18), ('TK_BEGIN', 'begin', 3, 5), ('TK_IDENTIFIER', 'a', 4, 4), ('TK_ASSIGNMENT', ':=', 4, 7), ('TK_INTEGER', '10', 4, 10), ('TK_SEMICOLON', ';', 4, 11), ('TK_WHILE', 'while', 5, 8), ('TK_IDENTIFIER', 'a', 5, 11), ('TK_LESS', '<', 5, 13), ('TK_INTEGER', '20', 5, 16), ('TK_DO', 'do', 5, 20), ('TK_BEGIN', 'begin', 6, 8), ('TK_WRITELN', 'writeln', 7, 13), ('TK_OPEN_PARENTHESIS', '(', 7, 14), ('TK_IDENTIFIER', 'a', 7, 15), ('TK_CLOSE_PARENTHESIS', ')', 7, 16), ('TK_SEMICOLON', ';', 7, 17), ('TK_IDENTIFIER', 'a', 8, 7), ('TK_ASSIGNMENT', ':=', 8, 10), ('TK_IDENTIFIER', 'a', 8, 12), ('TK_ADD', '+', 8, 13), ('TK_INTEGER', '1', 8, 16), ('TK_SEMICOLON', ';', 8, 17), ('TK_END', 'end;', 9, 6), ('TK_END_DOT', 'end.', 10, 4)]
	#if else statement
	#alist = [('TK_PROGRAM', 'program', 1, 7), ('TK_IDENTIFIER', 'ifChecking', 1, 18), ('TK_SEMICOLON', ';', 1, 19), ('TK_VAR', 'var', 2, 3), ('TK_IDENTIFIER', 'a', 2, 4), ('TK_COLON', ':', 2, 6), ('TK_ID_INTEGER', 'integer', 2, 14), ('TK_SEMICOLON', ';', 2, 15), ('TK_BEGIN', 'begin', 3, 5), ('TK_IDENTIFIER', 'a', 4, 2), ('TK_ASSIGNMENT', ':=', 4, 5), ('TK_INTEGER', '100', 4, 9), ('TK_SEMICOLON', ';', 4, 10), ('TK_IF', 'if', 5, 3), ('TK_OPEN_PARENTHESIS', '(', 5, 5), ('TK_IDENTIFIER', 'a', 5, 7), ('TK_LESS', '<', 5, 9), ('TK_INTEGER', '20', 5, 12), ('TK_CLOSE_PARENTHESIS', ')', 5, 13), ('TK_THEN', 'then', 5, 18), ('TK_WRITELN', 'writeln', 6, 9), ('TK_OPEN_PARENTHESIS', '(', 6, 10), ('TK_STRING', "'hello'", 6, 17), ('TK_CLOSE_PARENTHESIS', ')', 6, 18), ('TK_END_DOT', 'end.', 7, 4)]
	alist = [('TK_PROGRAM', 'program', 1, 7), ('TK_IDENTIFIER', 'ifChecking', 1, 18), ('TK_SEMICOLON', ';', 1, 19), ('TK_VAR', 'var', 2, 3), ('TK_IDENTIFIER', 'a', 2, 4), ('TK_COLON', ':', 2, 6), ('TK_ID_INTEGER', 'integer', 2, 14), ('TK_SEMICOLON', ';', 2, 15), ('TK_BEGIN', 'begin', 3, 5), ('TK_IDENTIFIER', 'a', 4, 2), ('TK_ASSIGNMENT', ':=', 4, 5), ('TK_INTEGER', '100', 4, 9), ('TK_SEMICOLON', ';', 4, 10), ('TK_IF', 'if', 5, 3), ('TK_OPEN_PARENTHESIS', '(', 5, 5), ('TK_IDENTIFIER', 'a', 5, 7), ('TK_LESS', '<', 5, 9), ('TK_INTEGER', '20', 5, 12), ('TK_CLOSE_PARENTHESIS', ')', 5, 13), ('TK_THEN', 'then', 5, 18), ('TK_WRITELN', 'writeln', 6, 9), ('TK_OPEN_PARENTHESIS', '(', 6, 10), ('TK_STRING', "'hello'", 6, 17), ('TK_CLOSE_PARENTHESIS', ')', 6, 18), ('TK_ELSE', 'else', 7, 5), ('TK_WRITELN', 'writeln', 8, 9), ('TK_OPEN_PARENTHESIS', '(', 8, 10), ('TK_IDENTIFIER', 'a', 8, 11), ('TK_CLOSE_PARENTHESIS', ')', 8, 12), ('TK_END_DOT', 'end.', 9, 4)]

	#get_token(alist)
	a = Parser(alist, 0)
	a.parse()
