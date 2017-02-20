from web import application
from web.template import render

urls = ('/(.*)', 'admin')
app = application(urls, globals())
templates = render('templates')

class admin:
	def GET(self, action):
		settings = {}
		with open('RocketMap/config/config.ini') as file:
			for line in file:
				line = line.strip()
				if not line or line.startswith('#'):
					continue
				key, value = line.split(': ')
				settings[key] = value
		return templates.settings(settings)
	def POST(self, action):
		return 'foo'

if __name__ == '__main__':
	app.run()
