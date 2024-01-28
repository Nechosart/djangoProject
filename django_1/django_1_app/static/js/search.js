var input = document.getElementById('search');

function send(){
    if ($('#search').val() != '') {
        var button = $(this)
        $.ajax(button.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'typeSend': 'search',
                'search': $('#search').val()
            },
            'success': function(data){

            }
        })
    }
}

$('#btn').click(send)
input.addEventListener('keypress', function(event) {
    if (event.key == 'Enter' ) { send(); }
})
