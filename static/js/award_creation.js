$(document).ready(function(){
  if(($('.del_btn_formset').length) == 1){
    $('.del_btn_formset').hide()
  }
  else{
    $('.del_btn_formset').each(function(i, obj) {
        $(obj).show()
    });    
  }
  $('.add_more').click(function() {
    $('.del_btn_formset').each(function(i, obj) {
      $(obj).show()
    });  
    $(".datepicker").datepicker("destroy");
    cloneMore('div.add_nomination_period:last', 'nominationperiod_set');
  });


  $('body').on('focus',".datepicker", function(){
    $(this).datepicker();
  });

  $(document).on('change', '[type=checkbox]', function(event) {
    event.preventDefault();
    if(event.target.id.endsWith('DELETE') ){
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
      var checkboxId = event.target.id;
      par_table = $('#'+checkboxId).closest('.add_nomination_period');
      par_table.remove();
      re_calc_total()
    }
  }); 
    
  function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();  
    newElement.find(':input').each(function() {
      var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
      var id = 'id_' + name;
      $(this).attr({'name': name, 'id': id}).val('').prop('checked', false);
    });
   
    newElement.find('label').each(function() {
      if ($(this).attr('for')  !== undefined ) {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
      }
    });

    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    newElement.find('input.datepicker').removeData('datepicker').unbind().datepicker();
    $(selector).after(newElement);
  }

  function re_calc_total() {
    total = $('#id_nominationperiod_set-TOTAL_FORMS').val();
    total--;
    $('#id_nominationperiod_set-TOTAL_FORMS').val(total);
    $('#id_nominationperiod_set-TOTAL_FORMS').attr('value', total);
  }
});
