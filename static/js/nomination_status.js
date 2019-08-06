$(document).ready(function(){
  $(document).ajaxStop(function(){
    window.location.reload();
  });
  $.fn.editable.defaults.mode = 'inline';
  $('.fa-edit').on('click', function(event){
    event.stopPropagation()
  });
  $('.enddate').click(function(e) {
    e.stopPropagation();
    $(this).editable('show');
  });
  $('.enddate').on('shown', function(e, editable) {
    datetext = $(this).next().find('.datetext')
    $('.editable-submit').addClass('fa fa-check')
    $('.editable-cancel').addClass('fa fa-times')
    id = $(this).attr('data-pk')
    $('.editable-submit').on('click', function(e){
      e.stopPropagation();
      e.preventDefault();
      $.ajax({
        method: 'POST',
        url: '/nominations/'+ id + '/',
        data: {
          'date': datetext.val(),
          'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),

        },
        dataType: 'json',
        success: function (data) {
          location.reload()
        }
      });
    })

    $(this).next().find('.datetext')
    $(datetext).datepicker({ startDate: "today",  maxViewMode: 1, orientation: "bottom",});
    $(datetext).on('click', function(e){
      e.stopPropagation()
    })
    
  });
  $('.enddate').on('hidden', function(e, editable) {
    $(this).editable('destroy');
  });
  $('#vacation').editable();
  $(document).on('click', '.tab_forms', function(event) {
    award_id=$(this).attr('value');
    $.ajax({
      url:'/nomination_status_load/' + award_id + '/',
      type:'GET',
      dataType: 'json',
      data: { csrfmiddlewaretoken: '{{ csrf_token }}', id:  award_id},
      success:function (json) {
        var length = json.length
        if (length == 0)
          {
            data='No Nomination Records Found For Selected Award'
            $('#nomination_status_table').html(data);
          }
        else
        {
          $('#nomination_status_table').html('');
          for (i = 0; i <= length-1 ; i++) 
            {
              data='<tr class="row"><td class="col-sm-8 user_name"> '+ json[i].nominator_name +' </td><td class="col-sm-4 status"> '+ json[i].nominator_status +' </td></tr>'
              $('#nomination_status_table').append(data);
            }
        }  
      }
    });                                     
  });
});