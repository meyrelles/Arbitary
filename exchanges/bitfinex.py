from exchanges.base import Exchange



class Bitfinex(Exchange):

    TICKER_URL = ''

    @classmethod
    def init2(self, turl):
        self.TICKER_URL = turl    

    @classmethod
    def _current_price_extractor(cls, data):
        return data.get('last_price')

    @classmethod
    def _current_bid_extractor(cls, data):
        return data.get('bid')

    @classmethod
    def _current_ask_extractor(cls, data):
        return data.get('ask')
