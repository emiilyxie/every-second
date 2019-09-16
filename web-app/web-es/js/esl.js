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

$("#pill-bottle-button").click(function() {
    $.get("https://us-central1-united-time-251622.cloudfunctions.net/website-call?userID=customer0001&pill_bottle=True",
    function(data, status) {
        console.log("Data: " + data)
        console.log("Status: " + status)
    })
});
