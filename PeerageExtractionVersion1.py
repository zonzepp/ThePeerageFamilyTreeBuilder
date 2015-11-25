#!/usr/bin/python
# Written by @simontuohy and @EamonnOToole Nov 2001

#Program to extract a family tree from www.thepeerage.com

import bs4
import requests 
import itertools
import time
import sys
class FamTreeNode(object):
	def __init__(self,value,url=None,peerageid=None,name = None,parents = [],gender=None,dob=None):
		self.parents = parents        	# Will the peerage ids of the parents
		self.gender = gender			# Will store M or F, male or female
		self.name = name				# Will store the persons name
		self.dob = dob					# Will store the persons DOB
		self.peerageid = peerageid      # Will store the i***** person id
		self.url = url  				# Will store the p****.htm
		self.value = value				# This is temporary, should allow a tree to be printed with the names
	def __repr__(self, level=0):
		ret = "\t"*level+repr(self.value)+"\n"
		for child in self.parents:
			ret += child.__repr__(level+1)
		return ret

def getPersonDetails(baseurl,thisNode):
	url = thisNode.url
	if pageDict.has_key(url):
		r = pageDict.get(url)
		soup = bs4.BeautifulSoup(r.text,"lxml")
		#print "Got from dict"
	else:
		r=requests.get(baseurl+url,headers={'User-Agent': 'Mozilla/5.0'})
		soup = bs4.BeautifulSoup(r.text,"lxml")
		pageDict[url] = r
		#print "Got from net"
	
		
	person = thisNode.peerageid
	
	try:
		subject = soup.find("div",{"id": person})
	except AttributeError: 
		print "no details"		
	try:
		details=subject.find("div",{"class": "narr"}) #get the person
 		links=details.find_all("a")
	except AttributeError:
		print "no Details"
	name = None
	try:
		name =subject.find("h2",{ "class":"sn sect-sn"})
		name= name.text #Must be better way of getting the name of the person
		name=name.split("1")
		subjectname=name[0]
	except AttributeError:
           print "no Details"
	myGender = None
	myDob = None
	try:
		headlineDetails = subject.find("div",{"class":"sinfo sect-ls"}) 	# get person gender, id and DOB hopefully
		splitDetails = headlineDetails.text.split(",")
		myGender = splitDetails[0]
		if(len(splitDetails) == 3):
			myDob = splitDetails[2]
	except AttributeError:
		print "Cannot get Gender and DOB"
	thisNode.name = subjectname
	thisNode.dob = myDob
	thisNode.gender = myGender
	thisNode.value = subjectname
	if myDob != None:
        	thisNode.value = thisNode.value + " " + myDob	
	lookFor = "daughter of"
	if myGender == "M":
		lookFor = "son of"
	
	parentsFound = False
	parseNext = False
	p = 0
	thisNode.parents = []
	while p < len(details.contents) and parentsFound == False:
		thisElement = details.contents[p]
		if lookFor in thisElement:
			parseNext = True
		elif parseNext:
			if type(thisElement) is bs4.element.NavigableString:
				if "." in thisElement:
					parentsFound = True
					parseNext = False
			else:
				fullLink=(thisElement.get('href'))
				personid=fullLink.split(u"\u0023")
				if len(personid[0]) > 0:
					parentNode = FamTreeNode(personid[1],personid[0],personid[1])
				else:
					parentNode = FamTreeNode(personid[1],thisNode.url,personid[1])
				familyDict[personid[1]] = parentNode
				thisNode.parents.append(parentNode)
				
		p = p + 1

pageDict = dict()
baseurl="http://www.thepeerage.com/"
familyDict = dict()

#~~~~~~~~~~~~~~~~~~~~Start of Program~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

input=sys.argv[1].split(u"\u0023") #take in system Arguements

rootPeer = input[1] 
root = FamTreeNode(input[1],input[0],input[1])


familyDict[rootPeer] = root

todo = []
todo.append(root)

i = 0;
while i < 100 and len(todo) > 0: #run for 100 generations
	time.sleep(1)
	for x in todo:
		
		getPersonDetails(baseurl,x)
	newToDo = []
	for x in todo:
		
		for y in x.parents:
			newToDo.append(y)
	todo = newToDo
	i = i + 1
	
print root #output the Family tree
