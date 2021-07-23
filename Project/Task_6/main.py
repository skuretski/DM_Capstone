import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import train_test_split

def get_word_vector():
  corpus = []
  with open('../Task_6/data/hygiene.dat', 'r') as f:
    for line in f:
      line = re.sub(r'[^A-Za-z\s]', '', line)
      corpus.append(line)
  f.close()
  vectorizer = CountVectorizer(strip_accents="unicode", stop_words="english")
  X = vectorizer.fit_transform(corpus)
  return X.toarray()

def vectorize_this(df, column):
  result = []
  vectorizer = CountVectorizer()
  for index, row in df.iterrows():
    result.append(str(row[column]))

  X = vectorizer.fit_transform(result)

  feature_vector = X.toarray()
  for index, row in enumerate(feature_vector):
    df.at[index, column] = row
  return df

def vectorize(df):
  word_vector = get_word_vector()
  df['Reviews'] = None
  for index, row in enumerate(word_vector):
    df.at[index, 'Reviews'] = row

  for column in df:
    if column == 'Categories' or column == 'Zip_Code':
      df = vectorize_this(df, column)
  return df

def get_y():
  labels = []
  with open('../Task_6/data/hygiene.dat.labels.txt', 'r') as f:
    for line in f:
      line = list(line)
      for ch in line:
        if ch == '0' or ch == '1':
          labels.append(int(ch))
  f.close()
  return labels

def main():
  df = pd.read_csv('../Task_6/data/hygiene.dat.additional', sep=",", usecols=[0,1,2,3], names=['Categories', 'Zip_Code', 'Num_Reviews', 'Rating'])
  df['Zip_Code'] = df['Zip_Code'].astype(str)
  df = vectorize(df)
  del df['Zip_Code']
  del df['Reviews']
  del df['Categories']
  df_X = df[['Num_Reviews', 'Rating']]
  labels = get_y()

  X_train, X_test, y_train, y_test = train_test_split(df_X, labels, train_size=0.60, shuffle=False)
  print(X_train)
  # mnb = MultinomialNB()
  # mnb.fit(X_train, y_train)
  # y_pred = mnb.predict(X_test)
  # print("F1 Score: ", f1_score(y_test, y_pred))

  return


if __name__ == "__main__":
  main()