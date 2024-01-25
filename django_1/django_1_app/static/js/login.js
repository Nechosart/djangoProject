function test(){
    $('#btn').click(function(){
        var button = $(this)
        $.ajax(button.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'username': $('#id_username').val(),
                'password': $('#id_password').val()
            },
            'success': function(data){
                if (data['ok']) {
                    window.location.href = '/'
                } else {
                    document.getElementById('answer').style = "visibility: visible;";
                    document.getElementById('answer').innerHTML = data['text'];
                }
            }
        })
    })
}

$(document).ready(function(){
    test();
})
