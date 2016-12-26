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
		var help = 'http://pgm.readthedocs.io/en/develop/extras/commandline.html';
		window.open(help);
	});
});
