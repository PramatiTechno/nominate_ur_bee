$(function() {

    $("#datepicker").datepicker({
        format: "MM yyyy",
        startView: "months",
        minViewMode: "months"
    });

    $('.submit').on('click', function() {
        var date = $('#datepicker').val()
        if (date != '') {
            $('#date-form').submit()
        }
    })

})