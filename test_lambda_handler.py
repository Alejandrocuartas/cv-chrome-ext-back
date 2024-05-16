""" testing """

import json
from .lambda_function import lambda_handler # type: ignore

def test_lambda_handler_():
    """ a big profile """

    event = {
            "body": json.dumps(
                {
                    # "html_s3_key": "1087653.html",
                    "html_s3_key": "4467640.html",
                }
            )
        }

    res = lambda_handler(event, {}) # type: ignore
    print(res)
    assert res.get('statusCode') == 200
