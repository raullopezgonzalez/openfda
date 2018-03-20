import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.github.com")
conn.request("GET", "/orgs/elastic/repos", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
print("total number of repositories",len(repos))

x = 0
while x < 30:
    
    print("The owner of this repository is", repos[x]['full_name'])
    
    x += 1
    


