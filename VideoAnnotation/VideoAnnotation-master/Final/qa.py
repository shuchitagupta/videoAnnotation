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
from nltk.tag import StanfordNERTagger
from math import *

st = StanfordNERTagger('./stanford-ner-2016-10-31/classifiers/english.all.3class.distsim.crf.ser.gz', './stanford-ner-2016-10-31/stanford-ner.jar')


stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')

def readfile(file_path):
	f = open(file_path, 'rU')
	freader = csv.reader(f, delimiter='\t')
	data = list(freader)
	np.set_printoptions(threshold=np.inf)
	arr = np.array(data)
	return arr

def readfilelines(file_path):
	with open(file_path) as f:
		content = f.readlines()
	return content

def createInvertedIndex(answers):
	global invertedIndex
	index = 0
	for sentence in answers:
		document = []
		tokens = tokenizer.tokenize(sentence)
		#	print tokens
		#tokens = [i.encode('utf-8') for i in tokens]
		try:
			stem_token = [stemmer.stem(word) for word in tokens if word not in stopwords.words('english')]
		except Exception, e:
			print e
			stem_token = [word for word in tokens if word not in stopwords.words('english')]
		document.extend(stem_token)
		document.extend(arr[index,0].lower().split('_'))
		print document
		#print index, stem_token
		for token in document:
			if token not in invertedIndex:
				freq = document.count(token)
				invertedIndex[token]=[[index, freq]]
			elif token in invertedIndex:
				l = [i[0] for i in invertedIndex[token]]
				if(index not in l):
					freq = document.count(token)
					invertedIndex[token].append([index,freq])
		index = index +1

def takeQueries():
	print "Enter your question >"
	while(1):
		query = raw_input().lower()
		if(query == 'exit()'):
			break
		else:
			tokens_t = tokenizer.tokenize(query)
			tokens = [stemmer.stem(word) for word in tokens_t if word not in stopwords.words('english')]
			print tokens
			if(len(tokens) ==1):
				scores = findTfIdf(tokens[0])
				if('-1' in scores):
					print "Didn't match anything"
				else:
					sorted_x = sorted(scores.items(), key=operator.itemgetter(1),reverse=True)
					result = []
					for i in sorted_x:
						result.append([i[0],answers[i[0]], i[1]])
					print result
			elif(len(tokens) > 1):
				scores = {}
				for token in tokens:
					score = findTfIdf(token)
					print score
					if('-1' not in score):
						for doc in score:
							if doc not in scores:
								scores[doc] = score[doc]
							else:
								scores[doc] = scores[doc] + score[doc]
				sorted_scores = sorted(scores.items(), key=operator.itemgetter(1),reverse=True)
				result = []
				for i in sorted_scores:
					result.append([i[0],answers[i[0]], i[1]])
				print result
				print "----------"


def takeQueriesCosine():
	while(1):
		print "Enter your question >"
		query = raw_input().lower()
		if(query == 'exit()'):
			break
		else:
			print answerQuery(query)
			print "---------------s"

def findTfIdf(word):
	global invertedIndex
	if word in invertedIndex:
		l = invertedIndex[word]
		docs = [i[0] for i in l]
		freq = [i[1] for i in l]
		tfidf = {}
		for i in l:
			tf = 1 + log(i[1])
			idf = log(N/len(docs))
			tfidf[i[0]] = tf * idf
		return tfidf

	else:
		return {'-1':0}

def giveTfIdf(word, doc):
	global invertedIndex, docMap, N
	if word in invertedIndex:
		l = invertedIndex[word]
		docs = [i[0] for i in l]
		for i in l:
			if(i[0]==doc):
				return (1 + log(i[1]) * log(N/len(docs)))
		return 0
	return 0



typeIndex = {}

def createTypeIndex(answers):
	global typeIndex
	index = 0
	for sentence in answers:
		document = []
		tag = st.tag(sentence.split())
		print tag
		for i in tag:
			if(i[0] not in stopwords.words('english')):
				if(i[1] == 'LOCATION'):
					typeIndex[stemmer.stem(i[0])] = 'L'
				elif(i[1] == 'PERSON'):
					typeIndex[stemmer.stem(i[0])] = 'P'
				elif(i[1] == 'ORGANIZATION'):
					typeIndex[stemmer.stem(i[0])] = 'O'
				else:
					pass

