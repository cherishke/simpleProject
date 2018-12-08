import re

import frontStart
import rdfDB.freebaseAPI as findFbname

def getAnswerTriple(entitymid,answer_mid_list,type_pattern):

	#找ans mid对应的string
	ansnameList,idlist=findFbname.googleFindname(answer_mid_list)
	print('~~~~~~~')
	print(ansnameList)
	# for amid in answer_mid_list:
	#     midname=frontStart.midtable.find_one({'mid': amid})
	#     if midname is not None:
	#     	# print(midname['name'])
	#     	answername.append(midname['name'])
	#     else:
	#     	print(amid)
	
	#找entity mid对应的string
	entityname=frontStart.midtable.find_one({'mid': entitymid})['name']
	
	#找sparql中的parse
	parse=re.split(r"<e>|\?",type_pattern)[2]
	parse=parse.strip()

	#得到ans triple
	answerTriple=[]
	for ans in ansnameList:
		temptriple=[]
		temptriple.append(entityname)
		temptriple.append(parse)
		temptriple.append(ans)
		# answerTriple.append(entityname+','+parse+','+ans)
		answerTriple.append(temptriple)

	return answerTriple,parse,entityname

def getOtherTriple(entityname,entitymid,parse,triplelen):
	parselist=parse.split('.')

	firstparse=parselist[0]
	secondparse=parselist[1]+'.'+parselist[2]
	firstother=frontStart.showtable.find({'e1':entitymid, 'parse':{'$regex': firstparse+'.(?!'+secondparse+'$)'}}).limit(15-triplelen)
	
	temptriple=[]
	thirdmidlist=[]
	for i in firstother:
		thirdmid=i['e2']
		print(thirdmid)
		tempparse=i['parse']
		thirdmidlist.append(thirdmid)
		temptriple.append([tempparse,thirdmid])

	print(thirdmidlist)

	finalotherTriple=[]
	thirdnamelist,thirdidlist=findFbname.googleFindname(thirdmidlist)
	print(thirdnamelist)
	
	for triple in temptriple:
		thirdmid=triple[1]
		if thirdmid in thirdidlist:
			id_index=thirdidlist.index(thirdmid)
			othertriple=[]
			othertriple.append(entityname)
			othertriple.append(triple[0])
			othertriple.append(thirdnamelist[id_index])
			finalotherTriple.append(othertriple)
		# finalotherTriple.append(entityname+','+triple[0]+','+thirdnamelist[num])

	return finalotherTriple

def getTypeTriple(entityname,entitymid,triplelen):

	typeother=frontStart.showtable.find({'e1':entitymid, 'parse':{'$regex': 'type.'}}).limit(15-triplelen)

	finaltypeTriple=[]
	for i in typeother:
		temptriple=[]
		thirdmid=i['e2']
		thirdname=frontStart.midtable.find_one({'mid':thirdmid})

		if thirdname is None:
			thirdname=thirdmid
		else:
			thirdname=thirdname['name']
			
		tempparse=i['parse']
		temptriple.append(entityname)
		temptriple.append(tempparse)
		temptriple.append(thirdmid)

		finaltypeTriple.append(temptriple)

	return finaltypeTriple





