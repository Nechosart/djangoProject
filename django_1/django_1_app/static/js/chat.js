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
                var message = document.getElementById('messages')
                var message = document.createElement('message')
                message.style = style="background: rgb(0,255,255);";

                var user = document.createElement('a')
                user.href = '/user/'+data['user']['id'];
                user.classList.add('user');
                user.innerHTML = data['user']['username'];
                message.appendChild(user);

                var time = document.createElement('time')
                time.innerHTML = data['createdAt'];
                message.appendChild(time);

                var br = document.createElement('br')
                message.appendChild(br);


                message.innerHTML += $('#text').val();
                messages.appendChild(message);
                input.value = '';
                messages.scrollTo(0,999999);
            }
        })
    }
}

$('#btn').click(send)
input.addEventListener('keypress', function(event) {
    if (event.key == 'Enter' ) { send(); }
})