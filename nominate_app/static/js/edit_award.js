$('#add_more').click(function() {
    cloneMore('div.table:last', 'nominationperiod_set');
});

$(document).on('change', '[type=checkbox]', function(event) {
	event.preventDefault();
	var checkboxId = event.target.id;
	var vall = Number($('#'+checkboxId).next('input').next('input')[0].value);
	par_table = $('#'+checkboxId).closest('.no_error');
	par_table.hide();
	$.ajax({

		url:'/delete/' + vall + '/',
		type:'POST',
		data:{
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
		},
		dataType: 'json',
		success:function(){

		}
	});
	
}); 
	function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
    });
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
}
	