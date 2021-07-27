import pandas as pd
import json
import geojson

def main():
  businesses = []
  for line in open('../../yelp_data/yelp_academic_dataset_business.json', 'r'):
    businesses.append(json.loads(line))

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
      } for d in businesses if "Restaurants" in d["categories"] 
    ]
  }

  output = open('./data/geojson.json', 'w')
  json.dump(geojson_obj, output)


if __name__ == "__main__":
  main()