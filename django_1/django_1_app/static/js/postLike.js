
var like = document.getElementById('{{p.id}}');
var likes = {{p.likes.count}};
var liked = {% if p.liked %} true; likes -= 1; {% else %} false; {% endif %}
var likesEl = document.getElementById('{{p.id}}s');

like.onclick = function(){
    if ({{user.id}}) {

        liked = !liked;
        if (liked) {
            like.src = '/static/liked.png';
            likesEl.innerHTML = likes + 1;
        } else {
            like.src = '/static/like.png';
            likesEl.innerHTML = likes;
        }

        var button = $(this)
        $.ajax(button.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'typeSend': 'like',
                'post': {{p.id}}
            },
            'success': function(data){

            }
        })
    }
};