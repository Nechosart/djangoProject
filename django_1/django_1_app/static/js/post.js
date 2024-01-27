$('#btnCom').click(function(){
    var button = $(this)
    $.ajax(button.data('url'), {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'typeSend': true,
            'text': $('#text').val()
        },
        'success': function(data){
            document.getElementById('comAnswer').innerHTML = data['comment'];
            $('#comAnswer').style.visibility = 'visible';
        }
    })
})


$('#btnEdit').click(function(){
    var button = $(this);
    $.ajax(button.data('url'), {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'typeSend': 'postEdit',
            'name': $('#name').val(),
            'description': $('#description').val()
        },
        'success': function(data){
            if(data['ok']) {
                window.location.reload();
            } else {
                document.getElementById('post').innerHTML += data['error'];
                document.getElementById('post').style = "visibility: visible;";
            }
        }
    })
})

