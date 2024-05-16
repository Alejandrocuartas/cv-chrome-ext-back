""" controllers for the app. """

import boto3 # type: ignore
from .utilities import scrappers
from .types.generate_cv import GenerateCVRequest

s3 = boto3.client('s3') # type: ignore

BUCKET_NAME = 's3-upload-stack-s3uploadbucket-v21uofyootpf'

def controller(request: GenerateCVRequest):
    """ api """

    object_content: str = ''

    try:
        print('getting object from s3')
        response = s3.get_object(Bucket=BUCKET_NAME, Key=request.html_s3_key) # type: ignore
        object_content = response['Body'].read().decode('utf-8') # type: ignore
    except Exception as e: # pylint: disable=broad-except
        msg = f"Error getting object '{request.html_s3_key}' from bucket '{BUCKET_NAME}': {e}"
        print(msg)
        raise RuntimeError(msg) from e

    profile_json = scrappers.extract_data_from_request(object_content) # type: ignore

    print(profile_json)

    return 'success'
