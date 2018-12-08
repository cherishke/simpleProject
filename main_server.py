#coding=utf-8
import frontStart
import simpleEntityModel.evaluate as evaluate
import simpleGetMid.turnTomid as tomid
import simpleGetMid.getMid as getmid
import simpleGetMid.getType as gettype
import simpleSPARQLmodel.LoadModel as simpleload
import simpleSPARQLmodel.getFinalSPARQL as fSparql
import ShowAnswer.getTriple as getAnsTriple
import rdfDB.freebaseAPI as fbapi

import re
import json
import requests
import os
from ast import literal_eval


from flask import Flask
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource, request

app = Flask(__name__)
CORS(app, supports_credentials=True);
api = Api(app)

inputquestion="which equestrian was born in dublin"
# inputquestion="what film did vidhu vinod chopra produce"
#entity model
ftype_q=open("type_q.txt",'w',encoding='utf-8')
simple_model_dir='bestSPARQLmodel'

simple_entitymodel,SSmodel, SShooks=frontStart.frontstart()
#命名实体识别部分
#启动模型
#entitymodel=frontStart.frontstart()
#entitymodel=evaluate.evalmain()

class EntityRecognization(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('inputquestion', type=str, location='json')
        self.reqparse.add_argument('IOBlist', type=str, location='json')
        self.reqparse.add_argument('bestentity', type=str, default="", location='json')
        self.reqparse.add_argument('midlist', type=str, default="", location='json')
        self.reqparse.add_argument('entityName', type=str, default="", location='json')
        super(EntityRecognization, self).__init__()

    def put(self):
        
        args = self.reqparse.parse_args()
        inputq = args['inputquestion'] or ''
        print('--->', inputq)
        IOBlist = evaluate.interactive_shell(simple_entitymodel, inputq)  # 将inputquestion放进model中  ==>  IOB list
        print(IOBlist)
        entity = tomid.findEntityname(inputq, IOBlist)  # 得到entitylist
        midlist,midnamelist = getmid.FindMid(entity)  # 得到midlist
        print(midlist)
        print(midnamelist)
        if len(midlist)<2:
            try:
                raise MyException("can't find entity ")
            except MyException as e:
                # print()
                return e.message, 400

        q_entity=midlist[0]
        q_entity_name=midnamelist[0]
        # if len(q_entity)<2:
        #     try:
        #         raise MyException("can't find entity ")
        #     except MyException as e:
        #         # print()
        #         return e.message, 400

        res = {
            'inputquestion': inputq,
            'bestentity': q_entity,
            'bestentity_name':q_entity_name,
            'midlist': midlist[1:-1],
            'midlist_name':midnamelist[1:],
            'entityName': entity,
        }
        return res, 200

    def post(self):
        args = self.reqparse.parse_args()
        q_entity = args['bestentity'] 
        inputquestion = args['inputquestion']
        q_entity_name=args['entityName']
        # 将问句转换为type_pattern
        midtype = gettype.getType(q_entity, inputquestion)  # 得到type
        print('midtype-->', midtype)

        # 转换typepattern
        typepattern = ""
        typepattern = inputquestion.replace(q_entity_name, '<' + midtype + '>')
        print(typepattern)
        ftype_q.write(typepattern)
        ftype_q.close()

        # 初始化simpleqa sparql model
        sess = None
        flags_input_pipeline = "class: ParallelTextInputPipeline\nparams:\n  source_files:\n  - type_q.txt"
        type_pattern, sess = simpleload.everySenPre(flags_input_pipeline, SSmodel, SShooks, simple_model_dir, sess)
        print(type_pattern)

        #addMid->FinalSparql
        finalSPARQL=fSparql.getSimpleSPARQL(type_pattern,q_entity)
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
        res = requests.post('http://0.0.0.0:5003/simplefreebase', data=json.dumps(payload), headers=header)
        # print(str(res.json()))

        #得到答案，处理答案，提出mid
        answer_mid_list=[]
        rdf=str(res.json())
        rdflist = re.split("ns/|\'", rdf)
        namelen = len(rdflist)
        i = 2
        while i < namelen:
            answer_mid_list.append(rdflist[i])
            i += 3
        print(answer_mid_list)

        #get description
        description=fbapi.googleFindDesc(q_entity)

        #ans triple
        ansTriple,parse,entityname=getAnsTriple.getAnswerTriple(q_entity,answer_mid_list,type_pattern)
        print('-------------------')
        print(ansTriple)
        triplelen=len(ansTriple)
        print(triplelen)

        # #most 15
        # triplelen=len(ansTriple)
        
        res = {
            'desc': description,
            'ansTriple': ansTriple,
            'entityname':entityname,
            'q_entity':q_entity,
            'parse':parse,
            'triplelen':triplelen,
        }

        return res, 200

class AnswerShow(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('entityname', type=str, location='json')
        self.reqparse.add_argument('q_entity', type=str, location='json')
        self.reqparse.add_argument('parse', type=str, location='json')
        self.reqparse.add_argument('triplelen', type=str, location='json')
        super(AnswerShow, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        entityname = args['entityname'] 
        q_entity = args['q_entity']
        parse=args['parse']
        triplelen=int(args['triplelen'])

        othertriple=[]
        if triplelen<15:
            othertriple=getAnsTriple.getOtherTriple(entityname,q_entity,parse,triplelen)
            print(othertriple)

        triplelen=triplelen+len(othertriple)
        print(triplelen)

        typetriple=[]
        if triplelen<15:
            typetriple=getAnsTriple.getTypeTriple(entityname,q_entity,triplelen)
            print(typetriple)
        othertriple=othertriple+typetriple

        res = {
            'otherTriple': othertriple,
        }

        return res, 200

class EntityResearch(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('keyword', type=str)
        super(EntityResearch, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        keyword = args['keyword']
        keylist,keynamelist = getmid.FindMid(keyword)  # 得到midlist
        final_key=keylist[0]
        final_key_name=keynamelist[0]

        #description
        key_description=fbapi.googleFindDesc(final_key)

        #triple
        ansTriple=[]
        #alias
        aliasname=frontStart.aliastable.find({'mid':final_key})
        for alias in aliasname:
            temp=[]
            temp.append(final_key_name)
            temp.append('common.topic.alias')
            temp.append(alias['name'])
            ansTriple.append(temp)
        #type
        commontype=frontStart.commontable.find_one({'mid':final_key})
        if commontype is not None:
            ansTriple.append([final_key_name,'common.topic.notable_types',commontype['type']])
        othertype=frontStart.othertable.find({'mid':final_key})
        if othertype is not None:
            for other in othertype:
                ansTriple.append([final_key_name,'type.object.type',other['type']])

        triplelen=len(ansTriple)
        otherTriple=[]
        otherthird=[]
        temp=[]
        if triplelen<15:
            randomparse=frontStart.showtable.find({'mid':final_key}).limit(15-triplelen)
            for r in randomparse:
                otherthird.append(r['e2'])
                temp.append([r['e2'],r['parse']])
            thirdname,thirdid=findFbname.googleFindname(otherthird)
            for t in temp:
                index=thirdid.index(t[0])
                otherTriple.append([final_key_name,t[1],thirdname[index]])

        res = {
            'description': key_description,
            'keyTriple': ansTriple,
            'otherTriple':otherTriple,
        }
        return res, 200


class EntityAnswer(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('question', type=str)
        super(EntityAnswer, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        inputquestion = args['question']

        IOBlist = evaluate.interactive_shell(web_entitymodel, inputquestion)  # 将inputquestion放进model中  ==>  IOB list
        entitylist = tomid.findEntityname(inputquestion, IOBlist)  # 得到entitylist
        midlist = getmid.FindMid(entitylist)  # 得到midlist

        # 将问句转换为type_pattern
        typelist = gettype.getType(midlist, inputquestion)  # 得到type
        print('typelist-->', typelist)
        # 转换typepattern
        typelen = len(typelist)
        typepattern = ""
        for i in range(typelen):
            typepattern = inputquestion.replace(entitylist[i], '<' + typelist[i] + '>')
        print(typepattern)
        ftype_q.write(typepattern)
        ftype_q.close()

        # 将type pattern 放sparql模型中
        # flags_tasks = "- class: DecodeText"
        # flags_model_params = "{}"
        # model_dir = "/Users/jipeng/htdocs/lkdocs/7.14/seq2seq/simple_type"
        sess = None

        # 初始化webqa sparql model
        # WSmodel, WShooks = webload.infer(flags_tasks, model_dir, flags_model_params)
        flags_input_pipeline = "class: ParallelTextInputPipeline\nparams:\n  source_files:\n  - type_q.txt"

        result, sess = webload.everySenPre(flags_input_pipeline, WSmodel, WShooks, web_model_dir, sess)
        print(result)


class EntityFeedback(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('feedback', type=str, required=True,
                                   help='No feedback provided', location='json')
        super(EntityFeedback, self).__init__()

    def post(self):
        # 写库
        args = self.reqparse.parse_args()
        print(args['feedback'])
        res = {

        }
        return res, 200


class MyException(Exception):
    def __init__(self,message):
        Exception.__init__(self)
        self.message=message  

# flags_input_pipeline = "class: ParallelTextInputPipeline\nparams:\n  source_files:\n  - type_q2.txt"
#
# result, sess = webload.everySenPre(flags_input_pipeline, WSmodel, WShooks, web_model_dir, sess)
# print(result)


# 路由
api.add_resource(EntityRecognization, '/api/EntityRecognization')
api.add_resource(EntityResearch, '/api/EntityResearch')
api.add_resource(EntityAnswer, '/api/EntityAnswer')
api.add_resource(EntityFeedback, '/api/EntityFeedback')
api.add_resource(AnswerShow, '/api/AnswerShow')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True,use_reloader=False)




