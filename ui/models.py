from django.db import models
from django.forms import ModelForm
import hashlib


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


class FormUploadFiles(ModelForm):
    class Meta:
        model = UploadFiles
        fields = ['file_name', 'file_src', 'file_hash']

    def clean(self):
        cleaned_data = super().clean()
        file_src = cleaned_data.get("file_src")
        if file_src:
            file = file_src.file.read()
            cleaned_data['file_hash'] = hashlib.sha1(file).hexdigest()
            if UploadFiles.objects.filter(file_hash=cleaned_data['file_hash']):
                self.add_error('file_hash', 'Файл с данным хешем был загружен ранее.')