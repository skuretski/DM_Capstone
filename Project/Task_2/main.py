import glob, random, pandas, argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity

def Tf_MaybeIDF(corpus, IDF:bool = True):
  vectorizer = TfidfVectorizer( strip_accents='unicode', 
                                max_df=0.5, min_df=2, 
                                stop_words='english', 
                                max_features=10000, 
                                use_idf=IDF)
  X = vectorizer.fit_transform(corpus)
  return X

def generate_csv(cosine_sim_matrix, column_names, file_name):
  output = []
  for i in range(len(column_names) - 1):
    for j in range(len(column_names) - 1):
      row = [column_names[i], column_names[j], cosine_sim_matrix[i][j]]
      output.append(row)

  pandas.DataFrame(output).to_csv(file_name, sep=',', header=['a', 'b', 'value'])

def main(args):
  text = []
  c_names = []
  cat_list = glob.glob("../scripts/categories/*")
  cat_size = len(cat_list)

  sample_size = min(30, cat_size)
  cat_sample = sorted(random.sample(range(cat_size), sample_size) )
  #print (cat_sample)
  count = 0
  for i, item in enumerate(cat_list):
    if i == cat_sample[count]:
      li =  item.split('/')
      cuisine_name = li[-1]
      c_names.append(cuisine_name[:-4].replace("_"," "))
      with open ( item ) as f:
        text.append(f.read().replace("\n", " "))
      count = count + 1
    
    if count >= len(cat_sample):
      print(f"Generating cuisine matrix with {count} cuisines")
      break

  if args.all:
    if args.tf or args.all:
      X1 = Tf_MaybeIDF(text, False)
      cosine_sim_1 = cosine_similarity(X1, X1)
      generate_csv(cosine_sim_1, c_names, 'tf_similarity_matrix.csv')
    if args.tfidf or args.all:
      X2 = Tf_MaybeIDF(text)
      cosine_sim_2 = cosine_similarity(X2, X2)
      generate_csv(cosine_sim_2, c_names, 'tfidf_similarity_matrix.csv')
    if args.lda or args.all:
      X3 = Tf_MaybeIDF(text)
      lda = LatentDirichletAllocation(n_components=args.n_components, max_iter=10, learning_method='online', learning_offset=50., random_state=0)
      X4 = lda.fit_transform(X3)
      cosine_sim_3 = cosine_similarity(X4, X4)
      generate_csv(cosine_sim_3, c_names, 'lda_similarity_matrix.csv')

  

if __name__ =="__main__":
  parser = argparse.ArgumentParser(description='Script to make CSV of similarity matrix using different models and methods.')

  parser.add_argument('--tf', action='store_true',
                    help='Create similiarity matrix based on term frequency only.')
  parser.add_argument('--tfidf', action='store_true',
                    help='Create similarity matrix based on TF-IDF.')
  parser.add_argument('--lda', action='store_true',
                    help='Incorporates LDA topic model to create similarity matrix.')
  parser.add_argument('--n_components', type=int, default=10, help='Number of components for LDA'),
  parser.add_argument('--all', action='store_true',
                    help='Does all of the above.')
  args = parser.parse_args()
  main(args)
