import json
import urllib.parse
import urllib.request

service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
params = {
    'ids': '/m/02pj2v6',
    'limit': 1,
    'indent': True,
    'key': 'AIzaSyCTs4ymbvhpGu4fNDB2VhUHUBHZ2SeYgWA',
}
url = service_url + '?' + urllib.parse.urlencode(params)
response = json.loads(urllib.request.urlopen(url).read())
description=''
for element in response['itemListElement']:
    print(element['result']['detailedDescription']['articleBody'])