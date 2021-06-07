import glob, random, pandas, argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans, DBSCAN
from scipy.spatial.distance import cdist

def TfIdfSimilarity(corpus, IDF:bool = True):
  vectorizer = TfidfVectorizer( max_df=0.5, min_df=2, 
                                stop_words='english', 
                                max_features=10000, 
                                use_idf=IDF)
  X = vectorizer.fit_transform(corpus)

  return np.vstack([cosine_similarity(val, X) for val in X])

def generate_csv(cosine_sim_matrix, column_names, file_name, labels=None):
  output = []
  for i in range(len(column_names) - 1):
    for j in range(len(column_names) - 1):
      if labels is None:
        row = [column_names[i], column_names[j], cosine_sim_matrix[i][j]]
      else:
        row = [column_names[i], column_names[j], cosine_sim_matrix[i][j], labels[i]]
      output.append(row)
  if labels is None:
    pandas.DataFrame(output).to_csv(file_name, sep=',', header=['a', 'b', 'value'])
  else:
    pandas.DataFrame(output).to_csv(file_name, sep=',', header=['a', 'b', 'value', 'cluster'])

def kmeans_clustering(matrix, n_clusters=3):
  kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit_predict(matrix)

  return kmeans

def dbscan(matrix, eps=0.5, min_samples=3):
  db = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(matrix)

  return db

def pca(matrix):
  pca = PCA(n_components=2)
  X = pca.fit_transform(matrix)

  return X

# From https://www.geeksforgeeks.org/elbow-method-for-optimal-value-of-k-in-kmeans/
def elbow(matrix, filename):
  distortions = []
  inertias = []
  mapping1 = {}
  mapping2 = {}
  K = range(1, 12)
  
  for k in K:
    # Building and fitting the model
    kmeanModel = KMeans(n_clusters=k).fit(matrix)
    kmeanModel.fit(matrix)

    distortions.append(sum(np.min(cdist(matrix, kmeanModel.cluster_centers_,
                                        'euclidean'), axis=1)) / matrix.shape[0])
    inertias.append(kmeanModel.inertia_)

    mapping1[k] = sum(np.min(cdist(matrix, kmeanModel.cluster_centers_,
                                  'euclidean'), axis=1)) / matrix.shape[0]
    mapping2[k] = kmeanModel.inertia_

  plt.plot(K, distortions, 'b')
  plt.xlabel('Values of K')
  plt.ylabel('Distortion')
  plt.title('The Elbow Method using Distortion')
  plt.savefig(filename)
  plt.clf()

def main(args):
  NUM_CLUSTERS = 8
  DBSCAN_EPS = 0.015
  text = []
  c_names = []
  cat_list = glob.glob("../scripts/categories/*")
  cat_size = len(cat_list)

  sample_size = min(50, cat_size)
  cat_sample = sorted(random.sample(range(cat_size), sample_size) )

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

  # TF Only
  if args.tf or args.all:
    sim = TfIdfSimilarity(text, False)

    labels = None
    elbow(sim, 'tf_elbow.png')

    if args.clustering:
      labels = kmeans_clustering(sim, NUM_CLUSTERS)
      generate_csv(sim, c_names, f'tf_kmeans_{NUM_CLUSTERS}.csv', labels)

      labels = dbscan(sim, 1.24)
      generate_csv(sim, c_names, 'tf_dbscan.csv', labels)

    generate_csv(sim, c_names, 'tf_similarity.csv', labels)

  # TF-IDF
  if args.tfidf or args.all:
    labels = None

    sim = TfIdfSimilarity(text)
    
    elbow(sim, 'tfidf_elbow.png')

    if args.clustering:
      labels = kmeans_clustering(sim, NUM_CLUSTERS)
      generate_csv(sim, c_names, f'tfidf_kmeans_{NUM_CLUSTERS}.csv', labels)

      labels = dbscan(sim, 1.24)
      generate_csv(sim, c_names, 'tfidf_dbscan.csv', labels)

    generate_csv(sim, c_names, 'tfidf_similarity.csv', labels)

  # LDA
  if args.lda or args.all:
    vectorizer = TfidfVectorizer(
                                max_df=0.5, min_df=2, 
                                stop_words='english', 
                                max_features=10000, 
                                use_idf=True)
    X = vectorizer.fit_transform(text)

    lda = LatentDirichletAllocation(n_components=args.n_components, max_iter=5, learning_method='online', learning_offset=50., random_state=0)
    X4 = lda.fit_transform(X)
    cosine_sim = cosine_similarity(X4, X4)
    generate_csv(cosine_sim, c_names, 'lda_similarity.csv', labels)

    vectorizer = TfidfVectorizer(
                                strip_accents='unicode',
                                max_df=0.8, min_df=2, 
                                stop_words='english', 
                                max_features=15000, 
                                ngram_range=(1,2),
                                use_idf=False)
    X = vectorizer.fit_transform(text)

    lda = LatentDirichletAllocation(n_components=args.n_components, max_iter=15, learning_method='online', learning_offset=50., random_state=0)
    X4 = lda.fit_transform(X)
    cosine_sim = cosine_similarity(X4, X4)
    generate_csv(cosine_sim, c_names, 'lda_similarity_imp.csv', labels)

    labels = None
    elbow(cosine_sim, 'lda_elbow.png')
    
    if args.clustering:
      labels = kmeans_clustering(cosine_sim, NUM_CLUSTERS)
      generate_csv(cosine_sim, c_names, f'lda_kmeans_{NUM_CLUSTERS}.csv', labels)

      labels = dbscan(cosine_sim, DBSCAN_EPS)
      generate_csv(cosine_sim, c_names, 'lda_dbscan.csv', labels)

    
if __name__ =="__main__":
  parser = argparse.ArgumentParser(description='Script to make CSV of similarity matrix using different models and methods.')

  parser.add_argument('--tf', action='store_true',
                    help='Create similiarity matrix based on term frequency only.')
  parser.add_argument('--tfidf', action='store_true',
                    help='Create similarity matrix based on TF-IDF.')
  parser.add_argument('--lda', action='store_true',
                    help='Incorporates LDA topic model to create similarity matrix.')
  parser.add_argument('--n_components', type=int, default=50, help='Number of components for LDA'),
  parser.add_argument('--clustering', action='store_true', help="Do K-Means and DBSCAN"),
  parser.add_argument('--all', action='store_true',
                    help='Does all of the above.')
  args = parser.parse_args()
  main(args)
