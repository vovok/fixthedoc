from django.db.models.signals import post_save
from django.dispatch import receiver
from ui.models import UploadFiles
from ui.blockchain import add_hash_to_bch


@receiver(post_save, sender=UploadFiles)
def add_hash(instance, **kwargs):
    if kwargs['created']:
        add_hash_to_bch(instance.id)