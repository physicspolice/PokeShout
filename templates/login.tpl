$def with (error)
<!DOCTYPE html>
<html>
	<head>
		<title>PokeShout Admin</title>
		<link rel="stylesheet" type="text/css" href="/static/main.css" />
		<meta charset="utf-8" />
	</head>
	<body>
		<section>
			<div>
				<p>$error</p>
			</div>
		</section>
		<footer>
			<form method="post" action="/login">
				<input type="password" name="password" />
				<input type="submit" value="Login" />
			</form>
		</footer>
	</body>
</html>
