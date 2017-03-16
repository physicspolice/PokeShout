import web # http://webpy.org/
from web.template import render

urls = ('/(.*)', 'admin')
app = web.application(urls, globals())
templates = render('templates')
config = 'RocketMap/config/config.ini'

class admin:

	def GET(self, action):
		settings = {}
		with open(config) as file:
			for line in file:
				line = line.strip()
				if not line or line.startswith('#'):
					continue
				key, value = line.split(': ')
				settings[key] = value
		return templates.settings(settings)

	def POST(self, action):
		web.header('Content-Type', 'text/plain')
		data = web.input()

		if action == 'save':
			try:
				with open(config, 'w') as file:
					for name, value in data.iteritems():
						if value != '':
							file.write('%s: %s\n' % (name, value))
				return 'Success'
			except Exception as e:
				return str(e)

		if action == 'restart':
			# get PID from (?)
			# kill process by PID
			# start new process
			# do (?) with new process PID
			return 'TODO'

		return 'Unrecognized POST action: %s' % action

if __name__ == '__main__':
	app.run()
