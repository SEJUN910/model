import sys
import time
import re
import os
from konlpy.tag import Kkma
from gensim.models import Word2Vec

start_time = time.time()

# input = sys.argv[1]
input = '예수'

model_path1 = 'data/model/key-model-123.model'
model_path2 = 'data/model/key-model-mall.model'
model_path3 = 'data/model/key-model-theme.model'

model = Word2Vec.load(model_path3)
kkma = Kkma()

stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

tokenized_sentence = kkma.morphs(input)
filtered_tokens = [token for token in tokenized_sentence if re.search('[가-힣]', token) ]
filtered_tokens2 = [token for token in filtered_tokens if not re.search('[ㄱ-ㅎ]', token) ]
stopwords_removed_sentence = [word for word in filtered_tokens2 if not word in stopwords] # 불용어 제거
searchWord = stopwords_removed_sentence[0]
# print(stopwords_removed_sentence)

resultNos = {}

# 답변내용을 담습니다.
template_answer = ''

test_word = model.wv.most_similar(searchWord)
# print(test_word)
keywords = [searchWord]
for words in test_word:
    keyword = words[0]
    keywords.append(keyword)

print(keywords)
end_time = time.time()
result = end_time - start_time
print("실행시간:", result, "초")
quit()