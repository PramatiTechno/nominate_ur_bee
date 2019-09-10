$(document).ready(function(){
    $("#submit_button").on("click", function(event){
      validate_checkbox(event)
    });
    $("#save_button").on("click", function(event){
      validate_checkbox(event)
  });
  $('.multichoice-option').on('change', function(){
    
    if($(this).attr("checked")){
      $(this).removeAttr("checked")
    }else{
      $(this).attr("checked", "checked")
    }
  })
  function validate_checkbox(event){
    $('.checkbox-container').map(function(){

      flag = false
      $(this).children().toArray().forEach(element => {
        if($(element).attr("checked")){
          flag = true
        }
      });
      if(!flag){
        event.preventDefault()
        $(this).find('.hidden').removeClass('hidden')
      }
    });
  }
  });