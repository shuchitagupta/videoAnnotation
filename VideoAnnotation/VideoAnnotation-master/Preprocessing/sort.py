import csv
import sys
import numpy as np
import time
from collections import Counter
import os
import nltk
from math import log
import operator
import glob
import os.path, time
import csv
import numpy as np
import time
from collections import Counter
import glob
import os.path, time
import json
import re
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
from nltk.corpus import stopwords
from scipy import spatial
from math import *
import collections 


def writeFile(arr, file):
	with open(file, 'w') as csvfile:
		a = csv.writer(csvfile)
		for value in arr:
			a.writerow(value)


def readfile(file_path):
	f = open(file_path, 'r')
	freader = csv.reader(f, delimiter='\t')
	data = list(freader)
	np.set_printoptions(threshold=np.inf)
	arr = np.array(data)
	return arr

def readfilelines(file_path):
	with open(file_path) as f:
		content = f.readlines()
	return content

d = readfilelines('results3.txt')

fr = {}

for i in d:
	frame = i.split(',')[0].split('/')[2].split('.')[0]
	result = i.split(',')[1].strip('\n')
	fr[int(frame)] = result

d = readfilelines('results4.txt')

for i in d:
	frame = i.split(',')[0].split('/')[2].split('.')[0]
	result = i.split(',')[1].strip('\n')
	fr[int(frame)] = result


res = collections.OrderedDict(sorted(fr.items()))

f = open('final_results3.csv', 'w')
for k, v in res.iteritems(): 
	print k, v
	f.write(str(k) +"," + str(v) + '\n')
f.close()

# for i in new_score:
# 	print i
# new_score = np.array(new_score)
# with open('in2_score.csv', 'w') as fp:
# 		a = csv.writer(fp,delimiter=',')
# 		for row in new_score:
# 			a.writerow(row)
# print new_score
# print len(new_score)