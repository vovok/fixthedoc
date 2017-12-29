from web3.contract import ConciseContract
from django.apps import apps
from django.conf import settings
from ui.models import UploadFiles
from web3 import Web3


def add_hash_to_bch(file_id):
    web3 = apps.get_app_config('ui').web3
    contract_params = settings.ETHEREUM_CONTRACTS[0]

    params = {'from': web3.eth.accounts[0],
              'to': contract_params['address'],
              'gas': 1000000}

    contract = web3.eth.contract(contract_name='FixTheDoc',
                                 abi=contract_params['abi'],
                                 address=contract_params['address'],
                                 ContractFactoryClass=ConciseContract)

    obj = UploadFiles.objects.get(id=file_id)
    file_bch_trans = contract.addHash(Web3.toBytes(hexstr=hex(int(obj.file_hash, 16))), transact=params)
    obj.file_bch_trans = file_bch_trans
    obj.save()


def check_hash_from_bch(hash):
    web3 = apps.get_app_config('ui').web3
    contract_params = settings.ETHEREUM_CONTRACTS[0]
    contract = web3.eth.contract(contract_name='FixTheDoc',
                                 abi=contract_params['abi'],
                                 address=contract_params['address'],
                                 ContractFactoryClass=ConciseContract)

    res = contract.checkHash(Web3.toBytes(hexstr=hex(int(hash, 16))))
    return res
