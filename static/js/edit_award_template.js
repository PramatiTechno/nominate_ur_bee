
$(document).ready(function(){
  $('.objective-type').each(function(i, element){
    if(element.value == "SUBJECTIVE")
      $(this).parent().next().hide()
  })
  
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
  $(".objective-type").on('change', function(event){
    if(this.selectedIndex != 0){
      id = $(this).attr('id').split('-')[1]
      $('input[name="questions_set-'+ id +'-objectives"]').attr('required', true);

      $(this).parent().next().show()

    }else{
      id = $(this).attr('id').split('-')[1]
      $(this).parent().next().hide()
      $('input[name="questions_set-'+ id +'-objectives"]').attr('required', false);
    }
  });

  $(document).on('change', '[type=checkbox]', function(event) {
    event.preventDefault();
    if(event.target.id.endsWith('DELETE') ){
      
      checkboxId = event.target.id;
      id_val = checkboxId.split('DELETE')[0]
      var ques_id = Number($('#'+id_val+'id').val());
      $(this).val('on')

      par_table = $('#'+checkboxId).closest('.formset_table');
      par_table.remove();
      deleteForm('questions_set','del_btn_formset')

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
    else if (event.target.id.endsWith('-attachment_need')) {
      checkboxId = event.target.id;
      $(this).attr('value', this.checked ? 1 : 0);
      $(this).val(this.checked ? 1 : 0);
    }
  });

  function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
      var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
      var id = 'id_' + name;
      $(this).attr({'name': name, 'id': id}).val('').prop('checked', false);
      if($(this).attr('id').endsWith('qtype')){
        $(this).val('SUBJECTIVE')
      }
      else if($(this).attr('id').endsWith('role')){
        $(this).val(1)
      }
    });
    newElement.find('label').each(function() {
      if ($(this).attr('for')  !== undefined ) {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
      }  
    });
    newElement.find('.objective-type-container').each(function(){
      var container_id = $(this).attr('id').replace('-' + (total-1) + '-','-' + total + '-');
      $(this).attr('id', container_id)
    });
    newElement.find('.objective-add-button').each(function(){
      $(this).attr('value', "Add Choice")
    });
    newElement.find('.objective-cancel').each(function(){
      $(this).attr('value', "Remove")
    });
    newElement.find('.input-group').each(function(){
      id = $(this).children().first().children().attr('id');
      
      if($(this).parent().children().length != 2){
        $(this).remove()
      }else{
        inputText =$(this).children().first().children()
        oldName = inputText.attr('name')
        temp = oldName.split('-');
        temp[1] = "" + total
        newName = temp.join('-')
        inputText.attr('name', newName)
      }
      
    });
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    $("#id_questions_set-"+ (total-1) +"-objective-container").hide()
    $('input[name="questions_set-'+ (total-1) +'-objectives"]').removeAttr('required');
    
  }

  function re_calc_init(){
    initial_count = $('#id_questions_set-INITIAL_FORMS').val();
    initial_count--;
    $('#id_questions_set-INITIAL_FORMS').val(initial_count);
    $('#id_questions_set-INITIAL_FORMS').attr('value', initial_count);
  }
  function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1){
        var forms = $('.formset_table');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}

$('.objective-add-button').click(function(){
  parentElement = $(this).prev().clone(true)
  newElement = $(parentElement).children().first().children()
  oldId = $(newElement).attr('id')
  dconstructedId = oldId.split('-') 
  dconstructedId[1] = "" + (parseInt(dconstructedId[1]) + 1)
  newId = dconstructedId.join("-")
  $(newElement).val('');
  $(newElement).attr('id',newId)
  $(this).before(parentElement)
});

$('.objective-cancel').click(function(){

  if($(this).parent().parent().parent().children().length !=2){
    $(this).parent().parent().remove()
  }

});

function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}


});
