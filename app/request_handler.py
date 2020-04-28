import logging


class LunchRequestHandler:

    @staticmethod
    def process_lunch_request(loc: str, mode: str):
        try:
            logging.debug(f'loc={loc}, mode={mode}')
            result = {
                'data': {}    # TODO: get response from places api
            }
            return result
        except Exception as ex:
            logging.error(f'Exception processing request: {ex}')
