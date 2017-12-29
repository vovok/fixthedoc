from django.forms import ModelForm
import hashlib
from .models import UploadFiles
from .blockchain import add_hash_to_bch, check_hash_from_bch


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
            if UploadFiles.objects.filter(file_hash=cleaned_data['file_hash']) or check_hash_from_bch(cleaned_data['file_hash']):
                self.add_error('file_hash', 'Файл с данным хешем был загружен ранее.')
            if file_src.size > 1048576:
                self.add_error('file_src', 'Файл слишком большой.')