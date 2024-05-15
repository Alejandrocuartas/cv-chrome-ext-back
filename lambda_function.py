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

    except KeyError as e:
        message = "My Error. Please reach out to me."
        return responses.response_error(e, message, 502)

    except TypeError as e:
        message = "Bad Request. Please check the request body."
        return responses.response_error(e, message, 400)

    except Exception as e: # pylint: disable=broad-except
        message = "Unexpected error. Please reach out to me."
        return responses.response_error(e, message, 500)
