from scanner import Scanner
from parser import Parser
from simulator import Simulator
import sys

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "invalid argument"
		print "python /compiler/run.py examples/test code"
		sys.exit(0)

	filename = sys.argv[1]

	#set up scanner
	scanner = Scanner(1,1,False,'', False, False,[],'',[], False)
	tokens = scanner.scan(filename)
	
	#set parser
	parser = Parser(tokens, 0)
	e = parser.parse()

	#set simulator
	simulator = Simulator(e['symtable'], e['d_nodes'])
	simulate = simulator.simulate()
