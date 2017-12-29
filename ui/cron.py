from django.apps import apps

def add_block_info(web3):
    from ui.models import UploadFiles
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


def cron_run():
    web3 = apps.get_app_config('ui').web3
    add_block_info(web3)


# Для ручного запуска
if __name__ == '__main__':

    # Routing snippet
    import os
    import sys
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    sys.path.append(os.path.dirname(BASE_DIR))

    # Django snippet ecosystem loader
    from fixthedoc.wsgi import application

    cron_run()

