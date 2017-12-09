from wit import Wit
import json
import string
import webbrowser

def send(request, response):
    print('Sending to user...', response['text'])
def my_action(request):
    print('Received from user...', request['text'])

actions = {
    'send': send,
    'my_action': my_action,
}

client = Wit(access_token="BIFWIAYPQWZ6STKYSGTE3ESU7YIKAD6C", actions=actions)
question = raw_input()
resp = client.message(question)

# print('Yay, got Wit.ai response: ' + str(resp))

col_mp = {}
col_mp['bowler'] = 5
col_mp['six'] = 7
col_mp['four'] = 7
col_mp['fours'] = 7
col_mp['out'] = 7
col_mp['over'] = 4
col_mp['wickets'] = 3
col_mp['innings'] = 0
col_mp['runs'] = 2
col_mp['batsman'] = 6
col_mp['runs'] = 2
col_mp['wickets'] = 3
col_mp['bowler'] = 5
col_mp['time'] = 1

def convert_to_dig(x):
	all=string.maketrans('','')
	nodigs=all.translate(all, string.digits)
	x = x.translate(all, nodigs)
	return x

def openBrowser(timestamp):
	t = int(timestamp)
	m, s = divmod(t, 60)
	h, m = divmod(m, 60)
	print "%d:%02d:%02d" % (h, m, s)
	url = "https://youtu.be/Vn-nEEvYa_k?t=" +str(h)+"h" +str(m) +"m" + str(s) +"s" 
	webbrowser.open_new_tab(url)


# print ""
# print resp['entities'].keys()
intent = resp['entities']['intent'][0]['value']
# print intent

query = [""]*9
# print query
#innings
# print question
# print question.split().find("innings")
# print "2342342342343"
# print "cric_object" in resp['entities'].keys()
# print "innings" in resp['entities']["cric_object"]
if "intent" in resp['entities'].keys() and "intent" in resp['entities']["intent"]:
	query[0] = "?"
elif "cric_object" in resp['entities'].keys():
	for obj in resp['entities']["cric_object"]:
		if obj['value']=="innings":
	# print "!!!!!!"
			try:
				query_index = question.split().index("innings")
			except:
				query_index = question.split().index("inning")
			query_index-=1
			overs = convert_to_dig(question.split()[query_index])
			# print "overs",overs
			query[0] = overs

#time
if intent=="time":
	query[1]="?"

#runs
if intent=="runs":
	query[2]="?"

#wickets
if intent=="wickets":
	query[3]="?"
	query[7]="OUT"
elif "cric_object" in resp['entities'].keys() and "wickets" in resp['entities']["cric_object"]:
	for obj in resp['entities']["cric_object"]:
		if obj['value']=="wickets":
	# print "!!!!!!"
			try:
				query_index = question.split().index("wickets")
			except:
				query_index = question.split().index("wicket")
			query_index-=1
			overs = convert_to_dig(question.split()[query_index])
			# print "overs",overs
			query[3] = overs

#over
# print "@@@@"
# print resp['entities'].keys()
# print resp['entities']["cric_object"]
if intent=="overs":
	# print "!!!!!!"
	query[4]="?"
elif "cric_object" in resp['entities'].keys():
	for obj in resp['entities']["cric_object"]:
		if obj['value']=="over":
	# print "!!!!!!"
			try:
				query_index = question.split().index("overs")
			except:
				query_index = question.split().index("over")
			query_index-=1
			overs = convert_to_dig(question.split()[query_index])
			# print "overs",overs
			query[4] = overs

#bowler
if intent=="bowler":
	query[5]="?"
elif "action_bowl" in resp["entities"] and "contact" in resp["entities"]:
	query[5] = resp["entities"]["contact"][0]["value"]
#batsman
if intent=="batsman":
	query[6]="?"
elif "action_bat" in resp["entities"] and "contact" in resp["entities"]:
	query[6] = resp["entities"]["contact"][0]["value"]

if intent=="bowler" and "contact" in resp["entities"] and "action_bat" not in resp["entities"]:
	query[6] = resp["entities"]["contact"][0]["value"]

if "action_bat" not in resp["entities"] and "action_bowl" not in resp["entities"] and "contact" in resp["entities"]:
	query[6] = resp["entities"]["contact"][0]["value"]
# elif "action_bowl" in resp["entities"] and "contact" in resp["entities"]:
# 	query[6] = resp["entities"]["contact"][0]["value"]
#event
if "cric_event" in resp["entities"]:
	for event in resp["entities"]["cric_event"]:
		val = event["value"]
		# print "valllll",val
		if val=="six":
			# print "its a six"
			query[7]="SIX"
		elif val=="fours":
			query[7]="FOUR"
		elif val=="out":
			query[7]="OUT"	

# if query[6]=="" and "contact" in resp["entities"]:
# 	query[6]

# print query

def get_vectors(fname):
	f = open(fname)
	lines = f.readlines()
	f.close()
	lines = [i.strip().split(";") for i in lines]
	return lines

vectors = get_vectors("../combined.csv")

# print len(vectors)
result=[]
if query[0]!="" and query[0]!="?":
	result = [i for i in vectors if i[0]==query[0]]
	# print "0",len(result)
if query[1]!="" and query[1]!="?":
	if result!=[]:
		result = [i for i in result if i[1]==query[1]]
	else:
		result = [i for i in vectors if i[1]==query[1]]		
	# print "1",len(result)
if query[2]!="" and query[2]!="?":
	if result!=[]:
		result = [i for i in result if i[2]==query[2]]
	else:
		result = [i for i in vectors if i[2]==query[2]]		
	# print "2",len(result)
if query[3]!="" and query[3]!="?":
	if result!=[]:
		result = [i for i in result if i[3]==query[3]]
	else:
		result = [i for i in vectors if i[3]==query[3]]		
	# print "3",len(result)
if query[4]!="" and query[4]!="?":
	# print "!!!!",len(result)
	# for i in result:
		# print i[4]
	if result!=[]:
		result = [i for i in result if i[4].split(".")[0]==query[4]]
	else:
		result = [i for i in vectors if i[4].split(".")[0]==query[4]]		
	# print "4",len(result)
if query[5]!="" and query[5]!="?":
	if result!=[]:
		result = [i for i in result if i[5]==query[5]]
	else:
		result = [i for i in vectors if i[5]==query[5]]		
	# print "5",len(result)
if query[6]!="" and query[6]!="?":
	if result!=[]:
		result = [i for i in result if i[6]==query[6]]
	else:
		result = [i for i in vectors if i[6]==query[6]]		
	# print "6",len(result)
if query[7]!="" and query[7]!="?":
	if result!=[]:
		result = [i for i in result if query[7] in i[7]]
	else:
		result = [i for i in vectors if query[7] in i[7]]		
	# print "7",len(result)
if query[8]!="" and query[8]!="?":
	if result!=[]:
		result = [i for i in result if i[8]==query[8]]
	else:
		result = [i for i in vectors if i[8]==query[8]]		
	# print "8",len(result)

# print len(result)
# print result

search_index = query.index("?")
if "How many runs" in question:
	res = [i[search_index] for i in result]
	res = int(res[-1])-int(res[0])+1
elif "How many" in question:
	res = len([i[search_index] for i in result])

else:
	res = list(set([i[search_index] for i in result]))
	if "When" in question:
		for val in res:
			openBrowser(int(val)-10)
			raw_input()
print "RES",res




