import enum
from numpy import float32
import pandas as pd
import numpy as np
import json, copy
from itertools import chain
from sklearn.feature_extraction.text import TfidfVectorizer
from pandas.io.formats.format import CategoricalFormatter
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans, DBSCAN
import matplotlib.pyplot as plt

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


if __name__ == "__main__":
  main()