import sys
import json
from functools import reduce

#taking the name of a specific committer from the command line
first_arg = sys.argv[1]



def getCommitterSummary(fname):
	#extracting the json data from file data.json in a dictionary
	filename = 'data.json'
	with open('data.json') as d:
    		committers = json.load(d)


	#extracting data of the given committer
	committer = filter(lambda x: x['committer']==fname,committers["committers"])
        if(committer):        
        	#extracting the lines of code and dates committed in two separate list
        	loclist = map(lambda x: x['loc'],committer)
        	datelist = map(lambda x : x['date'],committer)
        	projects = map(lambda x: x['project'],committer)

        	#converting the project list to set to remove duplicates
        	projectset = set(projects)
        	#print(projectset)
        
       		#extracting the added loc and deleted loc in two separate list
        	addedlist = map(lambda x : x['added'],loclist)
        	deletedlist = map(lambda x : x['deleted'],loclist)

        	#adding the added  and deleted loc for each project given committer has worked on (it is a list)
        	totloclist = map(lambda x,y: x + y,addedlist,deletedlist)
        
        	#finding the max loc
        	max = reduce(lambda x,y: x if(x>y) else y,totloclist)
        	#preparing a bool array to find the date of max committed loc
        	boolismax = map(lambda x: 1 if(x==max) else 0,totloclist)
        	maxupddate = map(lambda x,y: y if(x==1) else 0,boolismax,datelist)

        	#extracting the date in a single variable
        	for x in maxupddate:
                	if(x!=0):
                  	 date = x

        	#print(date)


        	#finding the total of added and deleted loc for each project given committer has worked on
        	totadded = reduce(lambda x,y: x + y,addedlist,0)
        	totdeleted = reduce(lambda x,y: x + y,deletedlist)
        
        	#preparing the json data
        	result = "{committer:" + fname + ",projectsWorkedOn:["
        	length=len(projectset)
        	counter = 0 
        	for project in projectset:
           		if(counter==(length - 1)):
             			result = result + project
           		else:
             			result = result + project + ","
           		counter = counter + 1 
        	result = result +  "],locAdded:" + str(totadded) + ",locDeleted:" + str(totdeleted) + ",mostLinesModifiedOn:" + date + "}"
        	json_data = json.dumps(result)
        	print(json_data)
        else:
           print("the committer doesn't exist in the json database")
        

getCommitterSummary(first_arg)
