import web # http://webpy.org/
from web.template import render
from warnings import filterwarnings
from subprocess import Popen, check_output
from time import sleep
from json import dumps
from sys import executable
from os import makedirs
from os.path import getsize
from signal import signal, SIGILL
from sqlite3 import connect, PARSE_DECLTYPES

from settings import admin_password

# Suppress warnings thrown by webpy.
filterwarnings("ignore", category=DeprecationWarning)

urls = ('/(.*)', 'AdminPage')

app = web.application(urls, globals())

# http://webpy.org/cookbook/session_with_reloader
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'auth': False, 'page': None})
    web.config._session = session
else:
    session = web.config._session

server = None
logfile = None

class AdminPage:

	config = 'RocketMap/config/config.ini'
	script = 'RocketMap/runserver.py'
	logpath = 'logs/map.txt'

	def GET(self, action):
		if not session.auth:
			session.page = action
			return render('templates').login('')
		settings = {}
		with open(self.config) as file:
			for line in file:
				line = line.strip()
				if not line or line.startswith('#'):
					continue
				key, value = line.split(': ')
				settings[key] = value
		return render('templates').settings(settings, int(self.running()), self.captchas())

	def POST(self, action):
		data = web.input()
		if action == 'login':
			if data.password == admin_password:
				session.auth = True
				raise web.seeother('/' + session.page)
			return render('templates').login('Password incorrect.')
		web.header('Content-Type', 'text/plain')
		if not session.auth:
			return self.response('Unauthorized.')
		if action == 'save':
			try:
				with open(self.config, 'w') as file:
					for name, value in data.iteritems():
						if value != '':
							file.write('%s: %s\n' % (name, value))
				return self.response('')
			except Exception as e:
				return self.response(e)
		if action == 'start':
			return self.response(self.start())
		if action == 'stop':
			return self.response(self.stop())
		if action == 'restart':
			return self.response(self.stop() or self.start())
		if action == 'poll':
			logs = ''
			end = 0
			if data.get('logs', False):
				start = int(data.get('offset', 0))
				fsize = getsize(self.logpath)
				if start > fsize:
					start = 0 # Logs may have been truncated, start over.
				try:
					if start > 0:
						with open(self.logpath) as file:
							file.seek(start)
							for line in file:
								end = file.tell()
								logs += line
								if len(logs) > 100240:
									break # Send up to 100 KB at a time.
					else:
						logs = check_output(['tail', '-n' '46', self.logpath])
						end = fsize
				except:
					pass # Oh well.
			return self.response(logs=logs, offset=end)
		return self.response('Unrecognized POST action: %s' % action)

	def start(self):
		global server, logfile
		if self.running():
			return 'The map server is already running.'
		try:
			makedirs('logs')
		except:
			pass # Already there.
		try:
			logfile = open(self.logpath, 'a')
		except:
			return 'Cannot open log file: %s' % self.logpath
		try:
			server = Popen([executable, self.script], stdout=logfile, stderr=logfile)
		except:
			return 'Failed to open map server subprocess!'
		return '' # No error.

	def stop(self):
		global server, logfile
		if not self.running():
			return 'The map server is not running.'
		server.terminate()
		logfile.close()
		tries = 1
		while self.running():
			if tries > 100:
				return 'The map server did not close promptly.'
			sleep(0.1)
			tries += 1
		return '' # No error.

	def response(self, error='', logs='', offset=0):
		response = {
			'error': str(error),
			'running': self.running(),
			'captchas': self.captchas(),
			'logs': logs,
			'offset': offset,
		}
		return dumps(response)

	def running(self):
		global server
		return bool(server and server.poll() is None)

	def captchas(self):
		try:
			# Create a new DB connection because it can only be used in this thread.
			db = connect('pogom.db', detect_types=PARSE_DECLTYPES)
			return db.execute('SELECT SUM(captcha) FROM workerstatus').fetchone()[0]
		except Exception as e:
			return str(e)

if __name__ == '__main__':
	def clean():
		if server:
			server.terminate()
			server.wait()
	signal(SIGILL, clean)
	app.run()
