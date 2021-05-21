import pandas as pd
import numpy as np

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

data = open("./../output/review_sample_100000.txt", "r")
cv = CountVectorizer(stop_words = 'english', strip_accents="unicode")
df = cv.fit_transform(data)
lda = LatentDirichletAllocation(n_components=10, random_state=0)
lda.fit(df)

for index, topic in enumerate(lda.components_):
    print('Top 15 words for Topic #%d' % index)
    print([cv.get_feature_names()[i] for i in topic.argsort()[-15:]])
    print('\n')
