# Adapted from https://github.com/scottstamp/pgoapi/blob/master/scripts/accept-tos.py

from sys import argv

from pgoapi import PGoApi
from pgoapi.utilities import f2i
from pgoapi import utilities as util
from pgoapi.exceptions import AuthException
import pprint
import time
import threading

def accept_tos(login_type, username, password):
	api = PGoApi()
	api.set_position(37.3503221, -121.991064, 0.0)
	api.login(login_type, username, password)
	time.sleep(2)
	req = api.create_request()
	req.mark_tutorial_complete(tutorials_completed = 0, send_marketing_emails = False, send_push_notifications = False)
	response = req.call()
	print('Accepted Terms of Service for %s' % username)

with open(str('accounts.csv')) as f:
	credentials = [x.strip().split(',') for x in f.readlines()]

for login_type, username, password in credentials:
	try:
		accept_tos(login_type, username, password)
	except ServerSideRequestThrottlingException as e:
		print('Server side throttling, Waiting 10 seconds.')
		time.sleep(10)
		accept_tos(username, password)
	except NotLoggedInException as e1:
		print('Could not login, Waiting for 10 seconds')
		time.sleep(10)
