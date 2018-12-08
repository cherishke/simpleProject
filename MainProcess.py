#coding=utf-8
import frontStart
import simpleEntityModel.evaluate as evaluate
import simpleGetMid.turnTomid as tomid
import simpleGetMid.getMid as getmid
import simpleGetMid.getType as gettype
import simpleSPARQLmodel.LoadModel as simpleload
import simpleSPARQLmodel.getFinalSPARQL as fSparql
import ShowAnswer.getTriple as getAnsTriple

import re
import json
import requests
import os

inputquestion="what position does carlos gomez play"
# inputquestion="what film did vidhu vinod chopra produce"
#entity model
ftype_q=open("type_q.txt",'w',encoding='utf-8')
simple_model_dir='bestSPARQLmodel'

simple_entitymodel,SSmodel, SShooks=frontStart.frontstart()
#命名实体识别部分
#启动模型

IOBlist = evaluate.interactive_shell(simple_entitymodel, inputquestion)  # 将inputquestion放进model中  ==>  IOB list
print(IOBlist)
entity = tomid.findEntityname(inputquestion, IOBlist)  # 得到entitylist
midlist = getmid.FindMid(entity)  # 得到midlist
q_entity=midlist[0]
if len(midlist)>1:
	candidate_e=midlist[1:-1]
print(midlist)

# 将问句转换为type_pattern
midtype = gettype.getType(q_entity, inputquestion)  # 得到type
print('midtype-->', midtype)

# 转换typepattern
typepattern = ""
typepattern = inputquestion.replace(entity, '<' + midtype + '>')
print('typepattern:',typepattern)
ftype_q.write(typepattern)
ftype_q.close()

#getSPARQL
sess = None
flags_input_pipeline = "class: ParallelTextInputPipeline\nparams:\n  source_files:\n  - type_q.txt"

type_pattern, sess = simpleload.everySenPre(flags_input_pipeline, SSmodel, SShooks, simple_model_dir, sess)
print(type_pattern)

#addMid->FinalSparql
finalSPARQL=fSparql.getSimpleSPARQL(type_pattern,midlist)
print(finalSPARQL)

#查库
queryS='PREFIX ns:<http://rdf.freebase.com/ns/> '+finalSPARQL

header = {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate'
}
payload = {
    'sparql': queryS
}
print(payload)
res = requests.post('http://0.0.0.0:5003/simplefreebase', data=json.dumps(payload), headers=header)
# print(res.json())


#得到答案，处理答案，提出mid
answer_mid_list=[]
# rdf="[['http://rdf.freebase.com/ns/m.0gsl7g'], ['http://rdf.freebase.com/ns/m.02pkn5g'], ['http://rdf.freebase.com/ns/m.047q2k1'], ['http://rdf.freebase.com/ns/m.02pm1dz'], ['http://rdf.freebase.com/ns/m.0gqfsr'], ['http://rdf.freebase.com/ns/m.05stpm'], ['http://rdf.freebase.com/ns/m.0278nyf'], ['http://rdf.freebase.com/ns/m.07ccp2'], ['http://rdf.freebase.com/ns/m.0ch40r3'], ['http://rdf.freebase.com/ns/m.03ndy9'], ['http://rdf.freebase.com/ns/m.08lrs1'], ['http://rdf.freebase.com/ns/m.0f2jhv'], ['http://rdf.freebase.com/ns/m.02pp_6v'], ['http://rdf.freebase.com/ns/m.0bwj0j9']]"
rdf=str(res.json())
# if 'Literal' in rdf:
#     rdflist = rdf.split("\'")
#     answer_mid_list.append(rdflist[1])
# else:
rdflist = re.split("ns/|\'", rdf)
# print(rdflist)
namelen = len(rdflist)
i = 2
while i < namelen:
    answer_mid_list.append(rdflist[i])
    i += 3
print(answer_mid_list)

#ans triple
ansTriple,parse,entityname=getAnsTriple.getAnswerTriple(q_entity,answer_mid_list,type_pattern)
print('-------------------')
print(ansTriple)

#most 15
triplelen=len(ansTriple)
othertriple=[]
if triplelen<15:
	# parselist=parse.split('.')
	# temp_parse=parselist[0]+'.'+parselist[1]
	# othertriple=os.system('grep -r '+midlist[0]+'.*type.'+' /Users/jipeng/htdocs/lkdocs/freebase/showTriple.txt')
	# print(othertriple)
	othertriple=getAnsTriple.getOtherTriple(entityname,q_entity,parse,triplelen)
	print(othertriple)

ansTriple=ansTriple+othertriple
triplelen=len(ansTriple)
print(triplelen)

typetriple=[]
if triplelen<15:
	typetriple=getAnsTriple.getTypeTriple(entityname,q_entity,triplelen)
	print(typetriple)

ansTriple=ansTriple+typetriple





