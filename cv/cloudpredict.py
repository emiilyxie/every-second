import sys
import json
from google.cloud import storage
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2


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
    params = {}
    response = prediction_client.predict(name, payload, params)
    # print(response)
    for result in response.payload:
        print("Display Name: {}".format(result.display_name))
        print("Bounding Box: {}".format(result.image_object_detection.bounding_box))
        print("Score: {}".format(result.image_object_detection.score))
        # return response # waits till request is returned
