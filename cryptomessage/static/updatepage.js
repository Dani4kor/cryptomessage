/* update page.js */
$(document).ready(function() {
    $('#reload-button').click(function(event) {
        jQuery.ajax({
            url: '//localhost:8888/',
            type: 'POST',
            dataType: 'json',
            data: {
                action: 'reload',
            },
            success: function() {
                window.location.reload(true);
            }
        });
    });
});