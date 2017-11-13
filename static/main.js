var order = []; // order of games
var next = 0; // current index of order to show next

$(document).ready(function() {
    // make sure cookie containing the order is set
    if(order.length === 0) {
        update_list_order(Cookies.get("listOrder"));
    }
    next = Cookies.get("nextToShow");
    display_game_info();
});

// display game information
function display_game_info() {
    $.getJSON("game/" + next, function(data) {
        $("h2").text(data.title);
        $("p").text(data.description);
        $("a").attr("href", data.gameLink);
        $("img").attr("src", data.pictureURL);
        $("#developer").append(data.developer);
        $("#developer").attr("href", data.developerLink);
        $("#platforms").append(data.platform);
        $("#genres").append(data.genres);
    });
}

// parse the cookie and store it in array.
function update_list_order(list) {
    //decode flask cookie
    list = list.replace('[', '');
    list = list.replace(']', '');
    list = list.replace(/\\/g, '');
    list = list.replace(/054/g, '');
    order = list.split(' ');
}

// called on refresh
// increments nextToShow cookie and resets it to zero
// if it reaches the end of the array
$(window).on('beforeunload', function(){
    if(next >= order.length - 1)
        next = 0;
    else
        next++;
    Cookies.set("nextToShow", next);
});

