/**
$("#pill-bottle-button").click(function() {
    $.post("https://us-central1-united-time-251622.cloudfunctions.net/website-call",
    {
        "userID":"customer0001",
        "pill_bottle":true
    },
    function(data, status) {
        console.log("Data: " + data)
        console.log("Status: " + status)
    })
});
**/

var STORAGE_BASE = 'https://storage.googleapis.com/';

$("#pill-bottle-button").click(function() {
    $.get("https://us-central1-united-time-251622.cloudfunctions.net/website-call?userID=customer0001&pill_bottle=True",
    function(data, status) {
        console.log("Data: " + data);
        console.log("Status: " + status);
        displayImgs(data);
    });
});

$("#food-button").click(function() {
    $.get("https://us-central1-united-time-251622.cloudfunctions.net/website-call?userID=customer0001&pill_bottle=True",
    function(data, status) {
        console.log("Data: " + data);
        console.log("Status: " + status);
        displayImgs(data);
    });
});

$("#people-button").click(function() {
    $.get("https://us-central1-united-time-251622.cloudfunctions.net/website-call?userID=customer0001&pill_bottle=True",
    function(data, status) {
        console.log("Data: " + data);
        console.log("Status: " + status);
        displayImgs(data);
    });
});

var displayImgs = function(data) {
    
    document.getElementById('img-section').querySelectorAll('*').forEach(n => n.remove());

    let paths = data.split(',');
    paths.forEach(function(path) {
        var newPath = "";
        if (path.startsWith('gs://')) {
            newPath = path.replace('gs://', STORAGE_BASE)
        }
        else {
            newPath = STORAGE_BASE + path;
        }
        var img = document.createElement('img');
        img.setAttribute("src", newPath);
        document.getElementById('img-section').append(img);
    });
}
