# Author: Olivier Grisel <olivier.grisel@ensta.org>
#         Lars Buitinck
#         Chyi-Kwei Yau <chyikwei.yau@gmail.com>
# License: BSD 3 clause

from time import time
import matplotlib.pyplot as plt
import json, re, nltk, string
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups

n_features = 50000
n_components = 10
n_top_words = 15

nltk.download('stopwords')
def plot_top_words(model, feature_names, n_top_words, title):
	fig, axes = plt.subplots(2, 5, figsize=(30, 15), sharex=True)
	axes = axes.flatten()
	for topic_idx, topic in enumerate(model.components_):
		top_features_ind = topic.argsort()[:-n_top_words - 1:-1]
		top_features = [feature_names[i] for i in top_features_ind]
		weights = topic[top_features_ind]

		ax = axes[topic_idx]
		ax.barh(top_features, weights, height=0.7)
		ax.set_title(f'Topic {topic_idx +1}',
									fontdict={'fontsize': 30})
		ax.invert_yaxis()
		ax.tick_params(axis='both', which='major', labelsize=20)
		for i in 'top right left'.split():
			ax.spines[i].set_visible(False)
		fig.suptitle(title, fontsize=40)

	plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
	plt.show()

def create_topics_json(model, feature_names, n_top_words, outputfile):
	output = {}
	output['name'] = "Topics"
	output['children'] = []
	for topic_idx, topic in enumerate(model.components_):
		top_features_ind = topic.argsort()[:-n_top_words - 1:-1]
		top_features = [feature_names[i] for i in top_features_ind]
		weights = topic[top_features_ind]
		topic_obj = {}
		topic_obj["name"] = f"Topic {topic_idx}"
		topic_obj["children"] = []

		for i in range(len(top_features)):
			if outputfile == 'output_LDA.json':
				topic_obj["children"].append({"name": top_features[i], "value": weights[i]/1000})
			else:
				topic_obj["children"].append({"name": top_features[i], "value": weights[i]})
		output['children'].append(topic_obj)
	
	with open(outputfile, 'w') as f:
		json.dump(output, f)

def create_top_words_json(model, feature_names, n_top_words, outputfile):
	output = []
	for topic_idx, topic in enumerate(model.components_):
		top_features_ind = topic.argsort()[:-n_top_words - 1:-1]
		top_features = [feature_names[i] for i in top_features_ind]
		weights = topic[top_features_ind]

		for i in range(len(top_features)):
			if outputfile == 'subsample_top_words_lda.json':
				output.append({"name": top_features[i], "value": weights[i]/1000})
			else:
				output.append({"name": top_features[i], "value": weights[i]})

	output.sort(key=lambda x: x['value'], reverse=True)
	with open(outputfile, 'w') as f:
		json.dump(output, f)

def tokenize_and_stem(text):
	stop_words = set(stopwords.words('english'))
	tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
	filtered_tokens = []
	# filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
	for token in tokens:
		if re.search('[a-zA-Z]', token):
			filtered_tokens.append(token)
	stems = [porter_stemmer.stem(t) for t in filtered_tokens if t not in stop_words]
	return stems

# Load the 20 newsgroups dataset and vectorize it. We use a few heuristics
# to filter out useless terms early on: the posts are stripped of headers,
# footers and quoted replies, and common English words, words occurring in
# only one document or in at least 95% of the documents are removed.

print("Loading dataset...")
t0 = time()
text = []
with open ('../Task_1/subsample_reviews_low.txt', 'r') as f:
  text = f.readlines()
print("done in %0.3fs." % (time() - t0))

porter_stemmer = PorterStemmer()

# Use tf-idf features for NMF.
print("Extracting tf-idf features for NMF...")
tfidf_vectorizer = TfidfVectorizer(max_df=0.5, min_df=2,
                                   max_features=n_features,
																	 stop_words='english',
                                   use_idf=True)
t0 = time()
tfidf = tfidf_vectorizer.fit_transform(text)
print("done in %0.3fs." % (time() - t0))

# Use tf (raw term count) features for LDA.
print("Extracting tf features for LDA...")
tf_vectorizer = CountVectorizer(max_df=0.5, min_df=2,
                                max_features=n_features,
                                stop_words='english')
t0 = time()
tf = tf_vectorizer.fit_transform(text)
print("done in %0.3fs." % (time() - t0))


# Fit the NMF model
print("Fitting the NMF model (Frobenius norm) with tf-idf features "
      "and n_features=%d..."
      % (n_features))
t0 = time()
nmf = NMF(n_components=n_components, random_state=1,
          alpha=.1, l1_ratio=.5).fit(tfidf)
print("done in %0.3fs." % (time() - t0))


tfidf_feature_names = tfidf_vectorizer.get_feature_names()
create_topics_json(nmf, tfidf_feature_names, n_top_words, 'output_nmf_frobenius.json')
create_top_words_json(nmf, tfidf_feature_names, 3, 'subsample_top_words_nmf_frob.json')
#plot_top_words(nmf, tfidf_feature_names, n_top_words, 'Topics in NMF model (Frobenius norm)')

#Fit the NMF model
print('\n' * 2, "Fitting the NMF model (generalized Kullback-Leibler "
      "divergence) with tf-idf features and n_features=%d..."
      % (n_features))
t0 = time()
nmf = NMF(n_components=n_components, random_state=1,
          beta_loss='kullback-leibler', solver='mu', max_iter=1000, alpha=.1,
          l1_ratio=.5).fit(tfidf)
print("done in %0.3fs." % (time() - t0))

tfidf_feature_names = tfidf_vectorizer.get_feature_names()
create_topics_json(nmf, tfidf_feature_names, n_top_words, 'output_nmf_KLdiv.json')
create_top_words_json(nmf, tfidf_feature_names, 3, 'subsample_top_words_nmf_kl.json')
#plot_top_words(nmf, tfidf_feature_names, n_top_words, 'Topics in NMF model (generalized Kullback-Leibler divergence)')

print('\n' * 2, "Fitting LDA models with tf features "
      "and n_features=%d..."
      % (n_features))
lda = LatentDirichletAllocation(n_components=n_components, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
t0 = time()
lda.fit(tf)
print("done in %0.3fs." % (time() - t0))

tf_feature_names = tf_vectorizer.get_feature_names()
#plot_top_words(lda, tf_feature_names, n_top_words, 'Topics in LDA model')
create_topics_json(lda, tf_feature_names, n_top_words, 'output_LDA.json')
create_top_words_json(lda, tf_feature_names, 3, 'subsample_top_words_lda.json')