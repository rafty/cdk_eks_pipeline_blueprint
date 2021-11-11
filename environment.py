import os


class Environment:

    def __init__(self):
        self._account_id = os.getenv('CDK_DEFAULT_ACCOUNT')
        self._region = 'ap-northeast-1'

    @property
    def account_id(self) -> str:
        return self._account_id

    @property
    def region(self) -> str:
        return self._region
