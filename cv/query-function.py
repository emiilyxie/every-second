from google.cloud import datastore
from flask import escape
import json
import collections
'''
Google Cloud Function that takes an HTTP request from the web interface,
searches through Google Cloud Datastore for relevant event images,
and formats it as a HTTP response payload
'''
USER_ID = 'userID'
PILL_BOTTLE = 'pill_bottle'
FOOD = 'food'
PEOPLE = 'people'
EVENT_SNAP = 'event-snap'
TIMESTAMP = 'timestamp'
GCS_PATH = 'gcsPath'
EVENT_COUNT = 'eventCount'
EVENT_NAME = 'eventName'
EVENT_MODE = 'eventMode'
EVENTS = 'events'
EVENT_START = 'eventStart'
EVENT_END = 'eventEnd'
IMAGE_PATHS = 'imagePaths'

def query(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    userID = filter_request(request,USER_ID)
    pillBottle = filter_request(request,PILL_BOTTLE)
    food = filter_request(request,FOOD)
    people = filter_request(request,PEOPLE)

    print("userID: " + userID)
    print("pill_bottle: " + pillBottle)

    client = datastore.Client()

    query = client.query(kind=EVENT_SNAP)

    query.add_filter(USER_ID, '=', userID)
    if pillBottle != '':
        bPill = False
        if( pillBottle == "True"):
            bPill = True
        query.add_filter(PILL_BOTTLE, '=', bPill)

    if food != '':
        bFood = False
        if( food == "True"):
            bFood = True
        query.add_filter(FOOD, '=', bFood)

    if people != '':
        bPeople = False
        if( people == "True"):
            bPeople = True
        query.add_filter(PEOPLE, '=', bPeople)

    query.order = [TIMESTAMP]

    ''' reference: https://cloud.google.com/datastore/docs/tools/indexconfig
        need composite indexes:
        - kind: every-snap
        properties:
            - name: pill_bottle
            - name: food
            - name: people
            - name: userID
            - name: timestamp
              direction: asc
    '''

    results = query.fetch()

    hmCountInMinute = {}
    hmImagesInMinute = {}
    rangeThreshold = 10

    '''
    Each image has a timestamp with accuracy to the second.
    We count how many images in each minute.
    '''
    for result in results:
        ts = result[TIMESTAMP]
        key = str(int(int(ts) / 100))
        if(key in hmCountInMinute):
            hmCountInMinute[key] += 1
        else:
            hmCountInMinute[key] = 1

        if(key in hmImagesInMinute):
            hmImagesInMinute[key].append(result[GCS_PATH])
        else:
            hmImagesInMinute[key] = [result[GCS_PATH]]

    orderedKeys = sorted(hmCountInMinute)
    ranges, rangeIndexes = determine_range(orderedKeys)

    json_data = construct_json(pillBottle, food, people, ranges, rangeIndexes, orderedKeys, hmCountInMinute, hmImagesInMinute)
    return (json_data, 200, headers)

def construct_json(pillBottle, food, people, ranges, rangeIndexes, orderedKeys, hmCountInMinute, hmImagesInMinute):
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    data = {}
    eventName = ''
    data[EVENT_COUNT] = len(ranges)
    if(pillBottle != ''):
        eventName = "medicine"
    if(food != ''):
        eventName = FOOD
    if(people != ''):
        eventName = PEOPLE
    data[EVENT_NAME] = eventName
    data[EVENT_MODE] = "today"
    data[EVENTS] = []

    index = 0
    for range in ranges:
        event = {}
        event[EVENT_START] = range[0]
        event[EVENT_END] = range[1]
        '''
        Issues with file access in Google Cloud Storage for the Video library

        event['videopath'] = 'gs://bucket.everysecond.live/customer/1001/query/video-' + eventName + event['eventStart'] + '.mp4'
        generateVideo(event['videopath'], rangeIndexes[index], orderedKeys, hmCountInMinute)
        '''
        event[IMAGE_PATHS] = getImagePaths(rangeIndexes[index], orderedKeys, hmCountInMinute, hmImagesInMinute)
        data[EVENTS].append(event)
        index += 1
    json_data = json.dumps(data)
    return json_data

'''
Among all the images for one particular event, we only pick out a pre-defined number of image paths by sampling with a equal interval
'''
def getImagePaths(rangeIndex, orderedKeys, hmCountInMinute, hmImagesInMinute):
    NUMBER_OF_IMAGES_TO_SHOW = 10
    size = rangeIndex[1] - rangeIndex[0]
    step = size / NUMBER_OF_IMAGES_TO_SHOW
    paths = []
    selectedPaths = []

    for index in range(rangeIndex[0], rangeIndex[1]):
        key = orderedKeys[index]
        paths.extend(hmImagesInMinute[key])

    if len(paths) > NUMBER_OF_IMAGES_TO_SHOW:
        size = len(paths)
        step = size / NUMBER_OF_IMAGES_TO_SHOW
        for i in range(0, NUMBER_OF_IMAGES_TO_SHOW-1):
            tempIndex = int(i*step)
            selectedPaths.append(paths[tempIndex])
    else:
        selectedPaths = paths

    return selectedPaths

'''
This function looks at the HTTP request parameters and picks out the corresponding values
'''
def filter_request(request,request_info):
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json and request_info in request_json:
        data_labels = request_json[request_info]
    elif request_args and request_info in request_args:
        data_labels = request_args[request_info]
    else:
        data_labels = ''
    return data_labels

def distance(key, lastKey):
    return int(key) - int(lastKey)

'''
Based on the ordered images by timestamp, this function determines if those images belong to one or more events.
If there is a time gap between two consecutive images, that gap marks it as a separation of two different events.
'''
def determine_range(orderedKeys):
    ranges = []
    rangeIndexes = []
    starting = ""
    startingIndex = 0
    ending = ""
    endingIndex = 0
    lastKey = ""
    count = 0
    GAP = 10
    for key in orderedKeys:
        if(starting == ""):
            starting = key
            startingIndex = count
            ending = key
        else:
            if(distance(key, lastKey) > GAP):
                ending = lastKey
                endingIndex = count
                range = [starting, ending]
                rangeIndex = [startingIndex, endingIndex]
                rangeIndexes.append(rangeIndex)
                ranges.append(range)
                ''' print('GAP ' + str(range) + ' ' + str(count)) '''
                starting = key
                startingIndex = count

        lastKey = key
        count += 1

        if(count >= len(orderedKeys)):
            ending = key
            range = [starting, ending]
            rangeIndex = [startingIndex, count]
            rangeIndexes.append(rangeIndex)
            ranges.append(range)
            ''' print('Ending ' + str(range)) '''

        ''' look at next key '''
    return ranges, rangeIndexes
