from gensim.test.utils import datapath
from gensim import utils
from gensim.models.phrases import Phrases, Phraser
from time import time
from collections import defaultdict
import gensim.models
import gensim.downloader
import pandas as pd
import logging, re, spacy, pickle
import argparse
import multiprocessing
import nltk
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
class MyCorpus:
  """An iterator that yields sentences (lists of str)."""

  def __iter__(self):
    corpus_path = datapath('../scripts/categories/Italian.txt')
    for line in open(corpus_path):
      # assume there's one document per line, tokens separated by whitespace
      yield utils.simple_preprocess(line)

def cleaning(doc):
  # Lemmatizes and removes stopwords
  # doc needs to be a spacy Doc object
  txt = [token.lemma_ for token in doc if not token.is_stop]
  # Word2Vec uses context words to learn the vector representation of a target word,
  # if a sentence is only one or two words long,
  # the benefit for the training is very small
  if len(txt) > 2:
      return ' '.join(txt)

def preprocess(data_frame):
  regex_clean = (re.sub("[^A-Za-z']+", ' ', str(row)).lower() for row in data_frame[0])

  nlp_en = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

  txt = [cleaning(doc) for doc in nlp_en.pipe(regex_clean, batch_size=5000, n_threads=-1)]

  df_clean = pd.DataFrame({'clean': txt})
  df_clean = df_clean.dropna().drop_duplicates()
  df_clean.to_pickle('cleaned.pickle')
  return df_clean

def main(args):
  if args.pickle:
    df = pd.read_pickle('cleaned.pickle')
  else:
    df = pd.read_csv('../scripts/categories/Italian.txt', delimiter="\t", header=None)
    print(df.columns)
    df = preprocess(df)
  sent = [row.split() for row in df['clean']]
  phrases = Phrases(sent, min_count=30, progress_per=10000)
  bigram = Phraser(phrases)
  sentences = bigram[sent]
  word_freq = defaultdict(int)
  for sent in sentences:
      for i in sent:
          word_freq[i] += 1
  print(len(word_freq))


  cores = multiprocessing.cpu_count() # Count the number of cores in a computer
  model = gensim.models.Word2Vec(
    min_count=20, 
    window=2, 
    vector_size=300, 
    sample=6e-5, 
    alpha=0.03, 
    min_alpha=0.0007, 
    negative=20, 
    workers= cores-1)
  t = time()
  model.build_vocab(sentences, progress_per=10000)
  print('Time to build vocab: {} mins'.format(round((time() - t) / 60, 2)))

  t = time()
  model.train(sentences, total_examples=model.corpus_count, epochs=30, report_delay=1)
  print('Time to train the model: {} mins'.format(round((time() - t) / 60, 2)))

  all_normed_vectors = model.wv.get_normed_vectors()

  df_it = pd.read_csv('./italian.label', delimiter="\t", header=None)
  print(df_it[1])
  pos_labels = df_it.loc[df_it[1] == 1.0][0].to_numpy()
  #print(df_it.loc[df_it[1] == '1'])
  print(pos_labels)
  neg_labels = df_it.loc[df_it[1] == 0.0][0].to_numpy()
  print(neg_labels)
  for word in pos_labels: 
    try: embedding_vector = model.wv.most_similiar(positive=[word], topn=20, restrict_vocab=None)
    except: print(word, 'not found')
  #print(model.wv.most_similar(positive=pos_labels, negative=neg_labels, topn=20, restrict_vocab=None))
  return

if __name__ =="__main__":
  parser = argparse.ArgumentParser(description='Script for Word2Vec')
  parser.add_argument('--pickle', action='store_true')
  args = parser.parse_args()
  main(args)
