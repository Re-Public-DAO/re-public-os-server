from django.db import models
from republic_os.utils.models import RePublicModel


class Event(RePublicModel):
    code = models.CharField(max_length=255)
    actor = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)

    def __str__(self):
        return self.code
