f = open("../t20/resi1.csv")
lines = f.readlines()
f.close()
lines = [i.strip() for i in lines]
total_runs = 0
res_f = open("../t20/final_resi1.csv","w")
for line in lines:
	over = line.split(";")[0]
	who = line.split(";")[1].split(",")[0]
	event = line.split(";")[1].split(",")[1].strip()
	comment = ",".join(line.split(";")[1].split(",")[2:])
	if "1" in event:# or event=="1 wide" or event=="1 bye" or event=="1 leg bye":
		total_runs+=1
	elif "2" in event: #event=="2 runs" or event=="2 byes":
		total_runs+=2
	elif "3" in event: #event=="3 runs" or event=="3 byes":
		total_runs+=3
	elif "FOUR" in event or "4" in event:
		total_runs+=4
	elif "SIX" in event or "6" in event:
		total_runs+=6
	res_f.write(over+";"+who+";"+event+";"+str(total_runs)+";"+comment+"\n")
res_f.close()