$(document).ready(function() {
	$('#id_due_date').datepicker({
		format: "dd/mm/yy",
		weekStart: 1,
		language: "fr",
		orientation: "top right",
		calendarWeeks: true,
		autoclose: true,
		todayHighlight: true
	});

	// enable buttons
	$('.complete_task_button').each(function () {
		$(this).prop('disabled', false);
	});

	// force modal popups to refresh after being hidden
	$('body').on('hidden', '.modal', function () {
		$(this).removeData('modal');
	});

	$('input#id_description').on('input', function () {
		if ($(this).val() == "") {
			changeCssToCreateForm();
		}
	});

});

$(document).on("click", "div.task_div", function() {
	changeAddTaskFormToUpdateForm($(this));
});

function changeAddTaskFormToUpdateForm(task) {
	emptyAddTaskForm();
	changeCssToUpdateForm(task.find('span.task_id').text().trim());
	fillAddTaskFormWithTaskValues(task);
}

function changeCssToUpdateForm(task_id) {
	add_task_table = $('#add_task_table');
	add_task_table.css('border', '1px solid #4772DF');
	add_task_table.css('box-shadow', '0 0 10px 0 #4772DF');
	$('#add_task_button').attr('value', 'Update');
	$('#add_task_button').attr('id', 'update_task_button');
	$('#add_task_form').attr('action', '/update_task/' + task_id + '/');
}

function changeCssToCreateForm() {
	emptyAddTaskForm();
	add_task_table = $('#add_task_table');
	add_task_table.css('border', '1px solid #CE6B02');
	add_task_table.css('box-shadow', '0 0 10px 0 #CE6B02');
	$('#update_task_button').attr('value', 'Add');
	$('#update_task_button').attr('id', 'add_task_button');
	$('#add_task_form').attr('action', '/save_task/');
}

function emptyAddTaskForm() {
	$('#add_task_form input#id_description').val("");
	$('#add_task_form select#id_priority').prop('selectedIndex', 0);
	$('#add_task_form input#id_due_date').val("");
}

function fillAddTaskFormWithTaskValues(task) {
	task_description = task.children().find('span.task_description').text().trim();
	task_priority = task.children().find('span.task_priority_id').text();
	task_due_date = task.children().find('span.task_formatted_due_date').text().trim();
	add_task_form = $('#add_task_form');
	add_task_form.children().find('#id_description').val(task_description);
	add_task_form.children().find('#id_priority').val(task_priority);
	add_task_form.children().find('#id_due_date').val(task_due_date);
}

$(document).on("click", '#add_task_button', function (event) {
	action_url = $('#add_task_form').attr('action');
	$.ajax({
		type: "POST",
		url: action_url,
		data: $('#add_task_form').serialize(),
		dataType: "json",
		beforeSend: function() {
			$(event.target).prop('disabled', true);
		},
		complete: function() {
			$(event.target).prop('disabled', false);
		},
		success: function(data) {
			changeCssToCreateForm();
			if (data.place == 1) {
				$("#add_task_div").after(data.html);
				$("#no_task").hide();
				$(".task_div:first").css("background-color", "#CE6B02");
				$(".task_div:first").animate({backgroundColor: "#FFF"}, 1000);
			} else {
				$(".task_div:nth-child(" + data.place + ")").after(data.html);
				$(".task_div:nth-child(" + (data.place + 1) + ")").css("background-color", "#CE6B02");
				$(".task_div:nth-child(" + (data.place + 1) + ")").animate({backgroundColor: "#FFF"}, 1000);

			}
		},
		error: function() {
			return false;
		}
	});
	return false;
});

