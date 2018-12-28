
(function ($, window, document) {

    "use strict";

function $onInit() {
    var ctrl = this;
        
    var options = { 
        now: "12:35", //hh:mm 24 hour format only, defaults to current time 
        twentyFour: false, //Display 24 hour format, defaults to false 
        upArrow: 'wickedpicker__controls__control-up', //The up arrow class selector to use, for custom CSS 
        downArrow: 'wickedpicker__controls__control-down', //The down arrow class selector to use, for custom CSS 
        close: 'wickedpicker__close', //The close class selector to use, for custom CSS 
        hoverState: 'hover-state', //The hover state class to use, for custom CSS 
        title: 'Timepicker', //The Wickedpicker's title, 
        showSeconds: false, //Whether or not to show seconds, 
        secondsInterval: 1, //Change interval for seconds, defaults to 1  , 
        minutesInterval: 1, //Change interval for minutes, defaults to 1 
        beforeShow: null, //A function to be called before the Wickedpicker is shown 
        show: null, //A function to be called when the Wickedpicker is shown 
        clearable: false, //Make the picker's input clearable (has clickable "x") 
    }; 
    // var myPicker = $('.timepicker').wickedpicker(); 
    $('.timepicker').wickedpicker(options);
    //myPicker.wickedpicker('setTime', 0, "5:00");
    console.log(timepickers.wickedpicker('time'));
}

/*
function $onSubmit() {
    var data = {    
        "brokerName": document.getElementById('playerName').value,
        "gameRoomName": document.getElementById('gameRoomName').value,
        "startingStockHoldings": document.getElementById('startingStockHoldings').value,
        "startingCash": document.getElementById('startingCash').value,
        "gameDuration": document.getElementById('myPicker').value,
        "playerIP": '127.0.0.1'
    };
    var input_json = JSON.stringify(data);
    console.log('input_json: ', input_json);
    $.post('/gameroom/', {data: input_json});

    //window.location.href = '../play/' + ctrl.gameRoomName;
}
*/

})(jQuery, window, document);


