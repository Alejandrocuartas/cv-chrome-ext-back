""" testing """

import json
from .lambda_function import lambda_handler # type: ignore

def test_lambda_handler_():
    """ a big profile """

    event = {
            "body": json.dumps(
                {
                    "html_s3_key": "Juan_Manuel_Aizama.html",
                }
            )
        }

    res = lambda_handler(event, {}) # type: ignore
    assert res.get('statusCode') == 200
