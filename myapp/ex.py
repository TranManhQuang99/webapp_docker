import requests
import json

url = "http://10.0.8.114:9200/monstache_test/_search"

payload = json.dumps({
  "query": {
    "match": {
      "post": "AI"
    }
  },
  "size": 100
})

headers = {
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)
hits = json.loads(response.text)
data = (hits['hits']['hits'])

for i in data:
  print(i['_source'])