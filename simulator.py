	#code for simulator will be placed here
class Simulator(object):
	def __init__(self, symtable, d_nodes, stack = []):
		self.symtable = symtable
		self.d_nodes = d_nodes
		self.stack = stack


	def simulate(self, d_nodes):
		for data in d_nodes:
			if data['instruction'] == 'push':
				if data['type'] == 'TK_IDENTIFIER':
					self.pushi(data['value'])
					#print "pushi " + str(data)
				else:
					#print "push " + str(data)
					#push value to stack
					self.push(data['value'])
					print self.stack

	def push(self, value):
		self.stack.insert(0,value)
		return

	def pushi(self, value):
		for v in self.symtable:
			if value == v['NAME']:
				self.stack.insert(0,v['VALUE'])
		return
	



if __name__ == '__main__':
	d_nodes = [{'ip': 0, 'instruction': 'push', 'type': 'TK_INTEGER', 'value': '100'}, {'ip': 1, 'instruction': 'pop', 'value': 'a'}, {'ip': 2, 'instruction': 'push', 'type': 'TK_IDENTIFIER', 'value': 'a'}, {'ip': 3, 'instruction': 'push', 'type': 'TK_INTEGER', 'value': '20'}, {'ip': 4, 'instruction': 'less', 'type': 'TK_LESS', 'value': 'less'}, {'ip': 5, 'instruction': 'jFalse', 'value': 11}, {'ip': 6, 'instruction': 'push', 'type': 'TK_STRING', 'value': "'hello'"}, {'ip': 7, 'instruction': 'writeln', 'type': 'TK_WRITELN', 'value': 'writeln'}, {'ip': 8, 'instruction': 'jmp', 'value': 11}, {'ip': 9, 'instruction': 'push', 'type': 'TK_IDENTIFIER', 'value': 'a'}, {'ip': 10, 'instruction': 'writeln', 'type': 'TK_WRITELN', 'value': 'writeln'}, {'ip': 11, 'instruction': 'ophalt', 'value': 'end.'}]
	symtable = [{'TYPE': 'integer', 'NAME': 'a', 'VALUE': 0, 'ADDRESS': 0}]
	s = Simulator(symtable, d_nodes)
	s.simulate(d_nodes)
