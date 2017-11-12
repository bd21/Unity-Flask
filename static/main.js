var order = [];
var next = 0;

$(document).ready(function() {
    //make sure the list_order cookie is parsed
    update_list_order(Cookies.get("listOrder"));
    next = Cookies.get("nextToShow");
    alert(next);
});

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
    next++;
    Cookies.set("nextToShow", next);
    alert(next);
});