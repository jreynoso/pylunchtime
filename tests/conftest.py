import pytest


@pytest.fixture(scope='function')
def lambda_context():
    class Context:
        aws_request_id = '12345'
    return Context()

