function autoHeight() {
  var bodyHeight = $(window).height();
  var vwptHeight = $(".col-sm-10.content").height() + 80;
  var gap = bodyHeight - 120;
  if (vwptHeight < bodyHeight) {
    $(".col-sm-10.content").css("height", gap);
  }
}
$(document).ready(function() {
  autoHeight();
});
$(window).resize(function() {
  autoHeight();
});
