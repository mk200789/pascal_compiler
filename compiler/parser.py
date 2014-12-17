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
		#count = 1
		#for row in self.d_nodes:
		#	print str(count)+ " :  "+str(row)
		#	count +=1
		return {'symtable': self.sym_table, 'd_nodes': self.d_nodes}

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
				self.sym_table.append({'NAME': self.cur_token[1], 'ADDRESS': self.address, 'TYPE': 'none', 'VALUE': 0})
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
					v['TYPE'] = 'int'
			self.match('TK_ID_INTEGER')

		if self.cur_token[0] == 'TK_ID_STRING':
			#print "MATCHED TK_ID_STRING current token :" + str(self.cur_token)
			for v in self.sym_table:
				if v['TYPE'] == 'none':
					v['TYPE'] = 'str'
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
				self.d_nodes.append({'instruction': 'halt', 'ip': self.ip, 'value': self.cur_token[1]})
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
			
			if self.cur_token[0] == 'TK_IDENTIFIER':
				self.lhs = self.cur_token
				#print "MATCHED with current token: " + str(self.cur_token)
				self.match('TK_IDENTIFIER')
				self.expression()

			#<for do statement> -- > for <initial condition> to <final value> do <begin statement>
			#if self.cur_token[0] == 'TK_FOR':
			#	self.for_do()

			#<repeat statement> --> repeat <statement> until <condition>
			if self.cur_token[0] == 'TK_REPEAT':
				self.repeat_loop()

			#<while statement> --> while <condition> do <statement>
			if self.cur_token[0] == 'TK_WHILE':
				self.while_loop()

			#<write statement> --> write (<expression>)			
			if self.cur_token[0] == 'TK_WRITELN':
				self.write_statement()	

			#<if-else statement> --> IF <condifiton> THEN <statement> ELSE <statement>
			if self.cur_token[0] == 'TK_IF':
				self.if_statement()


			if self.cur_token[0] =='TK_ASSIGNMENT':
				#print "MATCHED with current token: " + str(self.cur_token)
				self.match('TK_ASSIGNMENT')
				self.expression()
				#self.d_nodes.append({'instruction': 'pop', 'value':self.lhs[1], 'type': self.lhs[0]})
				self.op = True

				
			if self.cur_token[0] == 'TK_SEMICOLON':
				#print "MATCHED with current token: " + str(self.cur_token)
				self.match('TK_SEMICOLON')
				#self.var_declaration()
				if self.op:
					#print "{ instruction: 'pop', value:  "+ str(self.lhs[1])+", ip: "+ str(self.ip)+"}"
					#print self.cur_token
					self.d_nodes.append({'instruction': 'pop', 'value':self.lhs[1], 'ip': self.ip})
					self.ip += 1
					self.op = False
				self.var_declaration()
			
			if self.cur_token[0] == 'TK_UNTIL':
				return

			if self.cur_token[0] == 'TK_ELSE':
				return

			if self.cur_token[0] == 'TK_END_DOT' or self.cur_token[0] == 'TK_END':
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
		elif self.cur_token[0] == 'TK_GREATER':
			self.match('TK_GREATER')
			self.expression()
			self.postfix('TK_GREATER')
		elif self.cur_token[0] == 'TK_LESS_EQUAL':
			self.match('TK_LESS_EQUAL')
			self.expression()
			self.postfix('TK_LESS_EQUAL')
		elif self.cur_token[0] == 'TK_GREATER_EQUAL':
			self.match('TK_GREATER_EQUAL')
			self.expression()
			self.postfix('TK_GREATER_EQUAL')
		else:
			self.expression()

	def for_do(self):
		#function for for do loop

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
		self.d_nodes.append({'instruction': 'jmp', 'ip':self.ip, 'value': target})
		self.ip += 1
		self.d_nodes[hole]['value'] = self.ip

	def if_statement(self):
		#print "if statement"
		self.match('TK_IF')
		self.match('TK_OPEN_PARENTHESIS')
		self.expression()
		self.rel_operators()
		self.match('TK_CLOSE_PARENTHESIS')
		self.match ('TK_THEN')
		#ip hole for condition true
		#print self.ip
		hole1 = self.ip
		self.d_nodes.append({'instruction': 'jFalse', 'ip': self.ip, 'value': 0})
		self.ip += 1
		self.statements()

		if self.cur_token[0] == 'TK_ELSE':
			#print "TK_ELSE MAN"
			#print self.ip
			self.match('TK_ELSE')
			hole2 = self.ip 
			self.d_nodes.append({'instruction': 'jmp', 'ip': self.ip, 'value': 0})
			self.ip += 1
			self.statements()
			#print self.ip
			self.d_nodes[hole1]['value'] = self.ip
			self.d_nodes[hole2]['value'] = self.ip
		

	def write_statement(self):
		if self.cur_token[0] == 'TK_WRITELN':
			self.match('TK_WRITELN')
			self.match('TK_OPEN_PARENTHESIS')
			#print "curip writestatement" +str(self.ip)
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
		#print self.cur_token
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
		elif t == 'TK_GREATER':
			self.d_nodes.append({'instruction': 'greater', 'value': 'greater', 'type': t, 'ip':self.ip})
		elif t == 'TK_GREATER_EQUAL':
			self.d_nodes.append({'instruction': 'gtr_equal', 'value': 'gtr_equal', 'type': t, 'ip':self.ip})
		elif t == 'TK_LESS_EQUAL':
			self.d_nodes.append({'instruction': 'lss_equal', 'value': 'lss_eq', 'type': t, 'ip':self.ip})
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
