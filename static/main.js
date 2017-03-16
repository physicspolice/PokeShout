$(document).ready(function()
{
	$('input[value=Add]').click(function()
	{
		var key = prompt('Enter the new setting name.').toLowerCase();
		var setting = $('<div />');
		setting.append($('<label />').text(key));
		setting.append($('<input />').attr('type', 'text').attr('name', key));
		$('section').append(setting);
		$('html, body').animate({ 'scrollTop': $(document).height() }, 1000);
	});
	$('input[value=Help]').click(function()
	{
		var help = 'http://rocketmap.readthedocs.io/en/develop/extras/commandline.html';
		window.open(help);
	});
	$('input[value=Save]').click(function()
	{
		var settings = {};
		$('section div').each(function()
		{
			var name = $(this).find('label').text();
			var value = $(this).find('input').val();
			settings[name] = value;
		});
		$.post('/save', settings, function(response)
		{
			if(response != 'Success')
				alert(response);
		});
	});
	$('input[value=Restart]').click(function()
	{
		$.post('/restart', function(response)
		{
			if(response != 'Success')
				alert(response);
		});
	});
});
