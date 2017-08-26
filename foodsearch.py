# IPython log file

import googlemaps
import csv

cli = googlemaps.Client(key=open('apikey').read())
nearby = cli.places_nearby(location=(40.748920, -73.968912),
	keyword='supermarket',
	rank_by='distance')
placeids = [r['place_id'] for r in nearby['results']]
f = open('temp.csv', 'w')
csv_writer = csv.writer(f)
for placeid in placeids:
	details = cli.place(place_id=placeid)
	details = details['result']
	csv_writer.writerow((details['name'], details['formatted_address'], details['formatted_phone_number']))
f.close()

