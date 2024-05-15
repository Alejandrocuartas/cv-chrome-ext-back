""" lambda handler """

import json
import os
from dotenv import load_dotenv

load_dotenv()

if os.getenv('IS_LAMBDA_ENV'):

    from app.utilities import responses
    from app.controllers import controller
    from app.types.generate_cv import GenerateCVRequest

else:

    from .app.utilities import responses
    from .app.controllers import controller
    from .app.types.generate_cv import GenerateCVRequest

# pylint: disable=unused-argument
def lambda_handler(event: dict[str,str], context): # type: ignore
    """ lambda handler """
    print('event:', event)
    try:

        body: dict[str,str] = json.loads((event["body"]))

        request = GenerateCVRequest(**body)

        res = controller(request)

        return responses.response_ok({
            "message": res
        })

    except json.JSONDecodeError as e:
        return responses.response_error(e)
