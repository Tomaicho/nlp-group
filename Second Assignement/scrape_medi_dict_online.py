import requests
from bs4 import BeautifulSoup
import json

'''with(open("Second assignment/terms_v1.json",  encoding="utf-8") as file):
    terms_v1 = json.load(file) 

with(open("/Users/florianhetzel/Desktop/PLNEB/Practical/Second assignment/harvard_terms.json",  encoding="utf-8") as file):
    dic = json.load(file) '''

base_url = 'https://www.online-medical-dictionary.org/glossary'
headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"}
html_content = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(html_content, 'html.parser')

#class="card-body"
anchors = soup.find_all(class_="card-body")
anchors = anchors[-1]
soup_1 = BeautifulSoup(str(anchors), 'html.parser')
anchors = [anchor['href'] for anchor in soup_1.find_all('a')]

url_socket = 'https://www.online-medical-dictionary.org'
urls = []
for anchor in anchors:
    urls.append(url_socket + anchor)

dic = {}
for page in urls:
    print(page)
    page = requests.get(page, headers=headers).text
    page_html = BeautifulSoup(page, 'html.parser')
    body = page_html.find_all('li')
    termlinks = [url_socket + termlink.a['href'] for termlink in body]

    for termlink in termlinks:
        termpage = requests.get(termlink, headers=headers).text
        term_html = BeautifulSoup(termpage, 'html.parser')
        term = term_html.find('h2').text
        print(term)
        des_en = term_html.find('p').text
        relations = [relation.text for relation in term_html.find('p').find_all('a')]
        dic[term] = {'des_en':des_en, 'relations':relations}



with open('jsons/medi_dict_online_terms.json','w') as file:
    json.dump(dic,file, indent=6, ensure_ascii=False)