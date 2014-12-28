	#code for simulator will be placed here
import sys

class Simulator(object):
	def __init__(self, symtable, d_nodes, stack = [], ip=0):
		self.symtable = symtable
		self.d_nodes = d_nodes
		self.stack = stack
		self.ip = ip


	def simulate(self):
		while(1):
			print str(self.ip) + ":  [" + str(self.d_nodes[self.ip]['instruction']) + " : " +str(self.d_nodes[self.ip]['value']) + "]"
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
			elif self.d_nodes[self.ip]['instruction'] == 'div':
				self.div()
			elif self.d_nodes[self.ip]['instruction'] == 'less':
				self.less()
			elif self.d_nodes[self.ip]['instruction'] == 'greater':
				self.greater()
			elif self.d_nodes[self.ip]['instruction'] == 'equals':
				self.equals()
			elif self.d_nodes[self.ip]['instruction'] == 'mod':
				self.mod()
			elif self.d_nodes[self.ip]['instruction'] == 'halt':
				self.halt()
			elif self.d_nodes[self.ip]['instruction'] == 'jmp':
				self.jmp(self.d_nodes[self.ip]['value'])
			elif self.d_nodes[self.ip]['instruction'] == 'jFalse':
				self.jFalse(self.d_nodes[self.ip]['value'])
			elif self.d_nodes[self.ip]['instruction'] == 'jTrue':
				self.jTrue(self.d_nodes[self.ip]['value'])
			elif self.d_nodes[self.ip]['instruction'] == 'writeln':
				print self.d_nodes[self.ip+1]
				self.writeln()
			self.ip += 1
			print "stack: "+str(self.stack)
		print self.stack


	def jmp(self, value):
		self.ip = value - 1
		return

	def jFalse(self, value):
		value1 = self.stack.pop()
		if value1 == False:
			self.ip = value - 1
		return

	def jTrue(self, value):
		value1 = self.stack.pop()
		if value1 == True:
			self.ip = value -1
		return

	def push(self, value):
		self.stack.insert(0,value)
		return

	def pushi(self, value):
		for v in self.symtable:
			if value == v['NAME']:
				self.stack.insert(0,v['VALUE'])
		return

	def pop(self, value):
		#print "pop"
		value1 = self.stack.pop()
		for v in self.symtable:
			if value == v['NAME']:
				v['VALUE'] = value1
		print self.symtable
		return

	def add(self):
		#print "add"
		value1 = self.stack.pop()
		value2 = self.stack.pop()
		#if (type(value1) == type(value2)):
		#	print str(self.symtable) + "  HELOWORLD" 
		#	for v in self.symtable:
		#		if v['NAME'] == self.d_nodes[self.ip+1]['value']:
		#			tempTotal = v['TYPE']
		#		if v['VALUE'] == value1:
		#			tempValue1 = v['TYPE']
		#	if tempValue1 == tempTotal:
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

	def div(self):
		value1 = self.stack.pop()
		value2 = self.stack.pop()
		t = int(value1)/int(value2)
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

	def greater(self):
		value1 = self.stack.pop()
		value2 = self.stack.pop()
		t = int(value1) > int(value2)
		self.push(t)
		return		

	def equals(self):
		value1 = self.stack.pop()
		value2 = self.stack.pop()
		print type(value1)
		if type(value1) is int:
			t = (int(value1) == int(value2))
		if type(value1) is str:
			t = value1 == value2
		self.push(t)
		return

	def halt(self):
		print "END"
		self.printer()
		sys.exit(0)

	def printer(self):
		print "-------------------------------------------"
		print "%0s %8s %8s %10s %10s %0s" %('|','TOKEN|', 'VALUE|', 'TYPE|', 'ADDRESS', '|')
		print "-------------------------------------------"
		for n in self.symtable:
			print "%0s %8s %8s %10s %10s %0s" %('|', str(n['NAME'])+"|", str(n['VALUE'])+"|", str(n['TYPE'])+"|", n['ADDRESS'], '|')
		print "-------------------------------------------"
		return
	
	def writeln(self):
		value1 = self.stack.pop()
		return
