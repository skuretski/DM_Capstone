import pandas as pd
import json, csv, nltk, re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

def tokenize_and_stem(text):
  nltk.download('stopwords')
  porter_stemmer = PorterStemmer()
  stop_words = set(stopwords.words('english'))
  tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
  filtered_tokens = []
	# filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
  for token in tokens:
    if re.search('[a-zA-Z]', token):
      filtered_tokens.append(token)
  stems = [porter_stemmer.stem(t) for t in filtered_tokens if t not in stop_words]
  return stems

def extract_data():
  reviews_data = pd.read_json('../yelp_data/yelp_academic_dataset_review.json', lines=True)
  business_data = pd.read_json('../yelp_data/yelp_academic_dataset_business.json', lines=True)
  business_data['categories'] = business_data['categories'].values.tolist()

  italian = business_data.loc[business_data['categories'].astype(str).str.contains('Italian')]
  business_data['categories'] = business_data['categories'].astype(str)
  restaurants = italian.loc[italian['state'].str.contains('WI') | italian['state'].str.contains('NV') | italian['state'].str.contains('AZ') | italian['state'].str.contains('GA')]
  results = pd.merge(restaurants[['business_id', 'categories', 'name', 'latitude', 'longitude', 'state', 'full_address']],reviews_data[['stars', 'text', 'business_id']], on='business_id', how='inner')

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
    #text = tokenize_and_stem(text)
    business = row['business_id']
    name = row['name']
    stars = row['stars']
    state = row['state']
    latitude = row['latitude']
    longitude = row['longitude']
    categories = row['categories']
    address = row['full_address']
    words = str(text).split(' ')
    for word in words:
      if word in dishes_dict:
        dishes_dict[word]['total_count'] = dishes_dict[word]['total_count'] + 1
        if business in dishes_dict[word]['restaurants']:
          dishes_dict[word]['restaurants'][business]['name'] = name
          dishes_dict[word]['restaurants'][business]['state'] = state
          dishes_dict[word]['restaurants'][business]['latitude'] = latitude
          dishes_dict[word]['restaurants'][business]['longitude'] = longitude
          dishes_dict[word]['restaurants'][business]['categories'] = categories
          dishes_dict[word]['restaurants'][business]['latitude'] = latitude
          dishes_dict[word]['restaurants'][business]['longitude'] = longitude
          dishes_dict[word]['restaurants'][business]['address'] = address
          dishes_dict[word]['restaurants'][business]['count'] = dishes_dict[word]['restaurants'][business]['count'] + 1
          dishes_dict[word]['restaurants'][business]['stars'].append(stars)
          dishes_dict[word]['restaurants'][business]['avg_rating'] = sum(dishes_dict[word]['restaurants'][business]['stars'])/len(dishes_dict[word]['restaurants'][business]['stars'])
        else:
          dishes_dict[word]['restaurants'][business] = {}
          dishes_dict[word]['restaurants'][business]['count'] = 1
          dishes_dict[word]['restaurants'][business]['name'] = name
          dishes_dict[word]['restaurants'][business]['state'] = state
          dishes_dict[word]['restaurants'][business]['latitude'] = latitude
          dishes_dict[word]['restaurants'][business]['longitude'] = longitude
          dishes_dict[word]['restaurants'][business]['categories'] = categories
          dishes_dict[word]['restaurants'][business]['address'] = address
          dishes_dict[word]['restaurants'][business]['stars'] = [stars]
          dishes_dict[word]['restaurants'][business]['avg_rating'] = sum(dishes_dict[word]['restaurants'][business]['stars'])/len(dishes_dict[word]['restaurants'][business]['stars'])

  final_dish_dict = {}

  for key in dishes_dict:
    final_dish_dict[key] = {}
    final_dish_dict[key]['count'] = len(dishes_dict[key]['restaurants'].keys())
    dishes_dict[key]['unique'] = len(dishes_dict[key]['restaurants'].keys())
    total_avg_rating = 0
    for key2, value in dishes_dict[key]['restaurants'].items():
      total_avg_rating = value['avg_rating'] + total_avg_rating
    if dishes_dict[key]['unique'] > 0:
      dishes_dict[key]['total_avg_rating'] = total_avg_rating/dishes_dict[key]['unique']
      final_dish_dict[key]['rating'] = total_avg_rating/dishes_dict[key]['unique']
    else:
      final_dish_dict[key]['rating'] = 0
      dishes_dict[key]['total_avg_rating'] = 0

  with open("./new_data/dishes.json", "w") as outfile: 
    json.dump(dishes_dict, outfile)

  with open("./new_data/dishes.csv", "w") as out:
    w = csv.DictWriter(out, fieldnames=['dish_name', 'count', 'rating'])
    w.writeheader()
    for key in final_dish_dict:
      w.writerow({'dish_name': key, 'count': final_dish_dict[key]['count'], 'rating': final_dish_dict[key]['rating']})
  out.close()


  best_dishes = sorted(dishes_dict.items(), reverse=True, key=lambda x: x[1]['total_avg_rating'])
  best_dishes = best_dishes[1:201] # top 50, excluding 'menu' at top

  restaraunts_with_best_dishes = {}
  for best_dish_v in best_dishes:
    for rest_key, rest_value in best_dish_v[1]['restaurants'].items():
      curr = restaraunts_with_best_dishes.get(rest_value['name'],{
        "total": 0,
        "count": 0
      })
      total = curr['total'] + rest_value['avg_rating']
      count = curr['count']+1

      restaraunts_with_best_dishes[rest_value['name']] = {
        "total": total,
        "count": count,
        "state": rest_value['state'],
        "longitude": rest_value["longitude"],
        "latitude": rest_value["latitude"],
        "categories": rest_value["categories"],
        "address": rest_value["address"]
      }

  for r in restaraunts_with_best_dishes.values():
    r['avg'] = r['total']/r['count']
  filtered_dict = dict(filter(lambda elem: elem[1]['count'] > 2 and elem[1]['avg'] >= 3.5, restaraunts_with_best_dishes.items()))

  sorted_restaurants = sorted(filtered_dict.items(), reverse=True, key=lambda x: x[1]['avg'])

  with open("./new_data/restaurants.csv", "w") as out:
    w = csv.DictWriter(out, fieldnames=['name', 'state', 'latitude', 'longitude', 'rating', 'count', 'address', 'categories'])
    w.writeheader()
    for key, value in sorted_restaurants:
      w.writerow({'name': key, 'state': value['state'], 'latitude': value['latitude'], 'longitude': value['longitude'], 'rating': value['avg'], 'count': value['count'], 'address': value['address'], 'categories': value['categories'] })
  out.close()

  with open("./new_data/restaurants.json", "w") as outfile: 
    json.dump(sorted_restaurants, outfile)

  return

if __name__ == "__main__":
  main()