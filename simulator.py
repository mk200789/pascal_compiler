	#code for simulator will be placed here
class Simulator(object):
	def __init__(self, symtable, d_nodes, stack = []):
		self.symtable = symtable
		self.d_nodes = d_nodes
		self.stack = stack


	def simulate(self, d_nodes):
		for d in d_nodes:
			if d['instruction'] == 'push':
				if d['type'] == 'IDENTIFIER':
					print "pushi"
				else:
					print "push"

	#def push(self):
		#



#if __name__ == '__main__':
