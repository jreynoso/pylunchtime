from app.request_handler import LunchRequestHandler


def test_process_request():
    # given
    request_handler = LunchRequestHandler()
    loc = '0,0'
    mode = 'walk'

    # when
    response = request_handler.process_lunch_request(loc, mode)

    # then
    assert response['data'] == {}
