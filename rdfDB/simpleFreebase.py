import rdflib
import pyparsing
import time
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, request

app = Flask(__name__)
api = Api(app)


g = rdflib.Graph()
# g.parse('triple.rdf',format='nt')
start=time.time()
g.parse('/Users/jipeng/htdocs/lkdocs/freebase/fb2m.rdf',format='nt')
# g.parse('triple.rdf',format='nt')
end=time.time()
print(end-start)
print('=================')

class SimpleFreebase(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('sparql', type=str, default="", location='json')
        super(SimpleFreebase, self).__init__()
    def get(self):
        print(123)
    def post(self):

        args = self.reqparse.parse_args()
        q = args['sparql']
        print(q)
        try:
            # q=input('sparql:')
            querystart = time.time()
            x = g.query(q)
            queryend = time.time()
            print(queryend - querystart)
            print(list(x))
            return list(x), 200
            print('~~~~~~~~~~~~~~~~~')
        except pyparsing.ParseException:
            print('error')


# 路由
api.add_resource(SimpleFreebase, '/simplefreebase')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True, use_reloader=False)
# 