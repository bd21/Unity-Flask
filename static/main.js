var order = [];
var next = 0;

$(document).ready(function() {
    //make sure the list_order cookie is parsed
    if(order.length === 0) {
        update_list_order(Cookies.get("listOrder"));
    }
    next = Cookies.get("nextToShow");
    //update to show what order and next are
    $("ul").append("next is " + next + " and order[next] is " + order[next]);
    update_game_info();

});

function update_game_info() {

    $.getJSON("game/" + next, function(data){
        var items = []
        $.each( data, function( key, val ) {
            items.push( "<li id='" + key + "'>" + val + "</li>" );
        });

        $( "<ul/>", {
            "class": "my-new-list",
            html: items.join( "" )
        }).appendTo( "body" );
    });
}

function update_list_order(list) {
    //decode flask cookie
    list = list.replace('[', '');
    list = list.replace(']', '');
    list = list.replace(/\\/g, '');
    list = list.replace(/054/g, '');
    order = list.split(' ');

}

// called on refresh, increments nextToShow cookie
$(window).on('beforeunload', function(){
    if(next >= 76)
        next = 0;
    else
        next++;
    Cookies.set("nextToShow", next);
});

