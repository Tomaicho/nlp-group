import requests
from bs4 import BeautifulSoup
import json

with open('/Users/florianhetzel/Desktop/PLNEB/Practical/Second assignment/terms2.json') as file:
    dict = json.load(file)

for term_pt, dic in dict.items():
    terms_en = dic['en'].split(',')
    for term_en in terms_en:
        term_en = term_en.strip()
        link = f'https://www.oxfordlearnersdictionaries.com/definition/english/{term_en}?q={term_en}'
        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"}
        print(link)
        html_content = requests.get(link, headers= headers).text


        soup = BeautifulSoup(html_content, 'html.parser')

        topic_list = []
        span_list = soup.find_all('span', class_="topic_name")
        for span in span_list:
            topic = span.text.strip()
            topic_list.append(topic)

        if topic_list:
            print(term_pt, term_en, ' -> ', topic)
            dict[term_pt]['category'] = topic_list[0]
            with open('terms2.json', 'w') as file:
                json.dump(dict, file, indent=6, ensure_ascii=False)