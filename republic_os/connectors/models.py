from django.db import models
from django.core.exceptions import ValidationError

from republic_os.utils.models import RePublicModel


def validate_file_extension(value):
    import os
    from django.utils.deconstruct import deconstructible

    @deconstructible
    class ValidateFileExtension(object):
        extensions = ['svg']

        def __init__(self, extensions):
            self.extensions = [i.lower() for i in extensions]

        def __call__(self, value):
            ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
            if not ext.lower() in self.extensions:
                raise ValidationError(u'Unsupported file extension.')


# Tracks the install and status of a connector
class Connector(RePublicModel):
    name = models.CharField(max_length=255)
    republic_id = models.CharField(max_length=255, unique=True)
    is_installed = models.BooleanField(default=False)
    version_number = models.CharField(max_length=10, null=True, blank=True)
    build_number = models.CharField(max_length=20, null=True, blank=True)
    repo_url = models.URLField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='connectors', null=True, blank=True)
    svg = models.FileField(upload_to='connectors', null=True, blank=True, validators=[validate_file_extension])
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class ConnectorSync(RePublicModel):

    status = models.CharField(max_length=255, null=True)
    error = models.CharField(max_length=255, null=True)
    task_id = models.CharField(max_length=255, null=True)
    completed_at = models.DateTimeField(null=True)

    oauth_state = models.ForeignKey('oauth.OAuthState', on_delete=models.DO_NOTHING, null=True)
    connector = models.ForeignKey('connectors.Connector', on_delete=models.DO_NOTHING, null=True, related_name='syncs')

    def __str__(self):
        return f'ConnectorSync: {self.id}'


class RawFileIngest(RePublicModel):

    status = models.CharField(max_length=255, null=True)
    error = models.CharField(max_length=255, null=True)
    completed_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.status