import settings
from os import makedirs
from csv import reader
from sys import executable
from time import sleep
from twitter import Api
from sqlite3 import connect, Row, PARSE_DECLTYPES
from datetime import datetime, timedelta
from dateutil import tz
from subprocess import Popen

def sql_to_datetime(timestamp):
	d = datetime.strptime(timestamp.split('.')[0], '%Y-%m-%d %H:%M:%S')
	d = d.replace(tzinfo=tz.tzutc())  # Timestamp from database is in UTC.
	return d.astimezone(tz.tzlocal()) # Convert it to my local time zone.

def console(message):
	timestamp = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
	print('\r%s %s' % (timestamp, message))

# Load list of pokemon names.
csv = reader(open('pokedex.csv'))
pokedex = [x[0] for x in csv]

# Load list of quality pokemon.
try:
	makedirs('logs')
except:
	pass # Already there.
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
console('Twitter API connected: %s' % user.screen_name)

# Connect to database.
db = connect('pogom.db', detect_types=PARSE_DECLTYPES)
db.row_factory = Row
cursor = db.cursor()

# Start up the admin page.
log = open('logs/admin.txt', 'a')
admin = Popen([executable, 'admin.py'], stdout=log, stderr=log)

# Continuously poll for new pokemon.
captcha = False
seen = {}
query = "SELECT * FROM pokemon WHERE last_modified > '%s' ORDER BY last_modified DESC"
last_modified = db.execute('SELECT MAX(last_modified) FROM pokemon').fetchone()[0]
console('Last Pokemon seen: %s' % sql_to_datetime(last_modified).strftime('%Y-%m-%d %I:%M:%S %p'))
try:
	while True:
		if db.execute('SELECT 1.0 * SUM(captcha) / COUNT(*) FROM workerstatus').fetchone()[0] > 0.75:
			if not captcha:
				message = 'Running low on captchas...'
				console(message)
				for handle in settings.captcha_admins:
					try:
						api.PostDirectMessage(text=message, screen_name=handle)
					except:
						console('Failed to send direct message: %s' % handle)
				captcha = True
		elif captcha:
			console('Got more captchas!')
			captcha = False
		for pokemon in db.execute(query % last_modified):
			last_modified = pokemon['last_modified']
			if pokemon['encounter_id'] in seen:
				continue
			seen[pokemon['encounter_id']] = datetime.now()
			name = pokedex[pokemon['pokemon_id'] - 1]
			percent = (100.0 / 45.0) * (
				pokemon['individual_attack'] +
				pokemon['individual_defense'] +
				pokemon['individual_stamina']
			)
			if not name in worthy or percent < worthy[name]:
				console('%s (%.1f%%) is unworthy.' % (name, percent))
				continue
			until = sql_to_datetime(pokemon['disappear_time']).strftime('%-I:%M %p')
			url = 'https://www.google.com/maps?q=%s,%s' % (pokemon['latitude'], pokemon['longitude'])
			tweet = '%s (%.1f%%) %s %s' % (name, percent, until, url)
			console(tweet)
			api.PostUpdate(tweet)
		for encounter_id, when in seen.items():
			if when < datetime.now() - timedelta(minutes=60):
				del seen[encounter_id] # Clean out expired encounteres.
		sleep(1)
except KeyboardInterrupt:
	console('Shutting down...')
	log.close()
	admin.terminate()
	admin.wait()
