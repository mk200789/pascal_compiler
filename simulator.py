	#code for simulator will be placed here
import sys

class Simulator(object):
	def __init__(self, symtable, d_nodes, stack = [], ip=0):
		self.symtable = symtable
		self.d_nodes = d_nodes
		self.stack = stack
		self.ip = ip


	def simulate(self, d_nodes):
		while(1):
			if self.d_nodes[self.ip]['instruction'] == 'push':
				if self.d_nodes[self.ip]['type'] == 'TK_IDENTIFIER':
					self.pushi(self.d_nodes[self.ip]['value'])
				else:
					#push value to stack
					self.push(self.d_nodes[self.ip]['value'])
			elif self.d_nodes[self.ip]['instruction'] == 'pop':
				self.pop(self.d_nodes[self.ip]['value'])
			elif self.d_nodes[self.ip]['instruction'] == 'add':
				self.add()
			elif self.d_nodes[self.ip]['instruction'] == 'minus':
				self.minus()
			elif self.d_nodes[self.ip]['instruction'] == 'mult':
				self.mult()
			elif self.d_nodes[self.ip]['instruction'] == 'less':
				self.less()
			elif self.d_nodes[self.ip]['instruction'] == 'mod':
				self.mod()
			elif self.d_nodes[self.ip]['instruction'] == 'halt':
				self.halt()
			self.ip += 1
		print self.stack

	def push(self, value):
		#print "push"
		self.stack.insert(0,value)
		return

	def pushi(self, value):
		#print "pushi"
		for v in self.symtable:
			if value == v['NAME']:
				self.stack.insert(0,v['VALUE'])
		return

	def pop(self, value):
		#print "pop"
		#print "before pop"+str(self.stack)
		value1 = self.stack.pop()
		for v in self.symtable:
			if value == v['NAME']:
				v['VALUE'] = value1
				#print v
				#print "pop"+str(self.stack)
		return

	def add(self):
		#print "add"
		value1 = self.stack.pop()
		value2 = self.stack.pop()
		t = int(value1) + int(value2)
		self.push(t)
		return

	def minus(self):
		value1 = self.stack.pop()
		value2 = self.stack.pop()
		t = int(value1) - int(value2)
		self.push(t)
		return

	def mult(self):
		value1 = self.stack.pop()
		value2 = self.stack.pop()
		t = int(value1) * int(value2)
		self.push(t)
		return

	def mod(self):
		value1 = self.stack.pop()
		value2 = self.stack.pop()
		t = int(value1)%int(value2)
		self.push(t)
		return
	def less(self):
		value1 = self.stack.pop()
		value2 = self.stack.pop()
		t = int(value1) < int(value2)
		self.push(t)
		return

	def halt(self):
		print "END"
		sys.exit(0)
	#def writeln(self):
	#	value1 = self.stack.pop()


if __name__ == '__main__':
	#d_nodes = [{'ip': 0, 'instruction': 'push', 'type': 'TK_INTEGER', 'value': '100'}, {'ip': 1, 'instruction': 'pop', 'value': 'a'}, {'ip': 2, 'instruction': 'push', 'type': 'TK_IDENTIFIER', 'value': 'a'}, {'ip': 3, 'instruction': 'push', 'type': 'TK_INTEGER', 'value': '20'}, {'ip': 4, 'instruction': 'less', 'type': 'TK_LESS', 'value': 'less'}, {'ip': 5, 'instruction': 'jFalse', 'value': 11}, {'ip': 6, 'instruction': 'push', 'type': 'TK_STRING', 'value': "'hello'"}, {'ip': 7, 'instruction': 'writeln', 'type': 'TK_WRITELN', 'value': 'writeln'}, {'ip': 8, 'instruction': 'jmp', 'value': 11}, {'ip': 9, 'instruction': 'push', 'type': 'TK_IDENTIFIER', 'value': 'a'}, {'ip': 10, 'instruction': 'writeln', 'type': 'TK_WRITELN', 'value': 'writeln'}, {'ip': 11, 'instruction': 'ophalt', 'value': 'end.'}]
	#symtable = [{'TYPE': 'integer', 'NAME': 'a', 'VALUE': 0, 'ADDRESS': 0}]
	d_nodes = [{'ip': 0, 'instruction': 'push', 'type': 'TK_INTEGER', 'value': '2'}, {'ip': 1, 'instruction': 'pop', 'value': 'a'}, {'ip': 2, 'instruction': 'push', 'type': 'TK_INTEGER', 'value': '1'}, {'ip': 3, 'instruction': 'pop', 'value': 'b'}, {'ip': 4, 'instruction': 'push', 'type': 'TK_IDENTIFIER', 'value': 'a'}, {'ip': 5, 'instruction': 'push', 'type': 'TK_IDENTIFIER', 'value': 'b'}, {'ip': 6, 'instruction': 'add', 'type': 'TK_ADD', 'value': '+'}, {'ip': 7, 'instruction': 'pop', 'value': 'c'}, {'ip': 8, 'instruction': 'halt', 'value': 'end.'}]
	symtable = [{'TYPE': 'integer', 'NAME': 'a', 'VALUE': 0, 'ADDRESS': 0}, {'TYPE': 'integer', 'NAME': 'b', 'VALUE': 0, 'ADDRESS': 4}, {'TYPE': 'integer', 'NAME': 'c', 'VALUE': 0, 'ADDRESS': 8}]
	s = Simulator(symtable, d_nodes)
	s.simulate(d_nodes)
