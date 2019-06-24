from django.db import models

from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.

class Appointment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("users.MyUser", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    start = models.DateTimeField(auto_now=False, auto_now_add=False)
    end = models.DateTimeField(auto_now=False, auto_now_add=False)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=250, blank=True)

#    class Meta:
#        verbose_name = _("Appointment")
#        verbose_name_plural = _("s")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
