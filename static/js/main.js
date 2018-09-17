function addZero(x,n) {
    while (x.toString().length < n) {
        x = '0' + x;
    }
    return x;
}

function getFullTime() {
    var d = new Date();
    var h = addZero(d.getHours(), 2);
    var m = addZero(d.getMinutes(), 2);
    var s = addZero(d.getSeconds(), 2);
    var ms = addZero(d.getMilliseconds(), 3);
    return (String(h) + String(m) + String(s) + String(ms));
}

$(document).ready(function(){
    var sock = {};
    try{
        sock = new WebSocket('ws://' + window.location.host + '/' + getFullTime() + '/ws');
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