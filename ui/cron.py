from web3 import Web3, IPCProvider, HTTPProvider
from django.conf import settings
from web3.contract import ConciseContract


def add_hash_to_bch():
    contract_addr = '0x360F655Bb3171a4A28fe15787F5e3d92Cc537d70'
    hash_list = UploadFiles.objects.filter(file_bch_trans__isnull=True, file_hash__isnull=False).values('id')
    abi = [{"constant": True, "inputs": [{"name": "", "type": "bytes32"}], "name": "doc_hash",
            "outputs": [{"name": "", "type": "bool"}], "payable": False, "stateMutability": "view", "type": "function"},
           {"constant": False, "inputs": [], "name": "kill", "outputs": [], "payable": False,
            "stateMutability": "nonpayable", "type": "function"},
           {"constant": False, "inputs": [{"name": "s", "type": "bytes32"}], "name": "addHash", "outputs": [],
            "payable": False, "stateMutability": "nonpayable", "type": "function"},
           {"constant": True, "inputs": [], "name": "owner", "outputs": [{"name": "", "type": "address"}],
            "payable": False, "stateMutability": "view", "type": "function"},
           {"constant": True, "inputs": [{"name": "s", "type": "bytes32"}], "name": "checkHash",
            "outputs": [{"name": "", "type": "bool"}], "payable": False, "stateMutability": "view", "type": "function"}]

    params = {'from': web3.eth.accounts[0],
              'to': contract_addr,
              'gas': 1000000}

    contract = web3.eth.contract(contract_name='FixTheDoc', abi=abi, address=contract_addr,
                                 ContractFactoryClass=ConciseContract)

    for hs in hash_list:
        obj = UploadFiles.objects.get(id=hs['id'])
        file_bch_trans = contract.addHash(Web3.toBytes(hexstr=hex(int(obj.file_hash, 16))), transact=params)
        obj.file_bch_trans = file_bch_trans
        obj.save()


def add_block_info():
    from datetime import datetime
    check_list = UploadFiles.objects.filter(file_bch_block__isnull=True).values('id')
    for hs in check_list:
        obj = UploadFiles.objects.get(id=hs['id'])
        trz_obj = web3.eth.getTransaction(obj.file_bch_trans)
        try:
            block_obj = web3.eth.getBlock(trz_obj['blockNumber'])
            if block_obj:
                obj.file_bch_time_block = datetime.fromtimestamp(block_obj['timestamp'])
                obj.file_bch_block = trz_obj['blockNumber']
                obj.save()
        except:
            pass


# Для ручного запуска
if __name__ == '__main__':
    import os
    import sys

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    sys.path.append(os.path.dirname(BASE_DIR))

    from fixthedoc.wsgi import application
    from ui.models import UploadFiles

    # TODO: Set it settings
    try:
        web3 = Web3(IPCProvider())
        web3.personal.unlockAccount(web3.eth.accounts[0], settings.ETH_PWD)
    except:
        web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        web3.personal.unlockAccount(web3.eth.accounts[0], settings.ETH_PWD)


    add_hash_to_bch()
    add_block_info()
