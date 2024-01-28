$('document').ready(function(){

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