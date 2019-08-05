$(function() { // shortcut for onDocumentReady
        $('.comment-section').hide()

        // When you click an "a" tag who is child of an item with class "subcategory_list"…
        $(document).on('click', '.comment-link', function() {
            var instance_id = $(this).attr('value')
            var comment_section = $(this).parent('div').find('.comment-section')
            if (comment_section.is(':visible')) {
                comment_section.hide()
                return false;
            }else{
                comment_section.show()
            }
            $.ajax({
                type: "GET",
                url: "/nomination_feed/" + instance_id + "/comment/", 
                success : function(data) {
                    console.log("our data",data);
                    comment_section.html(data)
                 },
                error: function(response) {
                    console.log("error",response)
                }
            });
            return false;
        });

        $(document).on('click', '.like-link', function(){
            var instance_id = $(this).attr('value')
            var like_btn = $(this)
            var like_count = like_btn.parent().find('.like-count')
            var like_count_val = like_count.html()
            $.ajax({
                type: "GET",
                url: "/nomination_feed/" + instance_id + "/like/", 
                success : function(data) {
                    if (data.value === "like"){
                        like_btn.html("Liked")
                        like_count.html("You and " + like_count_val)
                    }else{
                        like_btn.html("Like")
                        like_count.html(like_count_val.replace("You and ", ""))
                    }
                    console.log("our data",data);
                 },
                error: function(response) {
                    console.log("error",response)
                }
            });
            return false;

        })

        $(document).on('submit', '.post-form', function() {
            var instance_id = $(this).find('.send').attr('value')
            var comment_text_field = $(this).find('.comment-text')
            var comment_section = $(this).parent('div').find('.comment-section')
            var csrf = $(this).find('input').val()
            $.ajax({
                type: "POST",
                url: "/nomination_feed/" + instance_id + "/comment/", 
                data: {
                    comment: comment_text_field.val(),
                    'csrfmiddlewaretoken' : csrf
                },
                success : function(data) {
                    console.log("success");
                    comment_section.html(data)
                    comment_section.show()
                    comment_text_field.val('')
                },
                error: function(response) {
                    console.log("error",response)
                }
            });
            return false;
        });

    });