def get_token(alist):
	#get token information
	#for x in alist:
	#	print x
	t = iter(alist)
	size = len(alist)
	while (size):
		print next(t)
		size -=1

if __name__ == '__main__':

	#Open file
	alist = [('TK_PROGRAM', 'program', 1, 7), ('TK_IDENTIFIER', 'AddExample', 1, 18), ('TK_SEMICOLON', ';', 1, 19)]

	get_token(alist)