import sys
from trace_parcer import parse
from processor import processor

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

	# init all the processors with pids
	ps = {}
	ps[pid_0] = processor(pid_0)
	ps[pid_1] = processor(pid_1)
	ps[pid_2] = processor(pid_2)
	ps[pid_3] = processor(pid_3)

	# sort the traces by timestamps then by pid
	all_traces = p0_trace + p1_trace + p2_trace + p3_trace
	all_traces.sort(key = lambda t: (t[1], t[0]))

	# each cycle has the form (pid, timestamp, read/write(1/0), tag (int), index(int), offset(int))
	for cycle in all_traces:
		c_pid, _, io, c_tag, c_index, c_offset = cycle
		bus_action = ps[c_pid].execute(io, c_tag, c_index, c_offset)

if __name__ == '__main__':
	if len(sys.argv[1:]) < 4:
		print('Invalid input. Call to main.py should be of the form:')
		print('python3 main.py p0_trace p1_trace p2_trace p3_trace')
	main(sys.argv[1:])