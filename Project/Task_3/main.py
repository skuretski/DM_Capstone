from gensim.models import KeyedVectors
from gensim.models.phrases import Phrases, Phraser
from time import time
from collections import defaultdict, OrderedDict
import gensim.models
import gensim.downloader
import pandas as pd
import logging, re, spacy, pickle
import argparse
import multiprocessing

logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)

# Taken from https://www.kaggle.com/pierremegret/gensim-word2vec-tutorial
def cleaning(doc):
  # Lemmatizes and removes stopwords
  # doc needs to be a spacy Doc object
  txt = [token.lemma_ for token in doc if not token.is_stop]
  # Word2Vec uses context words to learn the vector representation of a target word,
  # if a sentence is only one or two words long,
  # the benefit for the training is very small
  if len(txt) > 2:
      return ' '.join(txt)

# Taken from https://www.kaggle.com/pierremegret/gensim-word2vec-tutorial
def preprocess(data_frame):
  regex_clean = (re.sub("[^A-Za-z']+", ' ', str(row)).lower() for row in data_frame[0])

  nlp_en = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

  txt = [cleaning(doc) for doc in nlp_en.pipe(regex_clean, batch_size=5000, n_threads=-1)]

  df_clean = pd.DataFrame({'clean': txt})
  df_clean = df_clean.dropna().drop_duplicates()
  df_clean.to_pickle('cleaned.pickle')
  return df_clean

def main(args):
  # Own model
  if not args.google:
    if args.pickle:
      df = pd.read_pickle('cleaned.pickle')
    else:
      df = pd.read_csv('../scripts/categories/Italian.txt', delimiter="\t", header=None)
      df = preprocess(df)
    
    sent = [row.split() for row in df['clean']]
    phrases = Phrases(sent, min_count=30, progress_per=10000)
    bigram = Phraser(phrases)
    sentences = bigram[sent]
    word_freq = defaultdict(int)
    for sent in sentences:
        for i in sent:
            word_freq[i] += 1
    print("Most frequent words:\n")
    print(sorted(word_freq, key=word_freq.get, reverse=True)[:10])
    
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

  # Pre-trained model
  else:
    model = KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)

  df_it = pd.read_csv('./italian.label', delimiter="\t", header=None)

  pos_labels = df_it.loc[df_it[1] == 1.0][0].to_numpy()
  neg_labels = df_it.loc[df_it[1] == 0.0][0].to_numpy()

  embedding_vector = []
  for word in pos_labels: 
    word = word.replace(' ', '_')
    try:
      result = model.most_similar(positive=[word], topn=5, restrict_vocab=None)
      embedding_vector.extend(result)
    except: print(word, 'not found')
  sorted_vector = sorted(embedding_vector, key=lambda tup: tup[1], reverse=True)
  dupe_removed_vector = list(OrderedDict(sorted_vector[::-1]).items())[::-1]
  
  file = open("results.txt", 'w')
  for item in dupe_removed_vector:
    word = item[0].replace('_', ' ')
    file.write(f'{word}\t{item[1]}\n')
  file.close()
  return

if __name__ =="__main__":
  parser = argparse.ArgumentParser(description='Script for Word2Vec')
  parser.add_argument('--pickle', action='store_true')
  parser.add_argument('--google', action='store_true')
  args = parser.parse_args()
  main(args)
