$(document).ready(function () {
    $('#runajax').click(function (event) {
        var messageval = $("#inputmessage").val();
        var data =
        {
            message: messageval
        };
        var dataToSend = JSON.stringify(data);
        $.ajax(
                {
                    url: '/update/',
                    type: 'POST',
                    data: dataToSend,
                    success: function (jsonResponse) {
                        var objresponse = JSON.parse(jsonResponse);
                        console.log(objresponse['newkey']);
                        $("#message").text(objresponse['newkey']);
                    },
                    error: function () {
                        $("#message").text("Error to load api");
                    }
                });
        event.preventDefault();
    });
});