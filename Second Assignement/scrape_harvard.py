import requests
from bs4 import BeautifulSoup
import json

with(open("jsons/terms_v1.json",  encoding="utf-8") as file):
    terms_v1 = json.load(file) 

with(open("/Users/florianhetzel/Desktop/PLNEB/Practical/Second assignment/harvard_terms.json",  encoding="utf-8") as file):
    dic = json.load(file) 

base_url = 'https://www.health.harvard.edu/a-through-c#A-terms'
headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"}
html_content = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(html_content, 'html.parser')

#class="content-repository-content prose max-w-md-lg mx-auto flow-root getShouldDisplayAdsAttribute"
anchors = soup.find_all(class_="content-repository-content prose max-w-md-lg mx-auto flow-root getShouldDisplayAdsAttribute")
anchors = str(anchors[0].p)
soup_ = BeautifulSoup(anchors, 'html.parser')
anchors = [anchor['href'] for anchor in soup_.find_all('a')]

url_socket = 'https://www.health.harvard.edu'
urls = []
for anchor in anchors:
    urls.append(url_socket + anchor)

urls = urls[16]
print(urls)
page = requests.get(urls, headers=headers).text
page_html = BeautifulSoup(page, 'html.parser')
body = page_html.find(class_='content-repository-content prose max-w-md-lg mx-auto flow-root getShouldDisplayAdsAttribute')
body_html = BeautifulSoup(str(body), 'html.parser')
all_ps = body_html.find_all('p')
for p in all_ps[2:-1]:
    p_html = BeautifulSoup(str(p), 'html.parser')
    item = p_html.text
    list = item.split(':')
    if len(list) == 2:
        dic[list[0]] = list[1]

with open('jsons/harvard_terms.json','w') as file:
    json.dump(dic,file, indent=6, ensure_ascii=False)