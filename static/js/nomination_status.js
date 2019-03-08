$(document).ready(function(){
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
            data='<tr class="row"><td class="col-sm-8"> '+ json[i].nominator_name +' </td><td class="col-sm-8"> '+ json[i].nominator_status +' </td></tr>'
            $('#nomination_status_table').append(data);
          }
        }  
      }
    });                                     
  });
});