class Parser(object):
	def __init__(self, alist, cur_token):
		self.alist = alist
		self.cur_token = cur_token
		self.iterator = self.setup_iterator()

	def parse(self):
		self.get_token()


	def setup_iterator(self):
		tokens = iter(self.alist)
		return tokens

	def get_token(self):
		self.cur_token = self.iterator.next()
		return

	#def retrieve(self):
	#	self.get_token()


if __name__ == '__main__':

	#Open file
	alist = [('TK_PROGRAM', 'program', 1, 7), ('TK_IDENTIFIER', 'AddExample', 1, 18), ('TK_SEMICOLON', ';', 1, 19)]

	#get_token(alist)
	a = Parser(alist, 0)
	a.parse()