import json
import pandas as pd
from wordcloud import WordCloud, STOPWORDS

with open ('../Task_1/data/1.2/wordcloud/low/subsample_top_words_lda.json', 'r') as f:
  text = ''.join(f.readlines())
  text = text.replace('\n', '')

  json_line = json.loads(text)
  print(json_line)

f.close()