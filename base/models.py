from django.db import models

class ejemplo(models.Model):
    campo   = models.CharField(max_length=20)
    campos2 = models.CharField(max_length=20)
    jorge   = models.CharField(max_length=20)

    def __unicode__(self):
        return "Ejemplo"
