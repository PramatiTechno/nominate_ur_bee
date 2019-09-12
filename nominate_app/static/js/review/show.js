$(document).ready(function(){
	$('.submission-rating').starRating({
   		starSize: 18,
		readOnly: true,
    	callback: function(currentRating, $el){
        // make a server call here
    	}
	})
})