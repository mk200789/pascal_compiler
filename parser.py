class Parser(object):
	def __init__(self, alist, cur_token, nodes=[], d_nodes=[]):
		self.alist = alist
		self.cur_token = cur_token
		self.iterator = self.setup_iterator()
		self.d_nodes = d_nodes
		self.nodes = nodes	

	def parse(self):
		self.retrieve()

	def setup_iterator(self):
		tokens = iter(self.alist)
		return tokens

	def get_token(self):
		self.cur_token = self.iterator.next()
		return

	def retrieve(self):
		self.get_token()
		#self.expression()
		#for test purposes
		if self.cur_token[0] == 'TK_SEMICOLON':
			return

	def match(self, t):
		if (self.cur_token[0] == t):
			#get next token
			self.nodes.append(self.cur_token[1])
			self.get_token()
			return
		else:
			#error
			print "error"

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

	# T' --> *F[*]T' | /F[/]T' | e
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
		if t == 'TK_ADD':
			self.d_nodes.append('+')
		elif t == 'TK_MINUS':
			self.d_nodes.append('-')
		elif t == 'TK_MULT':
			self.d_nodes.append('*')
		elif t == 'TK_DIV':
			self.d_nodes.append('/')
		elif t[0] == 'TK_IDENTIFIER':
			self.d_nodes.append(self.cur_token[1])
		elif t[0] == 'TK_INTEGER':
			self.d_nodes.append(self.cur_token[1])
		else:
			pass


if __name__ == '__main__':

	#Open file
	#alist = [('TK_INTEGER', '2', 1, 1), ('TK_DIV', '/', 1, 3), ('TK_INTEGER', '3', 1, 5), ('TK_SEMICOLON', ';', 1, 6)]
	alist = [('TK_INTEGER', '2', 1, 1), ('TK_MULT', '*', 1, 3), ('TK_INTEGER', '4', 1, 5), ('TK_MINUS', '-', 1, 7), ('TK_INTEGER', '6', 1, 9), ('TK_MULT', '*', 1, 11), ('TK_INTEGER', '3', 1, 7), ('TK_SEMICOLON', ';', 1, 6)]

	#get_token(alist)
	a = Parser(alist, 0)
	a.parse()