from __future__ import unicode_literals

from django.db import models
from catalogo.models import alumno,categoria,ciclo_escolar,concepto

# Create your models here.

class movimiento(models.Model):
	fecha_registro 					= models.DateField(auto_now=False)
	fecha_captura 					= models.DateField(auto_now=False)
	ciclo 									= models.ForeignKey('catalogo.ciclo_escolar')  
	alumno 									= models.ForeignKey('catalogo.alumno')
	concepto 								= models.ForeignKey('catalogo.concepto')
	folio 									= models.CharField(max_length=50)
	referencia 							= models.CharField(max_length=50)
	monto 									= models.DecimalField(max_digits=6,decimal_places=2)