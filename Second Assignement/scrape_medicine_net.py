import requests
from bs4 import BeautifulSoup
import json

abc = ['s', 't', 'u', 'v', 'w', 'x', 'y', 'z']

with open('jsons/medicine_net_terms.json') as file:
        dic = json.load(file)

for letter in abc:
    base_url = f'https://www.medicinenet.com/script/main/alphaidx.asp?p={letter}_dict'
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"}
    html_content = requests.get(base_url, headers=headers).text
    soup = BeautifulSoup(html_content, 'html.parser')
    body = soup.find(class_='AZ_results')
    body_html = BeautifulSoup(str(body), 'html.parser')
    termlinks = body_html.find_all('li')

    for termlink in termlinks:
        termlink_ = 'https://www.rxlist.com' + termlink.a['href']
        term_page = requests.get(termlink_, headers=headers).text
        term_html = BeautifulSoup(term_page, 'html.parser')
        term_content = term_html.find(class_='pgContent')
        list = term_content.text.split(':')
        if len(list)==2:
            term = list[0].strip()
            des_en = list[1].strip()
        content_html = BeautifulSoup(str(term_content), 'html.parser')
        all_a = content_html.find_all('a')
        relations_list = []
        for a in all_a:
            relation = a.text
            relations_list.append(relation.strip())
        dic[term] = {'des_en':[des_en], 'relations':relations_list}
        print(term)


    with open('jsons/medicine_net_terms.json','w') as file:
        json.dump(dic,file, indent=6, ensure_ascii=False)