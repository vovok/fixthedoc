from django.db import models


class UploadFiles(models.Model):
    file_name = models.CharField(verbose_name='Название файла', max_length=72)
    file_src = models.FileField(verbose_name='Файл', upload_to='files/')
    file_hash = models.CharField(verbose_name='Хеш файла', max_length=144, null=True, blank=True)
    file_time = models.DateTimeField(verbose_name='Время загрузки файла', auto_now=True)
    file_bch_trans = models.CharField(verbose_name='Транзакция в блокчейне', max_length=144, null=True, blank=True)
    file_bch_block = models.CharField(verbose_name='Блок в блокчейне', max_length=144, null=True, blank=True)
    file_bch_time_block = models.DateTimeField(verbose_name='Время блока в блокчейне', null=True, blank=True)

    class Meta:
        verbose_name = 'Список загруженных файлов'
        verbose_name_plural = 'Список загруженных файлов'
        ordering = ('-file_time', )

    def __str__(self):
        return ('%s: %s') % (self.file_name, self.file_time.strftime('%d.%m.%Y %H:%M:%S'))


