function test(){
    $('#btn').click(function(){
        var button = $(this)
        $.ajax(button.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'name': $('#name').val()
            },
            'success': function(data){
                document.getElementById('#pr_name').innerHTML = data['resp'];
            }
        })
    })
}

$(document).ready(function(){
    test();
})