$(document).on("click", '#update_task_button', function (event) {
	action_url = $('#add_task_form').attr('action');
	$.ajax({
		type: "POST",
		url: action_url,
		data: $('#add_task_form').serialize(),
		dataType: "json",
		beforeSend: function() {
			$(event.target).prop('disabled', true);
		},
		complete: function() {
			$(event.target).prop('disabled', false);
		},
		success: function(data) {
			changeCssToCreateForm();
			$(".task_div:nth-child(" + data.old_place + ")").remove();
			if (data.place == 1) {
				$("#add_task_div").after(data.html);
				$("#no_task").hide();
				$(".task_div:first").css("background-color", "#88BAF8");
				$(".task_div:first").animate({backgroundColor: "#FFF"}, 1000);
			} else {
				$(".task_div:nth-child(" + data.place + ")").after(data.html);
				$(".task_div:nth-child(" + (data.place + 1) + ")").css("background-color", "#88BAF8");
				$(".task_div:nth-child(" + (data.place + 1) + ")").animate({backgroundColor: "#FFF"}, 1000);
			}
		},
		error: function() {
			return false;
		}
	});
	return false;
});

$(document).on("click", '.complete_task_button', function (event) {
	this_object = $(this);
	complete_task_href = this_object.parent().attr('href');
	$.ajax({
		url: complete_task_href,
		dataType: "json",
		beforeSend: function() {
			$(event.target).prop('disabled', true);
		},
		complete: function() {
			$(event.target).prop('disabled', false);
		},
		success: function(data) {
			this_object.closest('.task_div').remove();
		},
		error: function() {
			return false;
		}
	});
	return false;
});

$(document).on("click", '.uncomplete_task_button', function (event) {
	$(event.target).prop('disabled', true);
});

$(document).on("click", '#add_category_button', function (event) {
	action_url = $('#add_category_form').attr('action');
	$.ajax({
		type: "POST",
		url: action_url,
		data: $('#add_category_form').serialize(),
		dataType: "json",
		beforeSend: function() {
			$('#add_category_title .loading_img').show();
		},
		complete: function() {
			$('#add_category_title .loading_img').hide();
		},
		success: function(data) {
			$("#category_list .category:last").after(data.html);
			$("#add_category_popup .close").click();
		},
		error: function() {
			return false;
		}
	});
	return false;
});

$(document).on("click", '#update_category_button', function (event) {
	action_url = $('#update_category_form').attr('action');
	category_id = $('#update_category_form input#category_id').val();
	$.ajax({
		type: "POST",
		url: action_url,
		data: $('#update_category_form').serialize(),
		dataType: "json",
		beforeSend: function() {
			$('#modify_category_title .loading_img').show();
		},
		complete: function() {
			$('#modify_category_title .loading_img').hide();
		},
		success: function(data) {
			if (data.new_name) {
				$("#category_list .category_" + category_id + " a").html(data.new_name);
				$("#modify_category_popup .close").click();
			} else {
				$("form#update_category_form").replaceWith(data.html);
			}
		},
		error: function() {
			return false;
		}
	});
	return false;
});

$(document).on("click", '#delete_category_button', function (event) {
	action_url = $('#delete_category_form').attr('action');
	$.ajax({
		type: "POST",
		url: action_url,
		data: $('#delete_category_form').serialize(),
		dataType: "json",
		beforeSend: function() {
			$('#delete_category_title .loading_img').show();
		},
		complete: function() {
			$('#delete_category_title .loading_img').hide();
		},
		success: function(data) {
			$("li.category_" + data.category_id).remove();
			$("#delete_category_popup .close").click();
		},
		error: function() {
			return false;
		}
	});
	return false;
});


$(document).on("click", '#change_password_button', function (event) {
	action_url = $('#change_password_form').attr('action');
	$.ajax({
		type: "POST",
		url: '/change_password/',
		data: $('#change_password_form').serialize(),
		dataType: "html",
		beforeSend: function() {
			$('#change_password_title .loading_img').show();
		},
		complete: function() {
			$('#change_password_title .loading_img').hide();
		},
		success: function(html) {
			$("form#change_password_form").replaceWith(html);
		},
		error: function() {
			return false;
		}
	});
	return false;
});
