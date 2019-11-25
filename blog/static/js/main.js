$(function() {
const category_content = $('.dropdown-item')
const title_input = $('#user-input')
const posts_div = $('#replaceable-content')
// const search_icon = $('#search-icon')
const endpoint = ''
const delay_by_in_ms = 0
let scheduled_function = false


let ajax_call = function (endpoint, request_parameters) {
	$.getJSON(endpoint, request_parameters)
		.done(response => {
			posts_div.fadeTo(450, 0).promise().then(() => {
				posts_div.html(response['html_from_view'])
				posts_div.fadeTo(450, 1)
				// search_icon.removeClass('blink')
			})
		})
}


title_input.on('keyup', function () {
	var id = $(this).val();
	const request_parameters = {
		id: id
	}

	// search_icon.addClass('blink')

	if (scheduled_function) {
		clearTimeout(scheduled_function)
	}

	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})


category_content.on('click', function () {
	var pk = $(this).attr("id");
	const request_parameters = {
		pk: pk
	}

	if (scheduled_function) {
		clearTimeout(scheduled_function)
	}

	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})
})