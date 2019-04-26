import os

'''
Description:
	Given the trace file, read it in, make a tuple of
	(pid, timestamp, read/write(1/0), mem_address (converted to binary))

Parameters:
	filename: string
	pid: string

Returns:
	list of tuples
'''
def parse(filename, pid, bit_length=32):
	if not os.path.isfile(filename):
		raise FileExistsError
	
	trace  = []
	with open(filename, 'r') as f:
		for l in f:
			line = l.split(' ')
			b = bin(int(line[2], base=16))[2:].zfill(bit_length)
			t = (pid, int(line[0]), int(line[1]), b)
			trace.append(t)

	return trace