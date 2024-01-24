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
                    post.style = "visibility: visible; position: absolute;";
                    postEdit.style = "visibility: hidden; position: relative;";
                } else {
                    document.getElementById('post').innerHTML += data['error'];
                }
            }
        })
    })
}

$(document).ready(function(){ comment(); })
$(document).ready(function(){ postEdit(); })
