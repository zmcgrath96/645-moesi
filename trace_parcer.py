import os

'''
Description:
	Given the trace file, read it in, make a tuple of
	(pid, timestamp, read/write(1/0), tag (int), index(int), offset(int))

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
			# split the binary number into tag, index, offset
			# 5 bit offset
			offset = int(b[27:], 2)
			# 9 bit index
			index = int(b[18:27], 2)
			# 18 bit tag
			tag = int(b[0:18], 2)
			t = (pid, int(line[0]), int(line[1]), tag, index, offset)
			trace.append(t)

	return trace