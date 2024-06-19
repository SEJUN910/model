import re
import os
import json
from konlpy.tag import Kkma
from gensim.models import Word2Vec
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from dotenv import load_dotenv
import google.generativeai as genai
import typing_extensions as typing

# JSON CLASS
class JsonForm(typing.TypedDict):
    contents: str

# 제미나이 API 키 설정
load_dotenv()
api_key=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

es = Elasticsearch(
    hosts='https://elastic:ytNr+zAQ3RSPc+L7vkxt@localhost:9200',
    ca_certs='./http_ca.crt',
    verify_certs=False
    )

kkma = Kkma()

# 불용어 목록
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
model_list = ['key-model-123.model', 'key-model-theme.model', 'key-model-mall.model', 'key-model-words.model', 'normal']

class ModelClass:
    # 기본설정 question만 받음
    def __init__(self, keyword, model):
        self.keyword = keyword
        self.model = model

    def getKeyword(self):
        keyword = self.keyword
        model = self.model
        model_name = model_list[model]

        if model == 4:
            gemini = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
            prompt = str(keyword)
            response = gemini.generate_content(prompt)
            return { 'all': [], 'sep': {'theme': [], 'mall': [], 'words': []}, 'keywords': [], 'praying': response.text.replace("\n", "<br>") }


        tokenized_sentence = kkma.morphs(keyword)
        filtered_tokens = [token for token in tokenized_sentence if re.search('[가-힣]', token) ]
        filtered_tokens2 = [token for token in filtered_tokens if not re.search('[ㄱ-ㅎ]', token) ]
        stopwords_removed_sentence = [word for word in filtered_tokens2 if not word in stopwords] # 불용어 제거
        filtered_tokens3 = [ word for word in stopwords_removed_sentence if len(word) > 1 ]
        searchWord = filtered_tokens3

        keywords = [keyword]
        
        try:
            wordModel = Word2Vec.load(model_name)
            for key in searchWord:
                modelWord = wordModel.wv.most_similar(key)
            
                for words in modelWord:
                    if not re.search('[0-9]', words[0]):
                        keyword = words[0]
                        keywords.append(keyword)
        except:
            pass
        
        s_keyword = ' '.join(keywords)
        search = es.search(index='search_list', query={"match": {"contents": s_keyword}}, source=['kind','code','title','relat_date','point','isbn', 'contents'], aggs={ "by_kind": { "terms": { "field": "kind", "include": ["mall", "theme", "words"] }, "aggs": { "top_documents": { "top_hits": { "size": 3, "_source": ['kind','code','title','relat_date','point','isbn', 'contents']}}} } })

        hits = search['hits']['hits']
        recom = search['aggregations']['by_kind']['buckets']

        list_1 = []
        for item in hits:
            
            source = item['_source']
            score = item['_score']
            code = source['code']
            kind = source['kind']
            isbn = source['isbn']
            title = source['title']
            date = source['relat_date']
            point = source['point']
            contents = ''
            if kind == 'mall':
                link = 'https://mall.godpeople.com/?G='+code
                type = '도서'
            elif( kind == 'theme' ):
                link = 'https://cnts.godpeople.com/p/'+code
                type = '테마'
            else:
                link = '성경코드:'+code
                type = '성경'
                contents = source['contents']
            
            
            each = { 'type':type, 'title':title, 'link':link, 'isbn':isbn, 'date':date, 'point':point, 'score':score, 'code': code, 'contents': contents }
            list_1.append(each)

        list_2 = {'theme': [], 'mall': [], 'words': []}
        for item in recom:
            key = item['key']
            doc = item['top_documents']
            hits = doc['hits']['hits']
            for item in hits:
                source = item['_source']
                score = item['_score']
                code = source['code']
                kind = source['kind']
                isbn = source['isbn']
                title = source['title']
                date = source['relat_date']
                point = source['point']
                contents = ''
                if kind == 'mall':
                    link = 'https://mall.godpeople.com/?G='+code
                    type = '도서'
                elif( kind == 'theme' ):
                    link = 'https://cnts.godpeople.com/p/'+code
                    type = '테마'
                else:
                    link = '성경코드:'+code
                    type = '성경'
                    contents = source['contents']
                
                each = { 'type':type, 'title':title, 'link':link, 'isbn':isbn, 'date':date, 'point':point, 'score':score, 'code': code,'contents': contents }
                list_2[key].append(each)

        gemini = genai.GenerativeModel(model_name='models/gemini-1.5-pro')
        prompt_keywords = str(','.join(keywords))
        prompt = f"""
            저는 올바른 기도문을 제공하는 목사입니다.
            모든 답변은 한국어로 해주시고, 단어를 강조하시거나 특수문자를 넣지 말고 답변해주세요.
            [{prompt_keywords}] 키워드로 기도문을 작성해주세요.
        """
        
        response = gemini.generate_content(prompt)
        print(response.text)
        return { 'all': list_1, 'sep': list_2, 'keywords': keywords, 'praying': response.text.replace("\n", "<br>")}
        


