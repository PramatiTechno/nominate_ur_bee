$(document).ready(function(){

 if(($('.del_btn_formset').length) == 1){
    $('.del_btn_formset').hide()
  }
  else{
    $('.del_btn_formset').each(function(i, obj) {
        $(obj).show()
    });
  }
  $('#add_more').click(function() {
    $('.del_btn_formset').each(function(i, obj) {
        $(obj).show()
    });  
    cloneMore('div.add_template_questions:visible:last', 'questions_set');
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
      checkboxId = event.target.id;
      id_val = checkboxId.split('DELETE')[0]
      var ques_id = Number($('#'+id_val+'id').val());
      $(this).val('on')

      par_table = $('#'+checkboxId).closest('.formset_table');
      par_table.hide();

      if (ques_id != 0){
        $.ajax({
          url:'/question/delete/' + ques_id + '/',
          type:'POST',
          data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
          },
          dataType: 'json',
          success:function(){

          }
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
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        if($(this).attr('id').endsWith('qtype')){
          $(this).val('SUBJECTIVE')
        }
        else{
          $(this).val(1)
        }
    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
    });
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
  }

});