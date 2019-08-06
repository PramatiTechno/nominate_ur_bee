$(document).ready(function(){

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
          window.location.reload();
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

});