from numpy import float32
import pandas as pd
import json, copy
from itertools import chain

from pandas.io.formats.format import CategoricalFormatter

def create_restaruant_geojson(rest):
  geojson_obj = {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "Point",
          "coordinates": [d["longitude"], d["latitude"]]
        },
        "properties": d
      } for d in rest
    ]
  }

  output = open('./data/geojson.json', 'w')
  json.dump(geojson_obj, output)
  output.close()

def get_top_restaurants_by_state(restaurants):
  states = restaurants['state'].unique()
  rest_dict = {s: {} for s in states}
  categories = set(chain.from_iterable(restaurants['categories']))
  categories.remove('Gyms')
  categories.remove('Jazz & Blues')
  categories.remove('Internet Cafes')
  categories.remove('Do-It-Yourself Food')
  categories.remove('Hookah Bars')
  categories.remove('Event Planning & Services')
  categories.remove('Drugstores')
  categories.remove('Dive Bars')
  categories.remove('Arts & Entertainment')
  categories.remove('Food Delivery Services')
  categories.remove('Home Decor')
  categories.remove('Belgian')
  categories.remove('Butcher')
  categories.remove('Cambodian')
  categories.remove('Cheese Shops')
  categories.remove('Distilleries')
  categories.remove('Seafood Markets')
  categories.remove('Piano Bars')
  categories.remove('Leisure Centers')
  categories.remove('Horseback Riding')
  categories.remove('Performing Arts')
  categories.remove('Restaurants')
  categories.remove('Tours')
  categories.remove('Home & Garden')
  categories.remove('Gas & Service Stations')
  categories.remove('Health & Medical')
  categories.remove('Arcades')
  categories.remove('Casinos')
  categories.remove('Public Services & Government')
  categories.remove('Education')
  categories.remove('Hotels')
  categories.remove('Hotels & Travel')
  categories.remove('Specialty Food')
  categories.remove('Car Wash')
  categories.remove('Cultural Center')
  categories.remove('Arts & Crafts')
  categories.remove('Landmarks & Historical Buildings')
  categories.remove('Transportation')
  categories.remove('Medical Spas')
  categories.remove('Music Venues')
  categories.remove('Venues & Event Spaces')
  categories.remove('Swimming Pools')
  categories.remove('Automotive')
  categories.remove('Auto Repair')
  categories.remove('Ethnic Food')
  categories.remove('Taxis')
  categories.remove('Hospitals')
  categories.remove('Fitness & Instruction')
  categories.remove('Specialty Schools')
  categories.remove('Health Markets')
  categories.remove('Shopping')
  categories.remove('Shopping Centers')
  categories.remove('Personal Shopping')
  categories.remove('Amusement Parks')
  categories.remove('Gift Shops')
  categories.remove('Flowers & Gifts')
  categories.remove('Bowling')
  categories.remove('Convenience Stores')
  categories.remove('Grocery')
  categories.remove('Beauty & Spas')
  categories.remove('Cafeteria')
  categories.remove('Active Life')
  categories.remove('Appliances')
  categories.remove('Dry Cleaning & Laundry')
  categories.remove('Local Services')
  categories.remove('Party & Event Planning')
  categories.remove('Kitchen & Bath')
  categories.remove('Dance Clubs')
  categories.remove('Day Spas')
  categories.remove('Cooking Schools')
  categories.remove('Karaoke')
  categories.remove('Cinema')
  categories.remove('Colleges & Universities')
  categories.remove('Outlet Stores')
  categories.remove('Local Flavor')
  categories.remove('Social Clubs')
  categories.remove('Herbs & Spices')
  categories.remove('Airports')
  categories.remove('Fruits & Veggies')
  categories.remove('Pool Halls')
  categories.remove('Street Vendors')
  categories.remove('Nightlife')
  categories.remove('Personal Chefs')
  categories.remove('Caterers')
  categories.remove('Kids Activities')
  categories.remove('Festivals')
  categories.remove('Golf')
  categories.remove('Food')
  print(len(categories))
  categories_dict = {}
  for key in categories:
    categories_dict[key] = []
  for key in rest_dict:
    rest_dict[key] = copy.deepcopy(categories_dict)

  restaurant_results = []

  for index, row in restaurants.iterrows():
    state = row['state'] 
    categories = row['categories']
    if (state == 'WI' or state == 'NV' or state == 'GA' or state == 'AZ'):
      for c in categories:
        if c in categories_dict:
          rest_dict[state][c].append(row.to_dict())
          restaurant_results.append(row.to_dict())

  with open('./data/restaurant_by_state.json', 'w') as outfile:
    json.dump(rest_dict, outfile)

  return restaurant_results

def get_reviews_for_top_rest(dict):
  reviews = []
  reviews_by_rest = {}
  # for line in open('../../yelp_data/yelp_academic_dataset_review.json', 'r'):
  #   reviews.append(json.loads(line))

  # for r in reviews:
  #   if r['business_id'] not in 
  
  # return

def extract_data():
  reviews_data = pd.read_json('../../yelp_data/yelp_academic_dataset_review.json', lines=True)
  business_data = pd.read_json('../../yelp_data/yelp_academic_dataset_business.json',lines=True)
  business_data = business_data[['name', 'stars', 'categories', 'business_id', 'full_address', 'latitude', 'longitude', 'state']]
  business_data['categories'] = business_data['categories'].values.tolist()
  business_data['stars'] = business_data['stars'].astype(float32)
  business_data['state'] = business_data['state'].astype(str)

  restaurants = business_data.loc[(business_data['categories'].astype(str).str.contains('Restaurants')) & (business_data['stars'] > 3.0)]
  restaurants = restaurants.loc[restaurants['state'].str.contains('WI') | restaurants['state'].str.contains('NV') | restaurants['state'].str.contains('AZ') | restaurants['state'].str.contains('GA')]
  
  restaurant_reviews = pd.merge(restaurants[['state', 'name', 'categories', 'business_id']], reviews_data[['stars', 'text', 'business_id']], on='business_id', how='inner')

  return restaurant_reviews, restaurants


def main():
  reviews, restaurants = extract_data()
  new_restaurants = get_top_restaurants_by_state(restaurants)
  create_restaruant_geojson(new_restaurants)

  


if __name__ == "__main__":
  main()