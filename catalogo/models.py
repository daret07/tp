from __future__ import unicode_literals
from django.core.validators import MaxValueValidator
from django.db import models
from datetime import datetime 

# Create your views here.

class ciclo_escolar(models.Model):
  clave             = models.CharField(max_length=50)
  descripcion       = models.CharField(max_length=255)
  activo            = models.BooleanField(default=True) 
  def __unicode__(self):
    return  self.clave  

tipo_conceptos=(
  (u'ingreso',u'Ingreso'),
  (u'egreso',u'Egreso'),
)

tipo_cargo=(
  (u'eventual',u'Eventual'),
  (u'automatico',u'Automatico'),
)
class concepto(models.Model):
  clave               = models.CharField(max_length=50)
  nombre              = models.CharField(max_length=50)
  descripcion         = models.TextField(max_length=255)
  tipo                = models.CharField(max_length=20,choices=tipo_conceptos)
  tipo_de_cargo       = models.CharField(max_length=20,choices=tipo_cargo)
  importe             = models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
  formula             = models.CharField(max_length=60,blank=True,null=True)
  def __unicode__(self):
    return self.clave
  class Meta:
    unique_together = ('clave',)

class categoria(models.Model):
  nombre              = models.CharField(max_length=50)
  descripcion         = models.TextField(max_length=255)
  cupo_maximo         = models.IntegerField(validators=[MaxValueValidator(100)])
  estatus             = models.BooleanField(default=True)
  ciclo_escolar       = models.ForeignKey('catalogo.ciclo_escolar')
  def __unicode__(self):
    return self.nombre

tipo_persona=(
  (u'padre',u'Padre'),
  (u'emergencia',u'Emergencia'),
  )


class persona(models.Model):
  nombre              = models.CharField(max_length=60)
  paterno             = models.CharField(max_length=60)
  materno             = models.CharField(max_length=60)
  lugar_de_nacimiento = models.CharField(max_length=60)
  curp                = models.CharField(max_length=60)
  fecha_de_nacimiento = models.DateField(auto_now=False)
  calle               = models.CharField(max_length=100)
  numero              = models.IntegerField(default=0)
  colonia             = models.CharField(max_length=100)
  cp                  = models.IntegerField(default=0)
  poblacion           = models.CharField(max_length=50)
  municipio           = models.CharField(max_length=50)
  entidad_federativa  = models.CharField(max_length=255)
  telefono_casa       = models.CharField(max_length=255)
  telefono_celular    = models.CharField(max_length=255)
  email               = models.EmailField(max_length=50)
  tipo                = models.CharField(max_length=20,choices=tipo_persona)
  def __unicode__(self):
    return self.nombre+'--'+self.telefono_celular
      

alumno_plaza=(
  (u'1',u'Morelia CEFOMM'),
  (u'2',u'Otra Escuela'),
)
alumno_rama=(
  (u'1',u'Varonil'),
  (u'2',u'Femenil'),
)
class alumno(models.Model):
  id                  = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
  fecha_de_ingreso    = models.DateField(auto_now=False,default=datetime.now())
  nombre              = models.CharField(max_length=50)
  paterno             = models.CharField(max_length=50)
  materno             = models.CharField(max_length=50)
  fecha_de_nacimiento = models.DateField(auto_now=False)
  lugar_de_nacimiento = models.CharField(max_length=50)
  matricula           = models.CharField(max_length=50)
  plaza               = models.CharField(max_length=50,choices=alumno_plaza)
  equipo              = models.IntegerField()
  rama                = models.CharField(max_length=50,choices=alumno_rama)
  hermano_institucion = models.BooleanField(default=False,verbose_name='Tiene Hermano En La Institucion')
  padre               = models.ForeignKey('catalogo.persona',related_name='padre')
  emergencia          = models.ForeignKey('catalogo.persona',related_name='emergencia')
  calle               = models.CharField(max_length=100)
  no                  = models.IntegerField()
  colonia             = models.CharField(max_length=100)
  cp                  = models.IntegerField()
  poblacion           = models.CharField(max_length=50)
  municipio           = models.CharField(max_length=50)
  entidad_federativa  = models.CharField(max_length=50)
  estatus             = models.BooleanField(default=True)
  ciclo_escolar       = models.ForeignKey('catalogo.ciclo_escolar')
  def __unicode__(self):
    return self.nombre +' '+ self.paterno +' '+ self.materno +' ---- '+self.matricula

class referencias(models.Model):
  alumno              = models.ForeignKey('catalogo.alumno')
  referencia          = models.CharField(max_length=50)
  descripcion         = models.TextField(max_length=255)
