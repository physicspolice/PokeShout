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
		<section>
			$for key, value in settings.iteritems():
				<div>
					<label>$key</label>
					<input type="text" name="$key" value="$value" />
				</div>
		</section>
		<footer>
			<input type="button" value="Add" />
			<input type="button" value="Help" />
			<input type="button" value="Save" />
			<input type="button" value="Start" name='start' />
			<input type="button" value="Stop"  name='stop' />
		</footer>
	</body>
</html>
