$(function() {
  // shortcut for onDocumentReady

  // script for filter option
  $("#filter-block").css("display", "none");
  $("#filter-block").css("position", "absolute");
  $("#filter-block").css("z-index", "999");
  $("#filter-block").css("background", "white");

  $("#arrow").click(function() {
      if ($("#filter-block").is(":visible")) {
          $("#arrow").css("transform", "rotate(360deg)");
          $("#filter-block").css("display", "none");
          $("#filter-block").css("position", "absolute");
          $("#filter-block").css("z-index", "999");
          $("#filter-block").css("background", "white");
      } else {
          $("#arrow").css("transform", "rotate(180deg)");
          $("#arrow").css("padding-bottom", "5px");
          $("#filter-block").css("display", "block");
      }
  });

  //infinite scroll
  var infinite = new Waypoint.Infinite({
      element: $('.infinite-container')[0],
      onBeforePageLoad: function() {
          $('.loading').show();
          query_strings = window.location.search
          if (query_strings !== "") {
              $('.infinite-more-link').attr('href', $('.infinite-more-link').attr('href') + "&" + query_strings)
          }
      },
      onAfterPageLoad: function($items) {
          $('.loading').hide();
      }
  });


  $(".comment-section").hide();
 
  $('.datepicker').datepicker({
    maxViewMode: 1, 
    orientation: "bottom",
    autoclose: true,
  });
  $(".datepicker").attr("autocomplete", "off");


  // like link event
  $(document).on("click", ".like-link", function() {
    var instance_id = $(this).attr("value");
    var like_btn = $(this);
    var like_count = $(this)
      .parents("div.card-body")
      .find(".like-count");
    var like_count_val = like_count.html();
    $.ajax({
      type: "GET",
      url: "/nomination_feed/" + instance_id + "/like/",
      success: function(data) {
        if (data.value === "like") {
          like_btn.html("<i class='fa fa-heart'></i>");
          like_count.html("You and " + like_count_val);
        } else {
          like_btn.html("<i class='fa fa-heart-o'></i>");
          like_count.html(like_count_val.replace("You and ", ""));
        }
        console.log("our data", data);
      },
      error: function(response) {
        console.log("error", response);
      }
    });
    return false;
  });


  // like count event
  $(document).on("click", ".like-count", function() {
    var instance_id = $(this).attr("value");
    var count_link = $(this);
    $.ajax({
      type: "GET",
      url: "/nomination_feed/" + instance_id + "/liked_people/",
      success: function(data) {
        var modalDiv = $(".modal-body");
        var modal_content = "";
        data.liked_people.forEach(function(ppl, index) {
          modal_content = modal_content + "<p>" + ppl + "</p>";
        });
        modalDiv.html(modal_content);
        $("#like_modal").modal("show");
      },
      error: function(response) {
        console.log("error", response);
      }
    });
    return false;
  });

  // comment-link event
  $(document).on("click", ".comment-link", function() {
    var instance_id = $(this).attr("value");
    var comment_section = $(this)
      .parents("div.card-body")
      .find(".comment-section");

    var comment_rows = comment_section.find(".comment-rows");
    if (comment_section.is(":visible")) {
      comment_section.hide();
      return false;
    }
    if (comment_rows.children().length > 0) {
      comment_section.show();
      return false;
    }
    $.ajax({
      type: "GET",
      url: "/nomination_feed/" + instance_id + "/comment/",
      success: function(data) {
        console.log("our data", data);
        comment_rows.html(data);
        comment_section.show();
      },
      error: function(response) {
        console.log("error", response);
      }
    });
    return false;
  });

  // more comment event
  $(document).on("click", ".more-comments", function() {
    var more_comment_link = $(this);
    var comment_rows = $(this).parents("div.comment-rows");
    var instance_id = comment_rows.find("span.instance_id_span").html();
    var next_page = $(this).attr("value");

    $.ajax({
      type: "GET",
      url: "/nomination_feed/" + instance_id + "/comment/?page=" + next_page,
      success: function(data) {
        console.log("our data", data);
        more_comment_link.remove();
        comment_rows.prepend(data);
      },
      error: function(response) {
        console.log("error", response);
      }
    });
    return false;
  });


  // comment submit event
  $(document).on("submit", ".post-form", function() {
    var instance_id = $(this)
      .find(".send")
      .attr("value");
    var comment_text_field = $(this).find(".comment-text");
    var comment_rows = $(this)
      .parent("div")
      .find(".comment-rows");
    var csrf = $(this)
      .find("input")
      .val();
    $.ajax({
      type: "POST",
      url: "/nomination_feed/" + instance_id + "/comment/",
      data: {
        comment: comment_text_field.val(),
        csrfmiddlewaretoken: csrf
      },
      success: function(data) {
        console.log("success");
        comment_rows.append(data);
        comment_text_field.val("");
      },
      error: function(response) {
        console.log("error", response);
      }
    });
    return false;
  });


  // comment delete event
  $(document).on("click", ".comment-delete", function() {
    var comment_section = $(this).parents("div.comment-section");
    var comment_row = $(this).parents("div.comment");
    var instance_id = comment_section.find("span.instance_id_span").html();
    var comment_id = $(this).attr("value");
    $.ajax({
      type: "GET",
      url: instance_id + "/comment/" + comment_id + "/delete",
      success: function(data) {
        console.log("success");
        if (data.status == "deleted") {
          comment_row.remove();
        }
      },
      error: function(response) {
        console.log("error", response);
      }
    });
    return false;
  });
});
