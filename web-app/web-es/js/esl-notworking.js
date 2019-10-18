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
    console.log("clicked on pill bottle");

    $.get("https://us-central1-united-time-251622.cloudfunctions.net/website-call?userID=customer0001&pill_bottle=True",
    function(data, status) {
        console.log("Data: " + data);
        console.log("Status: " + status);
        //displayImgs(data);
        parseResponse(JSON.stringify(testJSON));
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

    document.getElementById('myCarousel-indicators').querySelectorAll('*').forEach(n => n.remove());
    document.getElementById('myCarousel-inner').querySelectorAll('*').forEach(n => n.remove());
    var count = 0;

    let paths = data;
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
        var item = document.createElement('div');
        item.setAttribute("class", "item");
        item.append(img);
        document.getElementById('myCarousel-inner').append(item);

        var indicator = document.createElement('li');
        indicator.setAttribute("data-target", "#myCarousel");
        indicator.setAttribute("data-slide-to", count.toString());
        if (count == 0){
            indicator.setAttribute("class", "active");
        }
        count++;
    });
}

var parseResponse = function(response) {
    var respJson = JSON.parse(response);
    document.getElementById('response-section').querySelectorAll('*').forEach(n => n.remove());
    document.getElementById("response-section").innerHTML = respJson.eventMode + " you saw " + respJson.event + respJson.eventCount + "times.";
    let imgs = respJson.events[0].imagePaths;
    //displayImgs(imgs);
}

var testJSON =
{
	"eventCount": 2,
	"event": "food",
	"eventMode": "today",
	"events": [
	{
		"eventStart": "20190922191518",
		"eventEnd": "20190922191525",
		"videoPath": "gs://my-first-bucket-yay123456/20190922_food/20190922191518.mp4",
		"imagePaths": ["gs://my-first-bucket-yay123456/20190922_food/20190922191518.jpg",
         "gs://my-first-bucket-yay123456/20190922_food/20190922191519.jpg",
         "gs://my-first-bucket-yay123456/20190922_food/20190922191525.jpg"]
    },
    {
		"eventStart": "20190922191532",
		"eventEnd": "20190922191538",
		"videoPath": "gs://my-first-bucket-yay123456/20190922_food/20190922191518.mp4",
		"imagePaths": ["gs://my-first-bucket-yay123456/20190922_food/20190922191532.jpg",
         "gs://my-first-bucket-yay123456/20190922_food/20190922191534.jpg",
         "gs://my-first-bucket-yay123456/20190922_food/2019092219152538.jpg"]
    },
    ]
};
