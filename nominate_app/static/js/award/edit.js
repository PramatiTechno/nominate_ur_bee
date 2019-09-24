$(document).ready(function(){




  frequency_checker = {
   'MONTHLY': function(submission_start, approval_end){
        return (submission_start.getMonth() === approval_end.getMonth() && submission_start.getYear() === approval_end.getYear())
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
    cloneMore('div.add_nomination_period:visible:last', 'nominationperiod_set');
  });

 
  $(document).on("focus", ".datepicker", function(){
      $('.datepicker').attr('autocomplete',"off");

      $(this).datepicker({ startDate: "today",  maxViewMode: 1, orientation: "bottom", autoclose: true});
  });

  $('.datepicker').on('click', function(){
    $(this).show();
  });     

  $(document).on('change', '[type=checkbox]', function(event) {
  	 event.preventDefault();
  	if(event.target.id.endsWith('DELETE') ){
	    checkboxId = event.target.id;
	  	id_val = checkboxId.split('DELETE')[0]
	  	var child_id = Number($('#'+id_val+'id').val())
      $(this).val('on')

  		par_table = $('#'+checkboxId).closest('.add_nomination_period');
  		par_table.remove()
      deleteForm('nominationperiod_set','del_btn_formset')
  		if (child_id != 0){
  			$.ajax({
  					url:'/delete/' + child_id + '/',
  					type:'POST',
  					data:{
  						csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
  					},
  					dataType: 'json',
  					success:function(){
  					}
  			});
        re_calc_init()
  		}
      if(($('.del_btn_formset').length) == 1){
        $('.del_btn_formset').each(function(i, obj) {
            $(obj).hide()
        });
      }
      else{
        $('.del_btn_formset').each(function(i, obj) {
            $(obj).show()
        });    
      }
  	}	
  }); 
    
  function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').prop('checked', false);
        // if($(this).attr('id').endsWith('level') || $(this).attr('id').endsWith('day')){
        //   $(this).val(1)
        // }
    });
   
      newElement.find('label').each(function() {
         if ($(this).attr('for')  !== undefined ) {
          var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
          $(this).attr('for', newFor);
    }
      });
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
     newElement.find('input.datepicker')
    .removeData('datepicker')
    .unbind()
    .datepicker({ startDate: "today", maxViewMode: 1, orientation: "bottom", autoclose: true});
    $(selector).after(newElement);
  }

  function re_calc_init(){
    initial_count = $('#id_nominationperiod_set-INITIAL_FORMS').val();
    initial_count--;
    $('#id_nominationperiod_set-INITIAL_FORMS').val(initial_count);
    $('#id_nominationperiod_set-INITIAL_FORMS').attr('value', initial_count);
  }
});

function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1){
        var forms = $('.add_nomination_period');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}

function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}