$(function() {
	
	$(document).on('click', '#delete', function(){
		$(this).closest('td').remove();
	});

});
$(document).ready(function(){
    $("#chosen-select").chosen({max_selected_options: 5})
    $("#chosen-select-adviser").chosen({max_selected_options: 5})
    $("#chosen-select-search-title").chosen({max_selected_options: 5})
    $("#chosen-select-search-student").chosen({max_selected_options: 5})

});
