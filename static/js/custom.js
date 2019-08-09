function autoHeight() {
  var bodyHeight = $(document).height();
  var vwptHeight = $(".col-lg-10.col-sm-10.content").height() + 80;
  var gap = bodyHeight - 120;
  if (vwptHeight < bodyHeight) {
    $(".col-lg-10.col-sm-10.content").css("min-height", gap);
  }
}
$(document).ready(function() {
  autoHeight();
});
$(window).resize(function() {
  autoHeight();
});
