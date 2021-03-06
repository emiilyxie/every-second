// client side javascript file to handle queries and responses for the example page

var STORAGE_BASE = 'https://storage.googleapis.com/';
var QUERY_ENDPOINT = 'https://us-central1-united-time-251622.cloudfunctions.net/query-function'

$("#pill-bottle-button").click(function() {
    $.get(QUERY_ENDPOINT + "?userID=customer0001&pill_bottle=True",
    function(data, status) {
        // console.log("Data: " + data);
        // console.log("Status: " + status);
        parseResponse(data);
    });
});

$("#food-button").click(function() {
    $.get(QUERY_ENDPOINT + "?userID=customer0001&food=True",
    function(data, status) {
        // console.log("Data: " + data);
        // console.log("Status: " + status);
        parseResponse(data);
    });
});

$("#people-button").click(function() {
    $.get(QUERY_ENDPOINT + "?userID=customer0001&people=True",
    function(data, status) {
        // console.log("Data: " + data);
        // console.log("Status: " + status);
        parseResponse(data);
    });
});

// creates an HTML carousel object with the images from the function
var displayImgs = function(data,number) {

    var respSect = document.getElementById('response-section');
    var count = 0;
    var sectionId = "myCarousel" + count + number;

    let paths = data;
    paths.forEach(function(path) {
        var newPath = "";
        if (path.startsWith('gs://')) {
            newPath = path.replace('gs://', STORAGE_BASE)
        }
        else {
            newPath = STORAGE_BASE + path;
        }

        if (count == 0) {
            console.log(sectionId);
            respSect.innerHTML += '<div id="' + sectionId + '" class="carousel slide" data-ride="carousel">';

            var indicatorList = document.createElement('ol');
            indicatorList.setAttribute('class', 'carousel-indicators');
            indicatorList.setAttribute('id', sectionId + "-indicators");
            document.getElementById(sectionId).append(indicatorList);

            var carouselInner = document.createElement('div');
            carouselInner.setAttribute('class','carousel-inner');
            carouselInner.setAttribute('id', sectionId+'-inner');
            document.getElementById(sectionId).append(carouselInner);

            var leftControl = document.createElement('a');
            leftControl.setAttribute('class','left carousel-control');
            leftControl.setAttribute('href', "#" + sectionId);
            leftControl.setAttribute('data-slide', 'prev');
            leftControl.innerHTML += '<span class="glyphicon glyphicon-chevron-left"></span><span class="sr-only">Previous</span>';
            document.getElementById(sectionId).append(leftControl);

            var rightControl = document.createElement('a');
            rightControl.setAttribute('class','right carousel-control');
            rightControl.setAttribute('href', "#" + sectionId);
            rightControl.setAttribute('data-slide', 'next');
            rightControl.innerHTML += '<span class="glyphicon glyphicon-chevron-right"></span><span class="sr-only">Previous</span>';
            document.getElementById(sectionId).append(rightControl);
        }

        var indicator = document.createElement('li');
        indicator.setAttribute("data-target", "#" + sectionId);
        indicator.setAttribute("data-slide-to", count.toString());
        if (count == 0){
            indicator.setAttribute("class", "active");
        }
        // console.log('indicator');
        document.getElementById(sectionId + "-indicators").append(indicator);

        var img = document.createElement('img');
        img.setAttribute("src", newPath);
        var item = document.createElement('div');
        item.setAttribute("class", "item");
        if (count == 0){
            item.setAttribute("class", "item active");
        }
        item.append(img);
        document.getElementById(sectionId + '-inner').append(item);

        count++;
    });
}

var parseResponse = function(response) {
    var respJson = JSON.parse(response);
    var respSect = document.getElementById('response-section');
    respSect.querySelectorAll('*').forEach(n => n.remove());
    var summaryHeading = document.createElement("h1");
    var message = "Here are the last " + respJson.eventCount + " times you've ";
    if (respJson.eventName == "medicine") {
        message = message + "taken medicine";
    }
    else if (respJson.eventName == "food") {
        message = message + "had a meal";
    }
    else {
        message = message + "met with people";
    }
    summaryHeading.innerHTML = message;
    respSect.append(summaryHeading);
    for (var i = respJson.events.length-1; i >= 0; i--) {
        var count = respJson.events.length-i;
        var eventHeading = document.createElement('h2');
        eventHeading.innerHTML += count + ". " + "At time " + tsToTime(respJson.events[i].eventStart);
        respSect.append(eventHeading);
        // console.log("image paths: " + respJson.events[i].imagePaths);
        // console.log("video path: " + respJson.events[i].videopath);
        let imgs = respJson.events[i].imagePaths;
        displayImgs(imgs,i);
    }
    respSect.scrollIntoView({behavior: "smooth", block: "start", inline: "nearest"});

}

var capitalize = function(s) {
    if (typeof s !== 'string') return '';
    return s.charAt(0).toUpperCase() + s.slice(1);
}

var tsToTime = function(ts) {
    var year = ts.slice(0,4);
    var month = ts.slice(4,6);
    var day = ts.slice(6,8);
    var hr = ts.slice(8,10);
    var min = ts.slice(10,12);
    return month + "/" + day + ", " + hr + ":" + min;
}

var parseEvent = function(ev) {
    var respSect = document.getElementById('response-section');
    respSect.innerHTML += "Started: " + ev.eventStart;
}

// for local testing purposes
var esTestJson =
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
