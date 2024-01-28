$('document').ready(function(){

    $('#btnEdit').click(function(){

        var formData = new FormData();
        formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val())
        formData.append('typeSend', 'userEdit')
        formData.append('username', $('#username').val())
        formData.append('email', $('#email').val())
        formData.append('file', document.getElementById('file').files[0])

        var button = $(this);
        $.ajax(button.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function(data){
                window.location.reload();
            }
        })
    })

    var subscribe = document.getElementById('subscribe');
    subscribe.classList.add('buttonSubscribed');
    if (subscribe.innerHTML == 'Subscribe') {
        subscribe.classList.remove('buttonSubscribed');
    }

    $('#subscribe').click(function(){
        if (subscribe.innerHTML == 'Subscribe') {
            subscribe.innerHTML = 'Subscribed';
            subscribe.classList.add('buttonSubscribed');
        } else {
            subscribe.innerHTML = 'Subscribe';
            subscribe.classList.remove('buttonSubscribed');
        }


        var button = $(this);
        $.ajax(button.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'typeSend': 'subscribe'
            },
            'success': function(data){

            }
        })
    })

})