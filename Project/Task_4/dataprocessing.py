import pandas as pd


def main():
  reviews_data = pd.read_json('../yelp_data/yelp_academic_dataset_review.json', lines=True)
  business_data = pd.read_json('../yelp_data/yelp_academic_dataset_business.json', lines=True)
  business_data['categories'] = business_data['categories'].values.tolist()

  italian = business_data.loc[business_data['categories'].astype(str).str.contains('Italian')]

  results = pd.merge(italian[['business_id', 'categories', 'name']],reviews_data[['stars', 'text', 'business_id']], on='business_id', how='inner')
  print(results.head(5))

  return

if __name__ == "__main__":
  main()