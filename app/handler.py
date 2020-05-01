import googlemaps
import json
import logging
import os
import random
from app.lunchtime_service import LunchtimeService
from app.lunch_option import LunchOption


def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.debug(f'event={event}')
    logger.debug(f'context={context}')

    query_params = get_query_params(event)
    loc = query_params['loc']
    mode = query_params['mode']
    logger.debug(f'loc={loc}')
    logger.debug(f'mode={mode}')

    result = get_lunchtime_service().process_lunch_request(loc, mode)
    response_body = get_response_body(loc, mode, result)
    logger.debug(f'response_body={response_body}')

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': 'https://lunchtime.dispassionproject.com'
        },
        'body': json.dumps(response_body),
    }


def get_query_params(event: dict):
    return event['queryStringParameters']


def get_response_body(loc: str, mode: str, results: list):
    num_results = len(results)
    suggestion = None
    if num_results > 0:
        suggestion_idx = random.randint(0, num_results-1)
        suggestion = lunch_option_to_dict(results.pop(suggestion_idx))
    options = list(map(lunch_option_to_dict, results))
    body = {
        'criteria': {
            'loc': loc,
            'mode': mode,
        },
        'options': options,
        'suggestion': suggestion,
    }
    return {k: v for k, v in body.items() if v is not None}


def lunch_option_to_dict(lunch_option: LunchOption):
    return lunch_option.__dict__


def get_lunchtime_service():
    google_api_key = os.environ['API_TOKEN']
    client = googlemaps.Client(google_api_key)
    return LunchtimeService(client)
