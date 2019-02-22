$(document).ready(function(){
  $('#add_more').click(function() {
    cloneMore('div:last', 'form');
  });

  $(document).on('change', '.del_btn_formset', function(event) {
    event.preventDefault();
    checkboxId = event.target.id;
    par_table = $('#'+checkboxId).closest('.formset_table');
    par_table.remove();
    // need ajax func for edit questions template form
    
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
});