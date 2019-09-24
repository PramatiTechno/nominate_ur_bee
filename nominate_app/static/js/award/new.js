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

  var elements = document.querySelectorAll('input,select,textarea');
  var invalidListener = function(){ this.scrollIntoView(false);};

  for(var i = elements.length; i--;)
    elements[i].addEventListener('invalid', invalidListener);

  frequency_checker = {
   'MONTHLY': function(submission_start, approval_end){
        return (submission_start.getMonth() === approval_end.getMonth()) && (submission_start.getYear() === approval_end.getYear())
    },
    'QUATERLY': function(submission_start, approval_end){
        var start_year = submission_start.getYear()
        var start_month = submission_start.getMonth() + start_year * 12;
        return (approval_end.getMonth() + approval_end.getYear() * 12 <= (start_month + 2))
    },
    'YEARLY': function(submission_start, approval_end){
        return (submission_start.getYear() === approval_end.getYear())
    }
  }

  $('#award_form').on('submit', function(){

    var frequency = $(this).find('#exampleSelect1').val()
    var error = $('.error')

    var submission_start = $(this).find('#id_nominationperiod_set-0-start_day').val()
    var rating_start = $(this).find('#id_nominationperiod_set-1-start_day').val()
    var approval_start = $(this).find('#id_nominationperiod_set-2-start_day').val()

    var submission_end = $(this).find('#id_nominationperiod_set-0-end_day').val()
    var rating_end = $(this).find('#id_nominationperiod_set-1-end_day').val()
    var approval_end = $(this).find('#id_nominationperiod_set-2-end_day').val()

    if (submission_start !== '' || rating_start !== '' || approval_start !== '' || submission_end !== '' || rating_end !== '' || approval_end !== ''){
      submission_start = new Date(submission_start)
      rating_start = new Date(rating_start)
      approval_start = new Date(approval_start)
      submission_end = new Date(submission_end)
      rating_end = new Date(rating_end)
      approval_end = new Date(approval_end)
      if (check_start_end_exceed(submission_start, submission_end, rating_start, rating_end, approval_start, approval_end)){
        if (frequency_checker[frequency](submission_start, approval_end)){
          return true
        } else {
          error.html('* Frequency and Period dates does not match')
          return false
        }

      } else {
          error.html('* Period Start and End date chain Exceeds')
          return false
      }
    } else {
      error.html('* please fill all the dates')
      return false
    }
  })

  function check_start_end_exceed(submission_start, submission_end, rating_start, rating_end, approval_start, approval_end){
    if (submission_start < submission_end && rating_start < rating_end && approval_start < approval_end){
      if (submission_end < rating_start && rating_end < approval_start){
        return true;
      }
    }
    return false;
  }


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
