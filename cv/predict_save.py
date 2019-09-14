import sys
import json
from google.cloud import storage
from google.cloud import datastore
from google.cloud import automl_v1beta1

def prediction(data, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.

    Args:
        data (dict): The Cloud Functions event payload.
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """

    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))
    print('Bucket: {}'.format(data['bucket']))
    print('File: {}'.format(data['name']))
    print('Metageneration: {}'.format(data['metageneration']))
    print('Created: {}'.format(data['timeCreated']))
    print('Updated: {}'.format(data['updated']))

    prediction_client = automl_v1beta1.PredictionServiceClient()
    name = 'projects/{}/locations/us-central1/models/{}'.format('377104581238', 'IOD2191836847552856064')
    imagepath = data['bucket'] + "/" + data['name']
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(data['bucket'])
    blob = bucket.blob(data['name'])
    content = blob.download_as_string()

    payload = {'image': {'image_bytes': content}}
    # print(content)
    """
    params = {}
    response = prediction_client.predict(name, payload, params)
    # print(response)
    for result in response.payload:
        print("Display Name: {}".format(result.display_name))
        print("Bounding Box: {}".format(result.image_object_detection.bounding_box))
        print("Score: {}".format(result.image_object_detection.score))
        # return response # waits till request is returned
    """

    record = {}
    file_path = data['name']
    path_parts = file_path.split('/')
    record['userID'] = path_parts[0]
    record['deviceID'] = path_parts[1]
    record['timestamp'] = path_parts[2][:-4]
    record['gcsPath'] = data['bucket'] + '/' + data['name']
    """record['labels'] = result.display_name"""
    record['labels'] = 'pillBottle'

    save_to_store(record)

def save_to_store(record):
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
   	    "userID": record['userID'],
        "deviceID": record['deviceID'],
        "timestamp": record['timestamp'],
        "gcsPath": record['gcsPath'],
		"labels": record['labels']
    })
    """print("new entity:" + entity)"""
    client.put(entity)
