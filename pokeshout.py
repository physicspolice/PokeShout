import settings
from csv import reader
from time import sleep
from twitter import Api
from sqlite3 import connect, Row, PARSE_DECLTYPES
from datetime import datetime, timedelta
from dateutil import tz

# Load pokemon CSVs.
csv = reader(open('pokedex.csv'))
pokedex = [x[0] for x in csv]

# Load pokemon CSVs.
csv = reader(open('worthy.csv'))
worthy = {}
for row in csv:
	worthy[row[1]] = int(row[0])

# Initialize Twitter API.
api = Api(
	consumer_key=settings.consumer_key,
	consumer_secret=settings.consumer_secret,
	access_token_key=settings.access_token,
	access_token_secret=settings.access_token_secret
)
user = api.VerifyCredentials()
print('Twitter API connected: %s' % user.screen_name)

# Connect to database.
db = connect('pogom.db', detect_types=PARSE_DECLTYPES)
db.row_factory = Row
cursor = db.cursor()

# Continuously poll for new Pokemon.
seen = {}
query = "SELECT * FROM pokemon WHERE last_modified > '%s' ORDER BY last_modified DESC"
last_modified = db.execute('SELECT MAX(last_modified) FROM pokemon').fetchone()[0]
while True:
	for pokemon in db.execute(query % last_modified):
		last_modified = pokemon['last_modified']
		if pokemon['encounter_id'] in seen:
			continue
		seen[pokemon['encounter_id']] = datetime.now()
		name = pokedex[pokemon['pokemon_id'] - 1]
		if pokemon['individual_attack']:
			percent = (pokemon['individual_attack'] + pokemon['individual_defense'] + pokemon['individual_stamina']) * 100.0 / 45.0
		if not name in worthy or percent < worthy[name]:
			print '%s (%.1f%%) is unworthy.' % (name, percent)
			continue
		until = datetime.strptime(pokemon['disappear_time'].split('.')[0], '%Y-%m-%d %H:%M:%S')
		until = until.replace(tzinfo=tz.tzutc()) # Timestamp from database is in UTC.
		until = until.astimezone(tz.tzlocal())   # Convert it to my local time zone.
		until = until.strftime('%-I:%M %p')
		url = 'https://www.google.com/maps?q=%s,%s' % (pokemon['latitude'], pokemon['longitude'])
		tweet = '%s (%.1f%%) %s %s' % (name, percent, until, url)
		print(tweet)
		api.PostUpdate(tweet)
	for encounter_id, when in seen.items():
		if when < datetime.now() - timedelta(minutes=15):
			del seen[encounter_id] # Clean out expired encounteres.
	sleep(1)
