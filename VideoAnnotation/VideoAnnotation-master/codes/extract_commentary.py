f = open("../t20/commentaryi2.html")
lines = f.readlines()
f.close()
lines = [i.strip() for i in lines]
html = " ".join(lines)
# print html
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
# html = #the HTML code you've written above
parsed_html = BeautifulSoup(html)
# print parsed_html
all_overs = parsed_html.body.findAll('div', attrs={'class':'commentary-event'})
res_f = open("../t20/resi2.csv","w")
for i in all_overs:
	# print i.text
	print i.text.split(" ")
	text = i.text.split(" ")[1:]
	over = text[0]
	if over=="":
		continue
	comment = " ".join(text[2:])
	res_f.write(over+";"+comment.encode("utf-8")+"\n")
res_f.close()
