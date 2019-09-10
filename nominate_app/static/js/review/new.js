$(document).ready(function(){
	$('.submission-rating').starRating({
		ratedColor: 'gold',
    	starSize: 18,
		useFullStars: true,
		disableAfterRate: false,
    	callback: function(currentRating, $el){
        // make a server call here
    	}
	})

	$('.post-review').on("click", function() {
	   	var rating = $('.submission-rating').starRating('getRating')
	   	var review = $('.review').val()
	   	var submission_id = $('.submission-id-field').val()

	    nojax_post('/nomination_review/'+submission_id, {
	    	'review': review,
	    	'rating': rating
	    })
	  });


	    function nojax_post (to,p) {
		  var myForm = document.createElement("form");
		  myForm.method="post" ;
		  myForm.action = to ;
		  for (var k in p) {
		    var myInput = document.createElement("input") ;
		    myInput.setAttribute("name", k) ;
		    myInput.setAttribute("value", p[k]);
		    myForm.appendChild(myInput) ;
		  }
		  document.body.appendChild(myForm) ;
		  myForm.submit() ;
		  document.body.removeChild(myForm) ;
		}


})