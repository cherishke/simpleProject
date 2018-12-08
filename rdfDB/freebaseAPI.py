import json
import urllib.parse
import urllib.request

class GooleKGAPI(object):
    def __init__(self):
        # self.api_key = open('api_key').read()
        self.api_key='AIzaSyCTs4ymbvhpGu4fNDB2VhUHUBHZ2SeYgWA'

    def getResult(self,midlist):
        service_url = 'https://kgsearch.googleapis.com/v1/entities:search'

        params = {
            'indent': True,
            'key': self.api_key,
        }
        pa = ''
        num=0
        for item in midlist:
            if num<15:
                pa += ('&' + urllib.parse.urlencode({ 'ids': item }))
                num+=1

        url = service_url + '?' + urllib.parse.urlencode(params) + pa
        # print(url)
        response = json.loads(urllib.request.urlopen(url).read())
        ansnameList=[]
        idlist=[]
        for element in response['itemListElement']:
            # print(element['result']['name'])
            idlist.append(element['result']['@id'].replace('/','.')[4:])
            ansnameList.append(element['result']['name'])

        # print(idlist)
        return ansnameList,idlist

    def getDescription(self,entitymid):
        service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
        params = {
            'ids': entitymid,
            'limit': 1,
            'indent': True,
            'key': self.api_key,
        }
        url = service_url + '?' + urllib.parse.urlencode(params)
        response = json.loads(urllib.request.urlopen(url).read())
        description=''
        for element in response['itemListElement']:
            description=element['result']['detailedDescription']['articleBody']
            # description=element['result']['detailedDescription']['articleBody']

        return description

    
def googleFindname(midlist):
    gkg = GooleKGAPI()
    for i in range(len(midlist)):
        midlist[i]='/'+midlist[i].replace('.','/')
    
    ansnameList,ansidlist=gkg.getResult(midlist)

    return ansnameList,ansidlist

def googleFindDesc(entitymid):
    gkg = GooleKGAPI()
    entitymid='/'+entitymid.replace('.','/')
    description=gkg.getDescription(entitymid)

    return description




