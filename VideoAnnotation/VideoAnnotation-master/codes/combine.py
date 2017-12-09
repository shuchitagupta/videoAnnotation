f1 = open("../in1_attempt2.csv")
f2 = open("../in2_attempt2.csv")

lines1 = f1.readlines()
lines2 = f2.readlines()

f1.close()
f2.close()

lines1 = ["1;"+i for i in lines1]
lines2 = ["2;"+i for i in lines2]

# print len(lines1)
# print len(lines2)

# print lines1[0]
# print lines2[0]

lines = lines1+lines2
res_f = open("../combines.csv","w")
for line in lines:
	res_f.write(line)
res_f.close()