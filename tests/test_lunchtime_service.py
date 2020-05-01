# pylint: skip-file
from app.lunchtime_service import LunchtimeService


def test_process_lunch_request(mocker):
    # given
    request_handler = LunchtimeService(get_mock_google_client(mocker))
    loc = '30.266406,-97.7090863'
    mode = 'walk'

    # when
    response = request_handler.process_lunch_request(loc, mode)

    # then
    assert len(response) == 2
    assert response[0].id == '1234'
    assert response[0].name == 'a restaurant'
    assert response[0].imageUrl == 'http://afakeurl.co/img.png'
    assert response[0].address == '1234 Some Place'
    assert response[0].rating == 4
    assert response[1].id == '5678'
    assert response[1].name == 'another restaurant'
    assert response[1].imageUrl == 'http://afakeurl.co/img.png'
    assert response[1].address == '5678 Some Other Place'
    assert response[1].rating == 3.5


def get_mock_google_client(mocker):
    mock_response = {'places_nearby.return_value': TEST_RESPONSE}
    patcher = mocker.patch('googlemaps.Client', **mock_response)
    return patcher


TEST_RESPONSE = {
    'results': [
        {
            'place_id': '1234',
            'name': 'a restaurant',
            'icon': 'http://afakeurl.co/img.png',
            'vicinity': '1234 Some Place',
            'rating': 4
        },
        {
            'place_id': '5678',
            'name': 'another restaurant',
            'icon': 'http://afakeurl.co/img.png',
            'vicinity': '5678 Some Other Place',
            'rating': 3.5
        }
    ]
}

