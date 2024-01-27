var input = document.getElementById('text');
document.getElementById('messages').scrollTo(0,999999);

function send(){
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
                document.getElementById('messages').scrollTo(0,999999);
            }
        })
    }
}

$('#btn').click(send)
input.addEventListener('keypress', function(event) {
    if (event.key == 'Enter' ) { send(); }
})