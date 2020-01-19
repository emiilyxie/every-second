import sys
import json
from google.cloud import storage
from google.cloud import datastore
from google.cloud import automl_v1beta1

'''
Google Cloud Function triggered by images being uploaded to the Google Cloud storage to start object detection, information extraction,
and saving indexes into the Google Cloud Datastore for future search and query events
'''
USER_ID = 'userID'
DEVICE_ID = 'deviceID'
TIMESTAMP = 'timestamp'
GCS_PATH = 'gcsPath'
BOX = 'box'
SCORE = 'score'
PILL_BOTTLE = 'pill_bottle'
FOOD = 'food'
PEOPLE = 'people'

PROJECT_NUMBER = '377104581238'
MODEL_NUMBER = 'IOD2191836847552856064'

DATASTORE_KIND = 'event-snap'

def prediction(data, context):
    '''Background Cloud Function to be triggered by Cloud Storage.
       This function processes an uploaded image in the cloud storage.

    Args:
        data (dict): The Cloud Functions event payload.
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is passed to save_to_store function

    For Debugging Purposes

    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))
    print('Bucket: {}'.format(data['bucket']))
    print('File: {}'.format(data['name']))
    print('Metageneration: {}'.format(data['metageneration']))
    print('Created: {}'.format(data['timeCreated']))
    print('Updated: {}'.format(data['updated']))
    '''
    prediction_client = automl_v1beta1.PredictionServiceClient()
    name = 'projects/{}/locations/us-central1/models/{}'.format(PROJECT_NUMBER, MODEL_NUMBER)
    imagepath = data['bucket'] + "/" + data['name']
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(data['bucket'])
    blob = bucket.blob(data['name'])
    content = blob.download_as_string()

    payload = {'image': {'image_bytes': content}}
    # print(content)

    params = {}
    response = prediction_client.predict(name, payload, params)

    record = {}
    file_path = data['name']
    path_parts = file_path.split('/')
    record[USER_ID] = path_parts[0]
    record[DEVICE_ID] = path_parts[1]
    record[TIMESTAMP] = path_parts[2][:-4]
    record[GCS_PATH] = "gs://" + data['bucket'] + '/' + data['name']
    record[BOX] = ""
    record[SCORE] = 0.0
    record[PILL_BOTTLE] = False
    record[FOOD] = False
    record[PEOPLE] = False

    # print(response)
    for result in response.payload:
        '''
        print("Display Name: {}".format(result.display_name))
        print("Bounding Box: {}".format(result.image_object_detection.bounding_box))
        print("Score: {}".format(result.image_object_detection.score))
        '''
        record[BOX] = "{}".format(result.image_object_detection.bounding_box)
        record[SCORE] = result.image_object_detection.score

        if (PILL_BOTTLE in result.display_name):
            record[PILL_BOTTLE] = True
        if (FOOD in result.display_name):
            record[FOOD] = True
        if ('person' in result.display_name):
            record[PEOPLE] = True
        # return response # waits till request is returned

    save_to_store(record)

def save_to_store(record):
    '''Save record into datastore
    Args:
        record: holds all the processed information of an image
    Returns:
        none
    '''

    client = datastore.Client()
    incomplete_key = client.key(DATASTORE_KIND)

    ''' to save Datastore index size, exclude some properties'''
    entity = datastore.Entity(
                key=incomplete_key,
                exclude_from_indexes=[GCS_PATH,BOX,SCORE])

    ''' need composite index for future query on multiple filters and order'''
    entity.update({
   	    USER_ID: record[USER_ID],
        DEVICE_ID: record[DEVICE_ID],
        TIMESTAMP: record[TIMESTAMP],
        PILL_BOTTLE: record[PILL_BOTTLE],
        FOOD: record[FOOD],
        PEOPLE: record[PEOPLE],
        GCS_PATH: record[GCS_PATH],
        BOX: record[BOX],
        SCORE: record[SCORE]
    })

    client.put(entity)
