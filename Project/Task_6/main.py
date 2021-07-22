import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import load_wine

def get_word_vector():
  corpus = []
  with open('../Task_6/data/hygiene.dat', 'r') as f:
    for line in f:
      line = re.sub(r'[^A-Za-z\s]', '', line)
      corpus.append(line)
  f.close()
  vectorizer = CountVectorizer()
  X = vectorizer.fit_transform(corpus)
  return X.toarray()

def get_y():
  train = []
  test = []
  with open('../Task_6/data/hygiene.dat.labels', 'r') as f:
    for line in f:
      line = list(line)
      for ch in line:
        if ch == '1' or ch == '0':
          train.append(int(ch))
        else:
          test.append(None)
  f.close()
  return train, test

def main():
  df = pd.read_csv('../Task_6/data/hygiene.dat.additional', sep=",", usecols=[0,1,2,3], names=['Categories', 'Zip_Code', 'Num_Reviews', 'Rating'])
  vectorizer = CountVectorizer()
  categories = []
  for index, row in df.iterrows():
    categories.append(row['Categories'])
  X = vectorizer.fit_transform(categories)
  

  word_vector = get_word_vector()
  train, test = get_y()
  features, target = load_wine(return_X_y=True)
  print(features)
  return


if __name__ == "__main__":
  main()