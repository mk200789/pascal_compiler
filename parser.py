def get_token(alist):
	#get token information
	for x in alist:
		print x

if __name__ == '__main__':

	#Open file
	alist = [('TK_PROGRAM', 'program', 1, 7), ('TK_IDENTIFIER', 'AddExample', 1, 18), ('TK_SEMICOLON', ';', 1, 19)]

	get_token(alist)