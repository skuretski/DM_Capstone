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
      dishes_dict[key] = { "total_count": 0, "restaurants": {} }
  f.close()

  for index, row in data.iterrows():
    text = row['text']
    business = row['business_id']
    stars = row['stars']
    words = str(text).split(' ')
    for word in words:
      if word in dishes_dict:
        dishes_dict[word]['total_count'] = dishes_dict[word]['total_count'] + 1
        if business in dishes_dict[word]['restaurants']:
          dishes_dict[word]['restaurants'][business]['count'] = dishes_dict[word]['restaurants'][business]['count'] + 1
          dishes_dict[word]['restaurants'][business]['stars'].append(stars)
          dishes_dict[word]['restaurants'][business]['avg_rating'] = sum(dishes_dict[word]['restaurants'][business]['stars'])/len(dishes_dict[word]['restaurants'][business]['stars'])
        else:
          dishes_dict[word]['restaurants'][business] = {}
          dishes_dict[word]['restaurants'][business]['count'] = 1
          dishes_dict[word]['restaurants'][business]['stars'] = [stars]
          dishes_dict[word]['restaurants'][business]['avg_rating'] = sum(dishes_dict[word]['restaurants'][business]['stars'])/len(dishes_dict[word]['restaurants'][business]['stars'])

  final_dish_dict = {}
  final_rest_dict = {}

  for key in dishes_dict:
    final_dish_dict[key] = {}
    final_dish_dict[key]['count'] = len(dishes_dict[key].keys()) - 1
    dishes_dict[key]['unique'] = len(dishes_dict[key].keys()) - 1
    total_avg_rating = 0
    for key2, value in dishes_dict[key]['restaurants'].items():
      total_avg_rating = value['avg_rating'] + total_avg_rating
    if dishes_dict[key]['unique'] > 0:
      dishes_dict[key]['total_avg_rating'] = total_avg_rating/dishes_dict[key]['unique']
      final_dish_dict[key]['rating'] = total_avg_rating/dishes_dict[key]['unique']
    else:
      final_dish_dict[key]['rating'] = 0
      dishes_dict[key]['total_avg_rating'] = 0

  # with open("dishes.csv", "w") as out:
  #   w = csv.DictWriter(out, fieldnames=['dish_name', 'count', 'rating'])
  #   w.writeheader()
  #   for key in final_dish_dict:
  #     w.writerow({'dish_name': key, 'count': final_dish_dict[key]['count'], 'rating': final_dish_dict[key]['rating']})
  # out.close()


  best_dishes = sorted(dishes_dict.items(), reverse=True, key=lambda x: x[1]['total_avg_rating'])
  best_dishes = best_dishes[1:51] # top 50, excluding 'menu' at top

  restaraunts_with_best_dishes = {}
  for best_dish_v in best_dishes.values():
    for rest_key, rest_value in best_dish_v['restaurants'].items():
      restaraunts_with_best_dishes[rest_key] = restaraunts_with_best_dishes.get(rest_key,0)+rest_value['avg_rating']

  print(restaraunts_with_best_dishes)
  return

if __name__ == "__main__":
  main()