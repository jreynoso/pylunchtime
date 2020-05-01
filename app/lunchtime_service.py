import logging
from googlemaps import Client
from app.lunch_option import LunchOption


class LunchtimeService:

    def __init__(self, client: Client):
        self.client = client

    def process_lunch_request(self, loc: str, mode: str):
        try:
            logging.debug(f'loc={loc}, mode={mode}')
            data = self.client.places_nearby(
                location=self.get_location(loc),
                radius=self.get_radius(mode),
                language='en-US',
                min_price=1,
                max_price=4,
                open_now=True,
                rank_by='prominence',
                type='restaurant',
            )
            results = data['results']
            return list(map(self.map_result_to_lunch_option, results))
        except Exception as ex:
            logging.error(f'Exception processing request: {ex}')

    @staticmethod
    def get_location(loc: str):
        lat_long = loc.split(',')
        return float(lat_long[0]), float(lat_long[1])

    @staticmethod
    def get_radius(mode: str):
        radii = {
            'walk': 1000,
            'scoot': 3000,
            'drive': 10000
        }
        return radii[mode]

    @staticmethod
    def map_result_to_lunch_option(result: dict):
        return LunchOption(
            id=result['place_id'],
            name=result['name'],
            image_url=result['icon'],
            address=result['vicinity'],
            rating=result['rating'],
        )

