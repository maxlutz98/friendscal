from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

import uuid

# Create your models here.

class Appointment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Nutzer'))
    title = models.CharField(_('Titel'), max_length=250)
    start = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name=_('Anfang'))
    end = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name=_('Ende'))
    description = models.TextField(_('Beschreibung'), blank=True)
    location = models.CharField(_('Ort'), max_length=250, blank=True)

#    class Meta:
#        verbose_name = _("Appointment")
#        verbose_name_plural = _("s")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('friendscal:appointment-detail', kwargs={"pk": self.pk})
