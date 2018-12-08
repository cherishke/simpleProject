#coding=utf-8
import pymongo
import simpleEntityModel.evaluate as simpleevaluate
import simpleSPARQLmodel.LoadModel as simpleload

#开启mongo数据库  ==> worddict
conn = pymongo.MongoClient('127.0.0.1', 27017)
db = conn['tripleDB']
realtable = db.realdict
aliastable = db.aliasdict

typedb = conn['typeDB']
commontable = typedb.commontype
othertable = typedb.othertype

midname=conn['midname']
midtable=midname.midname

showTripleDB=conn['showTripleDB']
showtable=showTripleDB.triple

def frontstart():
    #启动simple entity模型，返回
    simple_entitymodel = simpleevaluate.evalmain()
    print('done')

    # # 初始化webqa sparql model
    # web_flags_tasks = "- class: DecodeText"
    # web_flags_model_params = "{}"
    # # web_model_dir = "/Users/jipeng/htdocs/lkdocs/7.14/seq2seq/webqa_type"
    # web_model_dir='SPARQLmodel/web_type_model/best_webSPARQL'
    # WSmodel, WShooks = webload.infer(web_flags_tasks, web_model_dir, web_flags_model_params)

    # 初始化simple sparql model
    simple_flags_tasks = "- class: DecodeText"
    simple_flags_model_params = "{}"
    # simple_model_dir = "/Users/jipeng/htdocs/lkdocs/7.14/seq2seq/simple_type"
    simple_model_dir='bestSPARQLmodel'
    SSmodel, SShooks = simpleload.infer(simple_flags_tasks, simple_model_dir, simple_flags_model_params)

    return simple_entitymodel,SSmodel, SShooks

#返回要选的数据集
#def chooseDataset()：


