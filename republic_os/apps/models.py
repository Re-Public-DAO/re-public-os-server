import os
from django.db import models
from django.core.exceptions import ValidationError
from republic_os.utils.models import RePublicModel


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.jpeg', '.png', '.svg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class App(RePublicModel):

    app_name = models.CharField(max_length=255)
    app_store_id = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    single_install = models.BooleanField(default=True)
    price_usd = models.FloatField(null=True)
    image = models.ImageField(null=True, validators=[validate_file_extension])
    interface_url_web = models.CharField(max_length=255, null=True)
    interface_url_mobile = models.CharField(max_length=255, null=True)
    interface_url_desktop = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.app_name


class AppInstall(RePublicModel):

    status = models.CharField(max_length=255)
    app_store_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.app_store_id
