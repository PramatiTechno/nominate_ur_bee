$(function() {

    $("#datepicker").datepicker({
        format: "MM yyyy",
        startView: "months",
        minViewMode: "months",
        autoclose: true
    });

    $('.submit').on('click', function() {
        var date = $('#datepicker').val()
        if (date != '') {
            $('#date-form').submit()
        }
    })

})