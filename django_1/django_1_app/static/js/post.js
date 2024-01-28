var input = document.getElementById('text');

function send(){
    if ($('#text').val() != '') {
        var button = $(this)
        $.ajax(button.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'typeSend': 'comment',
                'text': $('#text').val()
            },
            'success': function(data){
                var comments = document.getElementById('comments')
                var comment = document.createElement('message')
                comment.style = style="background: rgb(0,255,255);";

                var user = document.createElement('a')
                user.href = '/user/'+data['user']['id'];
                user.classList.add('user');
                user.innerHTML = data['user']['username'];
                comment.appendChild(user);

                var time = document.createElement('time')
                time.innerHTML = data['createdAt'];
                comment.appendChild(time);

                var br = document.createElement('br')
                comment.appendChild(br);


                comment.innerHTML += $('#text').val();
                comments.insertBefore(comment, comments.firstChild);
                input.value = '';
            }
        })
    }
}

$('#btnCom').click(send)
input.addEventListener('keypress', function(event) {
    if (event.key == 'Enter' ) { send(); }
})


$('#btnEdit').click(function(){
    var formData = new FormData();
    formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val())
    formData.append('typeSend', 'postEdit')
    formData.append('name', $('#name').val())
    formData.append('description', $('#description').val())
    formData.append('file', document.getElementById('file').files[0])

    var button = $(this);
    $.ajax(button.data('url'), {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': formData,
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

