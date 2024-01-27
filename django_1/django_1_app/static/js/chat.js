var input = document.getElementById('text');

function send(){
alert('test')
    if ($('#text').val() != '') {
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
                var message = document.createElement('message')
                message.style = style="background: rgb(0,255,255);";
                message.innerHTML = $('#text').val();
                document.getElementById('messages').appendChild(message);
                input.value = '';
            }
        })
    }
}

$('#btn').click(send)
input.addEventListener('keypress', function(event) {
    if (event.key == 'Enter' ) { send(); }
})