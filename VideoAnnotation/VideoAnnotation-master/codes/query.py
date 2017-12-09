import string

def convert_to_dig(x):
	all=string.maketrans('','')
	nodigs=all.translate(all, string.digits)
	x = x.translate(all, nodigs)
	return x

def answer_1(x4, x0, vectors):
	over_no = convert_to_dig(x4)
	innings_no = convert_to_dig(x0)
	vector = [innings_no, '', '','',over_no,'','?','','']
	result = [i for i in vectors if i[0]==innings_no and over_no == i[4].split(".")[0]]
	result = [i[6] for i in result]
	return list(set(result))

def answer_2(x6, vectors):
	result = [i for i in vectors if i[6]==x6 and "OUT" in i[7]]
	return result[0][4]

def answer_3(x6, vectors):
	result = [i for i in vectors if i[6]==x6 and "OUT" in i[7]]
	return result[0][5]

def answer_4(x4, x0,vectors):
	over_no = convert_to_dig(x4)
	innings_no = convert_to_dig(x0)

	result = [i for i in vectors if over_no == i[4].split(".")[0] and innings_no==i[0]]
	# for i in result:
	# 	print i
	result = [i[5] for i in result]
	return list(set(result))

def answer_5(x6, vectors):
	result = [i for i in vectors if x6==i[6]]
	# for i in result:
	# 	print print i[6]
	score = [int(i[2]) for i in result]
	score = score[-1]-score[0]+1
	return score
	# print score
def answer_6(x5, vectors):
	result = [i for i in vectors if x5==i[5] and "OUT" in i[7]]
	return len(result)

def answer_7(x4, x0, vectors):
	over_no = convert_to_dig(x4)
	innings_no = convert_to_dig(x0)
	result = [i for i in vectors if over_no==i[4] and innings_no == i[0] and "OUT" in i[7]]
	return len(result)
	# result = []

def answer_8(x6, vectors):
	result = [i[4] for i in vectors if x6==i[6] and "FOUR" in i[7]]
	return result

def answer_9(x6, vectors):
	result = [i[4] for i in vectors if x6==i[6] and "SIX" in i[7]]
	return result

# def answer_10()

def get_vectors(fname):
	f = open(fname)
	lines = f.readlines()
	f.close()
	lines = [i.strip().split(";") for i in lines]
	return lines

vectors = get_vectors("../combined.csv")
answer1 = answer_1("3rd", "1st", vectors)
answer2 = answer_2("Ganguly", vectors)
answer3 = answer_3("Ganguly",vectors)
answer4 = answer_4("10th","1st",vectors)
answer5 = answer_5("Ganguly", vectors)
answer6 = answer_6("Khan", vectors)
answer7 = answer_7("3rd", "1st", vectors)
answer8 = answer_8("Ganguly", vectors)
answer9 = answer_9("Ganguly", vectors)
answer10 = answer_10("Khan", vectors)
print answer8
# print answer4