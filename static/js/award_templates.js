$(document).ready(function(){

 if(($('.del_btn_formset').length) == 1){
    $('.del_btn_formset').hide()
  }
  else{
    $('.del_btn_formset').each(function(i, obj) {
        $(obj).show()
    });
  }
  $('#add_more').click(function() {
    $('.del_btn_formset').each(function(i, obj) {
        $(obj).show()
    });  
    cloneMore('div.add_template_questions:last', 'questions_set');
  });

  $(document).on('change', '.del_btn_formset', function(event) {
    if(($('.del_btn_formset').length) == 2){
      $('.del_btn_formset').each(function(i, obj) {
          $(obj).hide()
      });
    }
    else{
      $('.del_btn_formset').each(function(i, obj) {
          $(obj).show()
      });    
    }
    event.preventDefault();
    checkboxId = event.target.id;
    par_table = $('#'+checkboxId).closest('.formset_table');
    par_table.remove();
    re_calc_total()
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

  function re_calc_total() {
    var total = $('#id_form-TOTAL_FORMS').val();
    total--;
    $('#id_form-TOTAL_FORMS').val(total);
    $('#id_form-TOTAL_FORMS').attr('value', total);
  }
});