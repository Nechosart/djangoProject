function comment(){
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
}

function postEdit(){
    $('#btn').click(function(){
        var button = $(this)
        $.ajax(button.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'typeSend': false,
                'name': $('#name').val(),
                'description': $('#description').val()
            },
            'success': function(data){
                if(data['ok']) {
                    var post = $('#post');
                    var postEdit = $('#postEdit');
                    postEdit.style = "visibility: hidden;";
                    post.style = "visibility: visible;";
                    postEdit.replaceWith(post);

                    post.innerHTML = 'worked'
                } else {
                    document.getElementById('post').innerHTML += data['error'];
                    document.getElementById('post').style = "visibility: visible;";
                }
            }
        })
    })
}

$(document).ready(function(){ comment(); })
$(document).ready(function(){ postEdit(); })
