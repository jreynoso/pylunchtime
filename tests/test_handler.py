# pylint: skip-file
import json
from app import handler
from app.lunch_option import LunchOption


def test_get_request_params():
    # given
    event = TEST_EVENT

    # when
    query_params = handler.get_query_params(event)

    # then
    assert query_params['loc'] == '47.6174755835663,-122.2883706665018'
    assert query_params['mode'] == 'walk'


def test_http_event(lambda_context, mocker):
    # given
    mock_lunchtime_serivce = mocker.patch.object(handler, 'LunchtimeService')
    handler.LunchtimeService.process_lunch_request.return_value = TEST_RESPONSE
    mocker.patch.object(handler, 'get_lunchtime_service')
    handler.get_lunchtime_service.return_value = mock_lunchtime_serivce
    event = TEST_EVENT

    # when
    response = handler.lambda_handler(event, lambda_context)

    # then
    body = response['body']
    assert body is not None
    data = json.loads(body)
    assert data['suggestion'] is not None
    assert data['options'] is not None
    criteria = data['criteria']
    assert criteria is not None
    assert criteria['loc'] == '47.6174755835663,-122.2883706665018'
    assert criteria['mode'] == 'walk'


TEST_RESPONSE = [
    LunchOption(
        id='1234',
        name='a restaurant',
        image_url='http://afakeurl.co/img.png',
        address='1234 Some Place',
        rating=4
    ),
    LunchOption(
        id='5678',
        name='another restaurant',
        image_url='http://afakeurl.co/img.png',
        address='5678 Some Other Place',
        rating=3.5
    )
]


TEST_EVENT = {
    'path': '/lunchtime',
    'httpMethod': 'GET',
    'headers': {
        'Accept': '*/*',
        'content-type': 'application/json; charset=UTF-8'
    },
    'queryStringParameters': {
        'loc': '47.6174755835663,-122.2883706665018',
        'mode': 'walk'
    },
    'pathParameters': 'null',
    'requestContext': {}
}
