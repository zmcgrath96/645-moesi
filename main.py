import sys
from trace_parcer import parse
from processor import processor

INPUT_FOLDER = 'traces/'
QUICK_FILE_PARAMS = [INPUT_FOLDER + 'p0.tr', INPUT_FOLDER + 'p1.tr', INPUT_FOLDER + 'p2.tr', INPUT_FOLDER + 'p3.tr']
INTERACTIVE_PARAMS = ['-i'] + QUICK_FILE_PARAMS

bus_states = {
    'r': 'BusRd', 
    'rx': 'BusRdX',
    'u': 'BusUpgr'
}

p_state_enum = {
	'o': 1,
	'm': 2, 
	's': 3,
	'e': 4
}

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
	INTERACTIVE = False
	if '-i' in args[0]:
		args = args[1:]
		INTERACTIVE = True

	elif '-q' in args[0]:
		args = args[1:]

	# ============================================================================================
	#			 INIT STUFF
	# ============================================================================================
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
	# ============================================================================================
	#							BUS STUFF
	# ============================================================================================
	for cycle in all_traces:
		# for debugging
		if INTERACTIVE:
			input('Enter for next cycle')

		## STEP ONE: GET PROCESSOR STATES AND CHANGE EXEC PROCESSOR
		# make it easier to read
		c_pid, _, io, c_tag, c_index, c_offset = cycle
		# get the states of all the processors
		shared = False
		get_from_pid = None
		get_from_state = None
		states = get_states(ps, c_index, c_tag)
		for pid in states:
			state = states[pid]
			if state != 'i' and pid != c_pid:
				get_from_pid, get_from_state = high_priority(get_from_pid, get_from_state, pid, state)
				shared = True
		# have the processor say what action it needs done
		bus_action = ps[c_pid].execute(io, c_tag, c_index, c_offset)

		## STEP 2: if shared someone has the data and reading
		## always update our current state first
		ps[c_pid].change_state_rw(io, c_index, shared, c_tag)

		if bus_action is None:
			continue
		# busrd
		if  bus_action == bus_states['r']:
			if shared:
				ps[get_from_pid].change_state_bus(bus_action, c_index, c_tag)
		#busupgr
		elif bus_action == bus_states['u']:
			invalidate_all(ps, c_index, c_tag, c_pid)
			
		#busrdx
		else:
			for pid in ps:
				if pid != c_pid:
					ps[pid].change_state_bus(bus_action, c_index, c_tag)
					
	# ============================================================================================
	#							END BUS STUFF
	# ============================================================================================

	# PRINT STATS
	for pid in ps:
		states = ps[pid].count_states()
		print('{} \tm: {} \to: {} \te: {} \ts: {} \ti: {}'.format(pid, states[0], states[1], states[2], states[3], states[4]))
	# end main

# ============================================================================================
#							HELPER FUNCTIONS
# ============================================================================================
#return all the states of the processors in form {pid: state, ...}
def get_states(ps, index, tag):
	states = {}
	for p in ps:
		states[p] = ps[p].get_state(index, tag)
	return states

# a 'max' function for the highest priority processor to ask for on a BusRd
# Owner > Modified > Shared > Exclusive
def high_priority(last_pid, last_state, this_pid, this_state):	
	if last_pid is None or last_state is None:
		return this_pid, this_state	
	if p_state_enum[last_state] < p_state_enum[this_state]:
		return this_pid, this_state
	return last_pid, last_state

# Invalidate all other processors at that index and tag
# used by BusRdX and BusUpgr
def invalidate_all(ps, index, tag, exception_pid):
	for pid in ps:
		if pid != exception_pid:
			ps[pid].invalidate(index, tag)
# ============================================================================================
#							END HELPER FUNCTIONS
# ============================================================================================

# enter the file
if __name__ == '__main__':
	if len(sys.argv[1:]) < 4:
		if len(sys.argv) == 2:
			if '-q' in sys.argv[1]:
				INTERACTIVE_PARAMS[0] = '-q'
			main(INTERACTIVE_PARAMS)
		else:
			print('Invalid input. Call to main.py should be of the form:')
			print('python3 main.py p0_trace p1_trace p2_trace p3_trace')
