from google.cloud import datastore
from flask import escape
import json
import collections

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

    userID = filter_request(request,'userID')
    pillBottle = filter_request(request,'pill_bottle')
    food = filter_request(request,'food')
    people = filter_request(request,'people')

    print("userID: " + userID)
    print("pill_bottle: " + pillBottle)

    client = datastore.Client()

    query = client.query(kind='event-snap')

    '''query.projection = ['timestamp', 'gcsPath']'''
    '''query.add_filter('timestamp', '>', '20190908150000')'''

    query.add_filter('userID', '=', userID)
    if pillBottle != '':
        bPill = False
        if( pillBottle == "True"):
            bPill = True
        query.add_filter('pill_bottle', '=', bPill)

    if food != '':
        bFood = False
        if( food == "True"):
            bFood = True
        query.add_filter('food', '=', bFood)

    if people != '':
        bPeople = False
        if( people == "True"):
            bPeople = True
        query.add_filter('people', '=', bPeople)

    query.order = ['timestamp']

    ''' reference: https://cloud.google.com/datastore/docs/tools/indexconfig
    recommended index is:
        indexes:

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

    for result in results:
        print(result)
        print(result['gcsPath'])
        ts = result['timestamp']
        key = str(int(int(ts) / 100))
        if(key in hmCountInMinute):
            hmCountInMinute[key] += 1
        else:
            hmCountInMinute[key] = 1

        if(key in hmImagesInMinute):
            hmImagesInMinute[key].append(result['gcsPath'])
        else:
            hmImagesInMinute[key] = [result['gcsPath']]

    print(hmImagesInMinute)
    print(hmCountInMinute)

    orderedKeys = sorted(hmCountInMinute)
    print(orderedKeys)

    ranges, rangeIndexes = determine_range(orderedKeys)
    print(ranges)
    json_data = construct_json(pillBottle, food, people, ranges, rangeIndexes, orderedKeys, hmCountInMinute, hmImagesInMinute)
    return (json_data, 200, headers)

def construct_json(pillBottle, food, people, ranges, rangeIndexes, orderedKeys, hmCountInMinute, hmImagesInMinute):
    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    data = {}
    eventName = ''
    data['eventCount'] = len(ranges)
    if(pillBottle != ''):
        eventName = "medicine"
    if(food != ''):
        eventName = "food"
    if(people != ''):
        eventName = "people"
    data['eventName'] = eventName
    data['eventMode'] = "today"
    data["events"] = []

    index = 0
    for range in ranges:
        event = {}
        event['eventStart'] = range[0]
        event['eventEnd'] = range[1]
        event['videopath'] = 'gs://bucket.everysecond.live/customer/1001/query/video-' + eventName + event['eventStart'] + '.mp4'
        '''generateVideo(event['videopath'], rangeIndexes[index], orderedKeys, hmCountInMinute)'''
        event['imagePaths'] = getImagePaths(rangeIndexes[index], orderedKeys, hmCountInMinute, hmImagesInMinute)
        data['events'].append(event)
        index += 1
    json_data = json.dumps(data)
    return json_data

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
                print('GAP ' + str(range) + ' ' + str(count))
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
            print('Ending ' + str(range))

        ''' look at next key '''
    return ranges, rangeIndexes
