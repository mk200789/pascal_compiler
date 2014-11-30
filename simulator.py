#code for simulator will be placed here
class Simulator(object):
	def __init__(self, symtable, d_nodes):
		self.symtable = symtable
		self.d_nodes = d_nodes


	def simulate(self, d_nodes):
		for d in d_nodes:
			if d['instruction'] == 'push':
				if d['type'] == 'IDENTIFIER':
					print "pushi"
				else:
					print "push"



#if __name__ == '__main__':
