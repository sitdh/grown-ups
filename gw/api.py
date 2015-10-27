# -*- code: utf-8 -*-

class TwitterCredential:

    def __init__(self):
        pass

    def credential(self, switcher = False):
        if switcher:
            return {
                    'consumer_key': '',
                    'consumer_secret': '',
                    'oauth_token': '',
                    'oauth_token_secret': ''
                    }
        else:
            return {
                    'consumer_key': '',
                    'consumer_secret': '',
                    'oauth_token': '',
                    'oauth_token_secret': ''
                    }
