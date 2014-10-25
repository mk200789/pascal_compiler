class Parser(object):
	def __init__(self, alist):
		self.alist = alist

	def parse(self):
		self.retrieve()

	def get_token(self, alist):
		t = iter(self.alist)
		size = len(self.alist)
		while (size):
			print next(t)
			print size
			size -=1

	def retrieve(self):
		self.get_token(self.alist)

if __name__ == '__main__':

	#Open file
	alist = [('TK_PROGRAM', 'program', 1, 7), ('TK_IDENTIFIER', 'AddExample', 1, 18), ('TK_SEMICOLON', ';', 1, 19)]

	#get_token(alist)
	a = Parser(alist)
	a.parse()