files = ["../in1_attempt2.csv","../in2_attempt2.csv"]

for file in files[1:]:
	f = open(file)
	lines = f.readlines()
	f.close()
	lines = [i.strip().split(";") for i in lines]
	for line_index in xrange(len(lines)):
		temp = [i.strip() for i in lines[line_index][4].split("to")]
		lines[line_index] = lines[line_index][:4]+temp+lines[line_index][5:]
		# print line[4]
	# print lines[0]
	lines = [";".join(i) for i in lines]
	print lines
	f = open(file,"w")
	for line in lines:
		f.write(line+"\n")
	f.close()
