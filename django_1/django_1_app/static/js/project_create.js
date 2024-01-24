function test(){
    $('#btn').click(function(){
        $.ajax('/project_create/', {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'name': $('#name').val()
            },
            'success': function(data){
                document.getElementById('resp').innerHTML += data['resp']
            }
        })
    })
}

$(document).ready(function(){
    test();
})
