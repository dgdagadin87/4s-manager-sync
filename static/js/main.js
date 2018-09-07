$(document).ready(function(){
    var sock = {};
    try{
        sock = new WebSocket('ws://' + window.location.host + '/ws');
    }
    catch(err){
        sock = new WebSocket('wss://' + window.location.host + '/ws');
    }

    $('#sync-button').click(function(){

        var checkBoxes = $('.sync-checkbox');
        var items = [];

        checkBoxes.each(function(i, syncCheckbox){
            var currentItem = $(syncCheckbox);
            var isChecked = currentItem.prop('checked');
            var currentId = currentItem.attr('itemId');

            if (isChecked) {
                items.push(currentId)
            }
        });

        if (items.length < 1) {
            alert('Выберите категории для синхронизации');
            return;
        }

        sock.send(JSON.stringify({
            msg_type: 'COMMON_START_SYNC',
            msg_data: items.join(',')
        }));
    });

    sock.onopen = function(){
        console.log('Connection to server started');
    };

    sock.onmessage = function(event) {

        var data = event.data || '{}'
        console.log(JSON.parse(data))
    };

    sock.onclose = function(event){
        if(event.wasClean){
            console.log('Clean connection end');
        }
        else{
            console.log('Connection broken');
        }
    };

    sock.onerror = function(error){
        console.log(error);
    };
});