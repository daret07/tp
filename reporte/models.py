from __future__ import unicode_literals

from django.db import models
from catalogo.models import alumno,categoria,ciclo_escolar,concepto

# Create your models here.

class movimiento(models.Model):
  fecha_registro          = models.DateField(auto_now=False,blank=True,null=True)
  fecha_captura           = models.DateField(auto_now=True,blank=True,null=True)
  ciclo                   = models.ForeignKey('catalogo.ciclo_escolar',blank=True,null=True,on_delete=models.SET_NULL)  
  alumno                  = models.ForeignKey('catalogo.alumno',blank=True,null=True,on_delete=models.SET_NULL)
  concepto                = models.ForeignKey('catalogo.concepto',blank=True,null=True,on_delete=models.SET_NULL)
  folio                   = models.CharField(max_length=50,blank=True,null=True)
  referencia              = models.CharField(max_length=50,blank=True,null=True)
  monto                   = models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
  archivo                 = models.FileField(blank=True,null=True,upload_to='archivo')
  descripcion             = models.CharField(max_length=50,blank=True,null=True)
  anticipo                = models.BooleanField(default=False)

  class Meta:
    permissions = (
      ('estado_cuenta','Can add estado_cuenta'),
      ('ficha_inscripcion','Can add ficha_inscripcion'),
      ('reporte_referencia','Can add reporte_referencia'),
      ('reporte_saldos','Can add saldo'),
      ('deudores','Can add deudores'),
      )