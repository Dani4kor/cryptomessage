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
                    url: '/parse/',
                    type: 'POST',
                    data: dataToSend,
                    success: function (jsonResponse) {
                        var objresponse = JSON.parse(jsonResponse);
                        $("#image").attr('src', objresponse['img']);
                    },
                    error: function () {
                        console.log('"Error to load img"');
                    }
                });
        event.preventDefault();
    });
});

