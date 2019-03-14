
$(document).on('change', '[type=selection]', function(event) {
event.preventDefault();
document.getElementById('create_link').href="/new_award_template/"+$(this).children("option:selected").val();
var award_id = $(this).children("option:selected").val();
$.ajax({
  url:'/award_template_load/' + award_id + '/',
  type:'GET',
  dataType: 'json',
  data: { csrfmiddlewaretoken: '{{ csrf_token }}' },
  success:function (json) {
      var length = json.length
      if (length == 0)
        {
          data='No Templates Found For Selected Award'
          $('#templates_table').html(data);
        }
      else
        {
          data=''
          $('#templates_table').html(data);
        }
      for (i = 0; i <= length-1 ; i++) 
      {
          data='<tr class="d-flex"><td class="col-10" style="padding-bottom: 6px; padding-top: 0;"> '+ json[i].fields.template_name +' </td><td class="col-2" style="padding-bottom: 6px; padding-top: 0;"><a href="/edit_award_template/'+json[i].pk+'" type="button" class="btn btn-success" value="View" >View</a></td></tr>'
          $('#templates_table').append(data);
      }
    }
  });
}); 

$(function() {
   $("#award").val($("#award option:first").val());
  if ($('.mySelect').val() != "No Awards Found" )
    {
      document.getElementById('create_link').href="/new_award_template/"+$('.mySelect').val()
    }

});