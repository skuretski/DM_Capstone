import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB

def get_word_vector():
  corpus = []
  with open('../Task_6/data/hygiene.dat', 'r') as f:
    for line in f:
      line = re.sub(r'[^A-Za-z\s]', '', line)
      corpus.append(line)
  
  vectorizer = CountVectorizer()
  X = vectorizer.fit_transform(corpus)
  return X.toarray()

def get_y():
  return

def main():
  df = pd.read_csv('../Task_6/data/hygiene.dat.additional', sep=",", usecols=[0,1,2,3], names=['Categories', 'Zip_Code', 'Num_Reviews', 'Rating'])
  word_vector = get_word_vector()


  return


if __name__ == "__main__":
  main()