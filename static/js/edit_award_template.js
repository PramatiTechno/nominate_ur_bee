
      $('#add_more').click(function() {
        console.log("in checkbox click")
          cloneMore('div:last', 'form');
      });

      $(document).on('change', '[name^=form-]', function(event) {
        event.preventDefault();
        checkboxId = event.target.id;
        ques_id = Number($('#'+checkboxId).next('input')[0].value);
        console.log(ques_id)
        par_table = $('#'+checkboxId).closest('.form_table');
        par_table.hide();
        // need ajax func for edit questions template form
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
      
    }); 
      function cloneMore(selector, type) {
        var newElement = $(selector).clone(true);
        var total = $('#id_' + type + '-TOTAL_FORMS').val();
        newElement.find(':input').each(function() {
            var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        });
        newElement.find('label').each(function() {
            var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
            $(this).attr('for', newFor);
        });
        total++;
        $('#id_' + type + '-TOTAL_FORMS').val(total);
        $(selector).after(newElement);
    }