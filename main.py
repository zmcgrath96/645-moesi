import sys
from trace_parcer import parse

'''
Description:
	intro file into this project

Parameters:
	Takes in the 4 filenames for the processor traces
	ex: python3 main.py p0_trace p1_trace p2_trace p3_trace 

Returns:
	none
'''
def main(args):
	pid_0 = 'p0'
	pid_1 = 'p1'
	pid_2 = 'p2'
	pid_3 = 'p3'
	p0_trace  = parse(str(args[0]), pid_0)
	p1_trace  = parse(str(args[1]), pid_1)
	p2_trace  = parse(str(args[2]), pid_2)
	p3_trace  = parse(str(args[3]), pid_3)

	# sort the traces by timestamps then by pid
	all_traces = p0_trace + p1_trace + p2_trace + p3_trace
	all_traces.sort(key = lambda t: (t[1], t[0]))

	

if __name__ == '__main__':
	main(sys.argv[1:])