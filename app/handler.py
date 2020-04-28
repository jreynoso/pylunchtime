import logging
from urllib.parse import parse_qs
from app.request_handler import LunchRequestHandler


def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.debug(f'event={event}')
    logger.debug(f'context={context}')
    request_handler = LunchRequestHandler()
    query_params = get_query_params(event)
    logger.debug(f'query_params={query_params}')
    loc = query_params['loc'][0]
    logger.info(f'loc={loc}')
    mode = query_params['mode'][0]
    logger.info(f'mode={mode}')
    result = request_handler.process_lunch_request(loc, mode)
    logger.debug(f'result={result}')
    data = result['data']
    response = {
        'status': '200',
        'statusDescription': 'OK',
        'headers': {
            'cache-control': [
                {
                    'key': 'Cache-Control',
                    'value': 'max-age=120'
                }
            ],
            'content-type': [
                {
                    'key': 'Content-Type',
                    'value': 'text/json'
                }
            ]
        },
        'body': data
    }
    return response


def get_query_params(event: dict):
    query_params = event['queryStringParameters']
    return parse_qs(query_params)

