import pandas as pd
import json, csv
from sklearn.feature_extraction.text import TfidfVectorizer

def TfIdf(corpus, IDF:bool = True):
  vectorizer = TfidfVectorizer( max_df=0.5, min_df=2, 
                                stop_words='english', 
                                max_features=5000, 
                                use_idf=IDF)
  return vectorizer.fit_transform(corpus)

def extract_data():
  reviews_data = pd.read_json('../yelp_data/yelp_academic_dataset_review.json', lines=True)
  business_data = pd.read_json('../yelp_data/yelp_academic_dataset_business.json', lines=True)
  business_data['categories'] = business_data['categories'].values.tolist()

  italian = business_data.loc[business_data['categories'].astype(str).str.contains('Italian')]

  results = pd.merge(italian[['business_id', 'categories', 'name']],reviews_data[['stars', 'text', 'business_id']], on='business_id', how='inner')

  return results

def transform_data_to_textcorpus(data, file_name):
  data.to_csv(file_name, columns=['text'], header=False, index=False)
  return

def main():

  data = extract_data()
  dishes_dict = {}

  with open("../Task_3/results.txt") as f:
    for line in f:
      (key, val) = line.split('\t')
      key = key.lower()
      dishes_dict[key] = { "total_count": 0 }
  f.close()

  for index, row in data.iterrows():
    text = row['text']
    business = row['business_id']
    stars = row['stars']
    words = str(text).split(' ')
    for word in words:
      if word in dishes_dict:
        dishes_dict[word]['total_count'] = dishes_dict[word]['total_count'] + 1
        if business in dishes_dict[word]:
          dishes_dict[word][business]['count'] = dishes_dict[word][business]['count'] + 1
          dishes_dict[word][business]['stars'].append(stars)
          dishes_dict[word][business]['avg_rating'] = sum(dishes_dict[word][business]['stars'])/len(dishes_dict[word][business]['stars'])
        else:
          dishes_dict[word][business] = {}
          dishes_dict[word][business]['count'] = 1
          dishes_dict[word][business]['stars'] = [stars]
          dishes_dict[word][business]['avg_rating'] = sum(dishes_dict[word][business]['stars'])/len(dishes_dict[word][business]['stars'])

  final_dict = {}
  for key in dishes_dict:
    final_dict[key] = {}
    final_dict[key]['count'] = len(dishes_dict[key].keys()) - 1
    dishes_dict[key]['unique'] = len(dishes_dict[key].keys()) - 1
    total_avg_rating = 0
    for key2, value in dishes_dict[key].items():
      if key2 != "total_count" and key2 != 'unique':
        total_avg_rating = dishes_dict[key][key2]['avg_rating'] + total_avg_rating
    if dishes_dict[key]['unique'] > 0:
      dishes_dict[key]['total_avg_rating'] = total_avg_rating/dishes_dict[key]['unique']
      final_dict[key]['rating'] = total_avg_rating/dishes_dict[key]['unique']
    else:
      final_dict[key]['rating'] = 0

  with open("dishes.csv", "w") as out:
    w = csv.DictWriter(out, fieldnames=['dish_name', 'count', 'rating'])
    w.writeheader()
    for key in final_dict:
      w.writerow({'dish_name': key, 'count': final_dict[key]['count'], 'rating': final_dict[key]['rating']})
  out.close()
  return

if __name__ == "__main__":
  main()