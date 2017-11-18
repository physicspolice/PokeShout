from __future__ import print_function

import settings

from re import compile
from sys import stdout
from time import sleep
from datetime import datetime
from traceback import format_exc
from twitter import Api, error

regex = compile(': (.+) ([\d\.]+)\% .+ \(L(\d+)\)')

# http://python-twitter.readthedocs.io/en/latest/twitter.html
api = Api(
	consumer_key=settings.consumer_key,
	consumer_secret=settings.consumer_secret,
	access_token_key=settings.access_token,
	access_token_secret=settings.access_token_secret
)
print('Twitter API connected: %s' % api.VerifyCredentials().screen_name)

count = 0
worthy = 0
since_id = None
try:
	while(True):
		try:
			tweets = api.GetUserTimeline(screen_name=settings.target, since_id=since_id)
			time = datetime.now().replace(microsecond=0)
			for tweet in tweets:
				since_id = max(since_id, tweet.id)
				match = regex.search(tweet.text)
				if not match:
					print('Failed to parse tweet: %s' % tweet.text)
					continue
				count += 1
				(name, percent, level) = match.groups()
				if round(float(percent)) != 100:
					continue # Hundred percenters only!
				if name not in settings.wishlist:
					continue # Only retweet from the wish list.
				if int(level) < settings.wishlist[name]:
					continue # Not high enough level to be worthy.
				try:
					api.PostUpdate(tweet.text)
					print('  %s %s' % (time, tweet.text))
					worthy += 1
				except error.TwitterError as e:
					try:
						message = e.message[0]['message']
					except Exception:
						message = str(e)
					if message != 'Status is a duplicate.':
						print('Twitter error: %s' % message)
			print('  %s Retweeted %d of %d tweets\r' % (time, worthy, count), end='')
			stdout.flush()
		except error.TwitterError:
			print('\nTwitter error: ' + e.message)
		except Exception:
			print("\n" + format_exc())
		sleep(10)
except KeyboardInterrupt:
	print('\nGoodbye.')
