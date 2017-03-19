var logTimer = null;
function logPoll()
{
	$.post('/logs', function(response)
	{
		$('section').text(response);
	});
}

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
	}, 'json');
}

$(document).ready(function()
{
	update(parseInt($('body').attr('data-running')));
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
		if(logTimer)
		{
			clearTimeout(logTimer);
			logTimer = null;
			$(this).val('Logs');
			$('#logs').hide();
			$('#settings').show();
		}
		else
		{
			logTimer = setInterval(logPoll, 500);
			$(this).val('End');
			$('#logs').show();
			$('#settings').hide();
		}
	});
});
