'''from google.cloud import datastore'''
'''from flask import escape'''
import collections

def query():
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    '''
    userID = filter_request(request,'userID')
    pillBottle = filter_request(request,'pill_bottle')
    food = filter_request(request,'food')
    people = filter_request(request,'people')

    print(userID)
    print(pillBottle)

    client = datastore.Client()

    query = client.query(kind='every-snap')
    query.add_filter('timestamp', '>', 20190908150000)
    query.add_filter('userID', '=', userID)
    if pillBottle != '':
        query.add_filter('pill_bottle', '=', pillBottle)
    if food != '':
        query.add_filter('food', '=', food)
    if people != '':
        query.add_filter('people', '=', people)
    results = query.fetch()
    '''
    hashmap = {'20190920132012':'path/image001.jpg', '20190920132015':'path/image002.jpg','20190920132017':'path/image002.jpg','20190920132025':'path/image002.jpg','20190921132025':'path/image002.jpg','20190921132125':'path/image1232.jpg','20190920132056':'path/image002.jpg', '20190920132112':'path/image001.jpg'}
    newhashmap = {}
    rangehashmap = {}
    rangeThreshold = 10
    '''
    for result in results:
        print(result)
        print(result['gcsPath'])
        ts = result['timestamp']
        key = str(int(int(ts) / 100))
        hashmap[key] = 1
    '''
    for result in hashmap:
        key = str(int(int(result) / 100))
        if(newhashmap.get(key) >= 1):
            newhashmap[key] += 1
        else:
            newhashmap[key] = 1
    '''
    hashmaplist = list(newhashmap.keys())
    for result in hashmaplist:
        if(hashmaplist[result+1] - hashmaplist[result] < rangeThreshold):
            '''
    print(newhashmap)
    orderedKeys = sorted(newhashmap)
    print(orderedKeys)
    print(determine_range(orderedKeys))


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
    starting = ""
    ending = ""
    lastKey = ""
    count = 0
    GAP = 10
    for key in orderedKeys:
        count += 1
        if(starting == ""):
            starting = key
            ending = key
        else:
            if(distance(key, lastKey)> GAP):
                ending = lastKey
                range = [starting, ending]
                ranges.append(range)
                print('GAP ' + str(range) + ' ' + str(count))
                starting = key

            if(count >= len(orderedKeys)):
                ending = key
                range = [starting, ending]
                ranges.append(range)
                print('Ending ' + str(range))

        lastKey = key
        ''' look at next key '''
    return ranges


query()
