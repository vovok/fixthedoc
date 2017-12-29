from django.apps import AppConfig
from web3 import Web3, IPCProvider
from django.conf import settings


class UiConfig(AppConfig):
    name = 'ui'
    verbose_name = 'Пользовательский интерфейс'

    def ready(self):
        self.web3 = self.eth()
        import ui.signals

    def eth(self):
        eth_acc_id = 0
        eth_pwd = settings.ETHEREUM_ACCOUNTS[eth_acc_id]

        try:
            web3 = Web3(IPCProvider())
            acc_obj = web3.eth.accounts[eth_acc_id]
            web3.personal.unlockAccount(acc_obj, eth_pwd)
        except:
            web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
            acc_obj = web3.eth.accounts[eth_acc_id]
            web3.personal.unlockAccount(acc_obj, eth_pwd)
        return web3