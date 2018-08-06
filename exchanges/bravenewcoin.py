from exchanges.base import Exchange

class BraveNewCoin(Exchange):
    TICKER_URL = ''

    @classmethod
    def init2(self, turl):
        self.TICKER_URL = turl

    def _current_price_extractor(self, data):
        return data['ticker']['bnc_price_index_usd']

    def get_current_bid(self):
        return None

    def get_current_ask(self):
        return None
