from google.cloud import datastore
from flask import escape

def query(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    userID = filter_request(request,'userID')
    pillBottle = filter_request(request,'pill_bottle')
    food = filter_request(request,'food')
    people = filter_request(request,'people')

    print(userID)
    print(pillBottle)

    client = datastore.Client()

    query = client.query(kind='every-snap')
    '''query.add_filter('timestamp', '>', 20190908150000)'''
    query.add_filter('userID', '=', userID)
    if pillBottle != '':
        query.add_filter('pill_bottle', '=', pillBottle)
    if food != '':
        query.add_filter('food', '=', food)
    if people != '':
        query.add_filter('people', '=', people)
    results = query.fetch()
    for result in results:
        print(result)
        print(result['gcsPath'])

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