def giveTfIdf(word, doc):
	global invertedIndex
	if word in invertedIndex:
		l = invertedIndex[word]
		docs = [i[0] for i in l]
		for i in l:
			if(i[0]==doc):
				return (1 + log(i[1]) * log(N/len(docs)))
		return 0
	return 0


def createWordMatrix(answers):
	global invertedIndex, words, WordMatrix
	words = invertedIndex.keys()
	for word in words:
		a = []
		for i in range(0,len(answers)):
			a.append(giveTfIdf(word,i))
		WordMatrix.append(a)
	WordMatrix = np.array(WordMatrix)


def square_rooted(x):
	return round(sqrt(sum([a*a for a in x])),3)
 
def cosine_similarity(x,y):
	numerator = sum(a*b for a,b in zip(x,y))
	denominator = square_rooted(x)*square_rooted(y)
	return round(numerator/float(denominator),3)

def answerQuery(query):
	tokens_t = tokenizer.tokenize(query.lower())
	tokens = [stemmer.stem(word) for word in tokens_t if word not in stopwords.words('english')]
	print tokens
	th = 0.3

	qvec=[]
	for word in words:
		if word in tokens:
			qvec.append(tokens.count(word))
		else:
			qvec.append(0)
	scores = {}
	for doc in range(0,WordMatrix.shape[1]):
		dist = cosine_similarity(list(qvec), list(WordMatrix[:,doc]))
		#print dist, th*square_rooted(qvec)*square_rooted(list(WordMatrix[:,doc]))
		#if(dist >= th*square_rooted(qvec)*square_rooted(list(WordMatrix[:,doc]))):
		if dist >0.0 and dist >0.3:
			scores[doc] =  dist 
			#print [dist,square_rooted(qvec)*square_rooted(list(WordMatrix[:,doc])), dist/square_rooted(qvec)*square_rooted(list(WordMatrix[:,doc]))]
	sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
	result = []
	for i in sorted_scores:
		if(i[1] >= th*sorted_scores[0][1]):
			result.append([i[0],questions[i[0]],answers[i[0]], i[1]])
	return result[0:3]

def testEngine(arr):

	global questions
	correct, incorrect = 0,0
	precision = [] 
	recall = []
	for i in range(1,arr.shape[0]):
		print "----------", i
		query = arr[i,1]
		result = answerQuery(query)
		rel = set([i for i, x in enumerate(questions) if x == query])
		print result, query
		try:
			qa.append([query,result[0][2]])
			actual_result = query
			retrev = set([a[0] for a in result])
			print rel, retrev
			p = float(len(rel & retrev))/float(len(retrev))
			precision.append(p)
			r = float(len(rel & retrev))/float(len(rel))
			recall.append(r)
			if(result[0][1] == query):
				correct = correct +1
			else:
				incorrect = incorrect + 1
		except Exception, e:
			print e
	print correct
	print incorrect
	print float(correct)/float(correct+incorrect)
	print precision
	print recall
	print np.mean(precision)
	print np.mean(recall)

arr = readfile('600_qa_pair.csv')
answers = list(arr[1:,2])
questions = arr[1:,1]

# createTypeIndex(answers)

# f=open('typeIndex.csv', 'w')
# for i in typeIndex:
# 	f.write(i + "," + typeIndex[i] + "\n")
# f.close()

qa=[]

invertedIndex={}
createInvertedIndex(answers)
N = len(invertedIndex.keys())

words = []
WordMatrix = []
createWordMatrix(answers)
print WordMatrix.shape

takeQueriesCosine()
#testEngine(arr)

# qa = np.array(qa)
# with open('part1_results.csv', 'w') as fp:
# 		a = csv.writer(fp,delimiter='\t')
# 		#a.writerow(["ArticleTitle","Question","Answer","DifficultyFromQuestioner","DifficultyFromAnswerer","ArticleFile","ArticlePath"])
# 		for row in qa:
# 			a.writerow(row)




