from google.cloud import datastore

def save_to_store(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    client = datastore.Client() 
    incomplete_key = client.key("every-snap")
    
    entity = datastore.Entity(key=incomplete_key)
    """print("key: " + incomplete_key)"""
    """print("entity: " + entity)"""
    entity.update({
   	    "userID": 101,
        "deviceID": 2,
        "timestamp": 20190908155703,
        "gcsPath": "gs://my-first-bucket-yay123456/file1",
		"labels": "pillBottle, person, food"
    })
    """print("new entity:" + entity)"""
    client.put(entity)
    
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return f'Hello World!'

