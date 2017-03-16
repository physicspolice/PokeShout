$def with (settings, running)
<!DOCTYPE html>
<html>
	<head>
		<title>PokeShout Admin</title>
		<link rel="stylesheet" type="text/css" href="/static/main.css" />
		<script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
		<script src="/static/main.js"></script>
		<meta charset="utf-8" />
	</head>
	<body data-running="$running">
		<header>
			<a href="$settings['manual-captcha-domain']/">Map</a>
			<a href="$settings['manual-captcha-domain']/stats">Stats</a>
			<a href="$settings['manual-captcha-domain']/bookmarklet">Captchas</a>
			<a href="https://twitter.com/PokeShout">Twitter</a>
			<a href="http://rocketmap.readthedocs.io/en/develop/extras/commandline.html">Docs</a>
		</header>
		<section>
			$for key, value in settings.iteritems():
				<div>
					<label>$key</label>
					<input type="text" name="$key" value="$value" />
				</div>
		</section>
		<footer>
			<input type="button" value="Add" />
			<input type="button" value="Save" />
			<input type="button" value="Start" name='start' />
			<input type="button" value="Stop"  name='stop' />
			<input type="button" value="Logs" />
		</footer>
	</body>
</html>
