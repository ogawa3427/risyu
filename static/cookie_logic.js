function cookiereader() {
    var cookie = document.cookie;
    var cookiearray = cookie.split(';');
    var cookieobj = {};
    for (var i = 0; i < cookiearray.length; i++) {
        var key = cookiearray[i].split('=')[0];
        var value = cookiearray[i].split('=')[1];
        cookieobj[key] = value;
    }
    return cookieobj;
}

function cookiewriter(cookieobj) {
    var cookie = '';
    for (var key in cookieobj) {
        cookie += key + '=' + cookieobj[key] + ';';
    }
    document.cookie = cookie;
}