$(document).ready(function(){
  // $("#needs-validation").submit(function(e){
  //   count = $('.datepicker').length / 2
  //   for(var i=0; i< count; i++){
  //     start_day = $("input[name=nominationperiod_set-"+ i +"-start_day]").datepicker('getDate')
  //     end_day = $("input[name=nominationperiod_set-"+ i +"-end_day]").datepicker('getDate')
  //     if(start_day > end_day){
  //       e.stopPropagation()
  //       $("input[name=nominationperiod_set-"+ i +"-start_day]").focus()
  //       $("input[name=nominationperiod_set-"+ i +"-end_day]").focus()
  //       e.preventDefault()
  //       break;
  //     }
  //   }
  // });
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
    $('.datepicker').attr('autocomplete',"off");
    $(this).datepicker({
      startDate: "today",
      maxViewMode: 1,
      orientation: "bottom",
      autoclose: true
    });
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
    newElement.find('input.datepicker').removeData('datepicker').unbind().datepicker(
      {
        startDate: "today",
        maxViewMode: 1,
        orientation: "bottom",
        autoclose: true
    }
    );
    $(selector).after(newElement);
  }

  function re_calc_total() {
    total = $('#id_nominationperiod_set-TOTAL_FORMS').val();
    total--;
    $('#id_nominationperiod_set-TOTAL_FORMS').val(total);
    $('#id_nominationperiod_set-TOTAL_FORMS').attr('value', total);
  }


});
