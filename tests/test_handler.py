# pylint: skip-file
import moto
from app import handler


def test_get_request_params():
    # given
    event = TEST_EVENT

    # when
    query_params = handler.get_query_params(event)

    # then
    assert query_params['loc'][0] == '47.6174755835663,-122.2883706665018'
    assert query_params['mode'][0] == 'walk'


@moto.mock_secretsmanager
def test_http_event(aws_credentials, lambda_context):
    # given
    event = TEST_EVENT

    # when
    response = handler.lambda_handler(event, lambda_context)

    # then
    assert response['body'] == {}


TEST_EVENT = {
    'path': '/lunchtime',
    'httpMethod': 'GET',
    'headers': {
        'Accept': '*/*',
        'content-type': 'application/json; charset=UTF-8'
    },
    'queryStringParameters': 'loc=47.6174755835663,-122.2883706665018&mode=walk',
    'pathParameters': 'null',
    'requestContext': {}
}
