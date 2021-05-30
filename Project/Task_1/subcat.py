import json

low_rest_IDs = set()
high_rest_IDs = set()

with open('../scripts/restaurantIds2ratings.txt', 'r') as f:
  for line in f.readlines():
    id, rating = line.split(' ')
    rating = float(rating)
    if rating < 2.0:
      low_rest_IDs.add(id)
    elif rating > 4.5:
      high_rest_IDs.add(id)

low_output = open('subsample_reviews_low.txt', 'wb')
high_output = open('subsample_reviews_high.txt', 'wb')

with open ('../yelp_data/yelp_academic_dataset_review.json', 'r') as f:
  for line in f.readlines():
    review_json = json.loads(line)
    if review_json['business_id'] in low_rest_IDs:
      low_output.write(f'\n{review_json["text"]}'.encode('ascii','ignore') )
    elif review_json['business_id'] in high_rest_IDs:
      high_output.write(f'\n{review_json["text"]}'.encode('ascii','ignore') )

low_output.close()
high_output.close()