$(document).ready(function(){

  $("#start_date").datepicker({
    maxViewMode: 1, 
    orientation: "bottom",
    autoclose: true,
  });
  $("#end_date").datepicker({
    maxViewMode: 1, 
    orientation: "bottom",
    autoclose: true,
  });

  $('.datepicker').attr('autocomplete',"off");
  $('.nomination-instances').hide()
  
  $(".show-nominations").on('click', function(){
    var nomination_row = $(this).parents('.nomination-row')
    while (nomination_row.attr('class') !== "nomination-instances"){
      nomination_row = nomination_row.next()
    }
    nomination_row.toggle()
  });
  
  $.fn.editable.defaults.mode = 'inline';

  $('.enddate').click(function(e) {
    e.stopPropagation();
    $(this).editable('show');
  });
  
  $('.enddate').on('shown', function(e, editable) {

    datetext = $(this).next().find('.datetext')
    $('.editable-submit').addClass('fa fa-check')
    $('.editable-cancel').addClass('fa fa-times')
    var period = $(this).attr('data-period')
    id = $(this).attr('data-pk')
    $('.editable-submit').on('click', function(e){
      e.stopPropagation();
      e.preventDefault();
      $.ajax({
        method: 'POST',
        url: '/nominations/'+ id + '/',
        data: {
          'date': datetext.val(),
          'period': period,
          'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),

        },
        dataType: 'json',
        success: function (data) {
          window.location.reload();
        }
      });    
    })

    $(this).next().find('.datetext')
    $(datetext).datepicker({ startDate: "today",  maxViewMode: 1, orientation: "bottom", autoclose: true});

    $(datetext).on('click', function(e){
      e.stopPropagation()
    })
    
  });


  $('.enddate').on('hidden', function(e, editable) {
    $(this).editable('destroy');
  });

  $('.submission-rating').starRating({
      starSize: 15,
      readOnly: true,
      callback: function(currentRating, $el){
      }
  })

  $("#show-nominations i").click(function(){
      $(this).toggleClass('fa-plus fa-minus');
  });


  $(document).on('click', '.reminder-mail', function(event){
    var username_and_instance_id = $(this).attr('value')
    $.ajax({
      type: "GET",
      url: "/reemail/"+ username_and_instance_id + "/",
      success: function(data) {
        if (data.status === "sent"){
          alert("Reminder Email has been sent")
        }else{
          alert("Email not sent !")
        }
      },
      error: function(response) {
        console.log("error", response);
      }
    })
    return false
  })

});