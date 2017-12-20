from web3 import Web3, IPCProvider
from django.conf import settings
from web3.contract import ConciseContract


def add_hash_to_bch():

    contract_addr = '0x4E8acD9e735FAee1e93Fc4D04ad2494C3D4041b0' #0x98e05684d713B689e65eE235F2f5114130dcB9C6' #'0x3C449Ee4dfedB7E3E1dB8BE32C2e71083cCCE7Db'
    hash_list = UploadFiles.objects.filter(file_bch_trans__isnull=True, file_hash__isnull=False).values('id')
    abi = [{"constant": True, "inputs": [], "name": "getLinesCount",
                     "outputs": [{"name": "", "type": "uint256", "value": "0"}], "payable": False,
                     "stateMutability": "view", "type": "function"},
                    {"constant": True, "inputs": [], "name": "blockInfo",
                     "outputs": [{"name": "", "type": "uint256", "value": "1513705119"},
                                 {"name": "", "type": "uint256", "value": "1442996"}], "payable": False,
                     "stateMutability": "view", "type": "function"},
                    {"constant": False, "inputs": [{"name": "s", "type": "string"}], "name": "addHash", "outputs": [],
                     "payable": False, "stateMutability": "nonpayable", "type": "function"}]

    params = {'from': web3.eth.accounts[0],
              'to': contract_addr,
              'gas': 1000000}

    contract = web3.eth.contract(contract_name='FixTheDoc', abi=abi, address=contract_addr, ContractFactoryClass=ConciseContract)

    for hs in hash_list:
        obj = UploadFiles.objects.get(id=hs['id'])
        file_bch_trans = contract.addHash(str(obj.file_hash), transact=params)
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
    from fixthedoc.wsgi import application
    from ui.models import UploadFiles

    web3 = Web3(IPCProvider())
    web3.personal.unlockAccount(web3.eth.accounts[0], settings.ETH_PWD)
    add_hash_to_bch()
    add_block_info()
