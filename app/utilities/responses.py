""" define the responses for the lambda functions """

import json

def response_ok(body: dict[str,str]):
    """ return a 200 response"""
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Content-Type': 'application/json'
        },
        'body': body
    }


def response_error(error: Exception):
    """ return a 500 response """

    body = json.dumps({
            'error': str(error)
        })

    return {
        'statusCode': 500,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Content-Type': 'application/json'
        },
        'body': body
    }
