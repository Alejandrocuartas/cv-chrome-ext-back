# pylint: skip-file

import boto3 # type: ignore
import json
import uuid

def generate_pdf(jsonString: str):
    sqs = boto3.client('sqs', region_name='us-east-1')  # type: ignore

    queue_url = 'https://sqs.us-east-1.amazonaws.com/277469568219/GenerateCvPdf.fifo'

    try:
        response = sqs.send_message( # type: ignore
            QueueUrl=queue_url,
            MessageBody=json.dumps({}),
            MessageAttributes={
                'JSONData': {
                    'StringValue': jsonString,
                    'DataType': 'String'
                },
            },
            MessageGroupId='cv_gen',  # Arbitrary string to group messages
            MessageDeduplicationId=str(uuid.uuid4())  # Unique ID for deduplication (optional)
        )

        print('Message sent successfully:', response['MessageId']) # type: ignore

    except Exception as e:
        print('Error sending message:', e)
