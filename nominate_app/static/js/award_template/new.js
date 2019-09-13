$(document).ready(function(){

  
  $('.multi-select').select2({
    placeholder: "select a group"
  });

  $('.objective-type').each(function(i, element){
    if(element.value == "SUBJECTIVE")
      $(this).parent().next().hide()
  })




$(".objective-type").on('change', function(event){
  if(this.selectedIndex != 0){
    
    $(this).parent().next().show()
    id = $(this).attr('id').split('-')[1]
    $('input[name="questions_set-'+ id +'-objectives"]').attr('required', true);


  }else{
    id = $(this).attr('id').split('-')[1]
      $(this).parent().next().hide()
      $('input[name="questions_set-'+ id +'-objectives"]').attr('required', false);
  }
});

  $(".objective-add-button").click(function() {
    parentElement = $(this)
      .prev()
      .clone(true);
    newElement = $(parentElement)
      .children()
      .first()
      .children();
    oldId = $(newElement).attr("id");
    dconstructedId = oldId.split("-");
    dconstructedId[1] = "" + (parseInt(dconstructedId[1]) + 1);
    newId = dconstructedId.join("-");
    $(newElement).val("");
    $(newElement).attr("id", newId);
    $(this).before(parentElement);
  });

  

  $(".objective-cancel").click(function() {
    if (
      $(this)
        .parent()
        .parent()
        .parent()
        .children().length != 2
    ) {
      $(this)
        .parent()
        .parent()
        .remove();
    }
  });
  if ($(".del_btn_formset").length == 1) {
    $(".del_btn_formset").hide();
  } else {
    $(".del_btn_formset").each(function(i, obj) {
      $(obj).show();
    });
  }
  $("#add_more").click(function() {
    $(".del_btn_formset").each(function(i, obj) {
      $(obj).show();
    });
    cloneMore("div.add_template_questions:last", "questions_set");
  });

  $(document).on("change", ".del_btn_formset", function(event) {
    if ($(".del_btn_formset").length == 2) {
      $(".del_btn_formset").each(function(i, obj) {
        $(obj).hide();
      });
    } else {
      $(".del_btn_formset").each(function(i, obj) {
        $(obj).show();
      });
    }
    event.preventDefault();
    checkboxId = event.target.id;
    par_table = $("#" + checkboxId).closest(".formset_table");
    par_table.remove();
    re_calc_total();
    // need ajax func for edit questions template form
  });
  function cloneMore(selector, type) {
    group_select = $(selector).find('.multi-select')
    group_select.select2('destroy')

    var newElement = $(selector).clone(true);
    var total = $("#id_" + type + "-TOTAL_FORMS").val();
    newElement.find(":input").each(function() {
      var name = $(this)
        .attr("name")
        .replace("-" + (total - 1) + "-", "-" + total + "-");
      var id = "id_" + name;
      $(this)
        .attr({ name: name, id: id })
        .val("")
        .prop("checked", false);
      if($(this).attr("id").endsWith('objectives')){
        $(this).attr('required', false)
      }
      if (
        $(this)
          .attr("id")
          .endsWith("qtype")
      ) {
        $(this).val("SUBJECTIVE");
      } else if (
        $(this)
          .attr("id")
          .endsWith("group")
      ) {
        $(this).val(1);
      }
    });
    newElement.find("label").each(function() {
      if ($(this).attr("for") !== undefined) {
        var newFor = $(this)
          .attr("for")
          .replace("-" + (total - 1) + "-", "-" + total + "-");
        $(this).attr("for", newFor);
      }
    });
    newElement.find(".objective-type-container").each(function() {
      var container_id = $(this)
        .attr("id")
        .replace("-" + (total - 1) + "-", "-" + total + "-");
      $(this).attr("id", container_id);
    });
    newElement.find(".objective-add-button").each(function() {
      $(this).attr("value", "Add Choice");
    });
    newElement.find(".objective-cancel").each(function() {
      $(this).attr("value", "Remove");
    });
    newElement.find(".input-group").each(function() {
      id = $(this)
        .children()
        .first()
        .children()
        .attr("id");

      if (
        $(this)
          .parent()
          .children().length != 2
      ) {
        $(this).remove();
      } else {
        inputText = $(this)
          .children()
          .first()
          .children();
        oldName = inputText.attr("name");
        temp = oldName.split("-");
        temp[1] = "" + total;
        newName = temp.join("-");
        inputText.attr("name", newName);
      }
    });
    total++;
    $("#id_" + type + "-TOTAL_FORMS").val(total);
    $(selector).after(newElement);
    $("#id_questions_set-" + (total - 1) + "-objective-container").hide();
    $('.multi-select').select2({
      placeholder: "Select a group",
    });
    group_select.select2({
      placeholder: "Select a group",
    })
  }

  function re_calc_total() {
    var total = $("#id_questions_set-TOTAL_FORMS").val();
    total--;
    $("#id_questions_set-TOTAL_FORMS").val(total);
    $("#id_questions_set-TOTAL_FORMS").attr("value", total);
  }

  $(document).on("change", "[type=checkbox]", function(event) {
    if (event.target.id.endsWith("-attachment_need")) {
      event.preventDefault();
      checkboxId = event.target.id;
      $(this).attr("value", this.checked ? 1 : 0);
      $(this).val(this.checked ? 1 : 0);
    }
  });
});
