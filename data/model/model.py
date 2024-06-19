import os
import requests
import json
import csv
import time
import re
from gensim.models import Word2Vec

start_time = time.time()

tokenized_data = []
# with open('data/data/theme_ko_sample_v2.csv', encoding='utf-8') as file:
#     csv_reader = csv.reader(file)
#     for idx, cell in enumerate(csv_reader):
#         keywords = cell[1].split(',')
#         tokenized_data.append(keywords)
#         print(idx)

# with open('data/data/mall_data.csv', encoding='utf-8') as file:
#     csv_reader = csv.reader(file)
#     for idx, cell in enumerate(csv_reader):
#         keywords = cell[1].split(',')
        
#         if '폰트' in keywords :
#             keywords.remove('폰트')

#         tokenized_data.append(keywords)
#         print(idx)

with open('data/data/words_data.csv', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    for idx, cell in enumerate(csv_reader):
        keywords = cell[1].split(',')
        tokenized_data.append(keywords)
        print(idx)

model = Word2Vec(sentences=tokenized_data, vector_size=300, window=10, min_count=5, workers=4, sg=0)
model.save("data/data/key-model-words.model")
print(model.wv.vectors.shape)

end_time = time.time()
result = end_time - start_time
print("실행시간:", result, "초")
quit()