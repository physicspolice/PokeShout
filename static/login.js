$(document).ready(function()
{
	var password = localStorage.getItem('password');
	if(password) $('input[name=password]').val(password);
	$('form').submit(function()
	{
		var password = $('input[name=password]').val();
		localStorage.setItem('password', password);
	});
});
