var interval = null;
var getLogs = false;
var offset = 0;

function update(running)
{
	$('input[name=start]').val(running ? 'Restart': 'Start');
	$('input[name=stop]').prop('disabled', !running);
	$('header a[data-type=server]').toggleClass('offline', !running);
}

function request(command, data={})
{
	$.post('/' + command, data, function(response)
	{
		if(response.error)
			alert(response.error);
		update(response.running);
		$('#captchas').text('Captchas (' + response.captchas + ')');
		if(offset == 0)
			$('#logs').text(''); // Remove loading message.
		if(response.logs)
		{
			var logs = $('#logs');
			var bottom = ($(window).scrollTop() + $(window).height() == $(document).height());
			logs.append(response.logs);
			if(bottom)
				window.scrollTo(0, $('body')[0].scrollHeight);
		}
		if(response.offset)
			offset = response.offset;
	}, 'json');
}

function polling()
{
	if(interval)
		clearInterval(interval);
	// 2 seconds when tailing logs.
	// 20 seconds on settings page.
	var duration = getLogs ? 2000 : 20000;
	interval = setInterval(function()
	{
		request('poll', {
			'logs': getLogs,
			'offset': offset,
		});
	}, duration);
}

$(document).ready(function()
{
	$('#logs').hide();
	update(parseInt($('body').attr('data-running')));
	$('#captchas').text('Captchas (' + $('body').attr('data-captchas') + ')');
	$('input[value=Add]').click(function()
	{
		var key = prompt('Enter the new setting name.').toLowerCase();
		var setting = $('<div />');
		setting.append($('<label />').text(key));
		setting.append($('<input />').attr('type', 'text').attr('name', key));
		$('section').append(setting);
		$('html, body').animate({ 'scrollTop': $(document).height() }, 1000);
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
		request('save', settings);
	});
	$('input[name=start], input[name=stop]').click(function()
	{
		var command = $(this).val().toLowerCase();
		request(command);
	});
	$('input[name=logs]').click(function()
	{
		getLogs = !getLogs;
		$(this).val(getLogs ? 'End' : 'Logs');
		$('#settings, #logs').toggle();
		polling();
	});
	polling();
});

// TODO add a "clear" button to log view.
// Separate footer buttons for log/setting views.
