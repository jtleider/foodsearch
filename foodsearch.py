import googlemaps
import csv
from collections import defaultdict

def search(output, location, search_term, api_key):
	cli = googlemaps.Client(key=api_key)
	csv_writer = csv.writer(output)
	csv_writer.writerow(location)
	csv_writer.writerow(['Search Term', 'Store Name', 'Address', 'Phone Number'])
	next_page_token = None
	while True:
		print("Searching...")
		nearby = cli.places_nearby(location=location,
			keyword=search_term,
			rank_by='distance',
			page_token = next_page_token)
		try:
			assert nearby['status'] == 'OK'
		except AssertionError:
			print('Warning, status not OK: {0}'.format(nearby['status']))
			print('Continuing anyway...')
		placeids = [r['place_id'] for r in nearby['results']]
		for placeid in placeids:
			details = cli.place(place_id=placeid)
			try:
				assert details['status'] == 'OK'
			except AssertionError:
				print('Warning, status not OK: {0}'.format(details['status']))
				print('Continuing anyway...')
			details = defaultdict(str, details['result'])
			csv_writer.writerow((search_term, details['name'], details['formatted_address'], details['formatted_phone_number']))
		if 'next_page_token' in nearby.keys():
			next_page_token = nearby['next_page_token']
		else:
			break


f = open('temp.csv', 'w')
for search_term in ['supermarket', 'convenience store', 'dollar store']:
	search(f, (40.748920, -73.968912), search_term, open('apikey').read())
f.close()

