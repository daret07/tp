from __future__ import unicode_literals

from django.db import models
from catalogo.models import alumno,categoria,ciclo_escolar
# Create your models here.

escolar=(
  (u'primaria',u'Primaria'),
  (u'secundaria',u'Secundaria'),
  (u'preparatoria',u'Preparatoria'),
  (u'licenciatura',u'Licenciatura'),
  (u'posgrador',u'Pos-Grado'),
)
turnos=(
  (u'matutino',u'Matutino'),
  (u'vespertino',u'Vespertino'),
  (u'sabatino',u'Sabatino'),
)
alumno_plaza=(
  (u'morelia_cefomm',u'Morelia CEFOMM'),
  (u'otra_escuela',u'Otra Escuela'),
)
alumno_rama=(
  (u'varonil',u'Varonil'),
  (u'femenil',u'Femenil'),
)
class inscripcion(models.Model):
  fecha_inscripcion              = models.DateField(auto_now=True)
  alumno                         = models.ForeignKey('catalogo.alumno')
  categoria                      = models.ForeignKey('catalogo.categoria')  
  ciclo                          = models.ForeignKey('catalogo.ciclo_escolar')
  alumno_nombre                  = models.CharField(max_length=50)
  alumno_paterno                 = models.CharField(max_length=50)
  alumno_materno                 = models.CharField(max_length=50)
  alumno_fecha_de_nacimiento     = models.DateField(auto_now=False)
  alumno_lugar_de_nacimiento     = models.CharField(max_length=50)
  alumno_curp                    = models.CharField(max_length=50)
  alumno_matricula               = models.CharField(max_length=50)
  alumno_plaza                   = models.CharField(max_length=50,choices=alumno_plaza)
  alumno_equipo                  = models.IntegerField()
  alumno_rama                    = models.CharField(max_length=50,choices=alumno_rama)
  alumno_calle                   = models.CharField(max_length=100)
  alumno_no                      = models.IntegerField()
  alumno_colonia                 = models.CharField(max_length=100)
  alumno_cp                      = models.IntegerField()
  alumno_poblacion               = models.CharField(max_length=50)
  alumno_municipio               = models.CharField(max_length=50)
  alumno_entidad_federativa      = models.CharField(max_length=50)
  alumno_estatus                 = models.BooleanField(default=True)
  alumno_tel_casa                = models.CharField(max_length=50)
  alumno_tel_calular             = models.CharField(max_length=50)
  alumno_email                   = models.CharField(max_length=50)
  alumno_nombre_colegio          = models.CharField(max_length=100)
  alumno_nivel_educativo         = models.CharField(max_length=50,choices=escolar)
  alumno_turno                   = models.CharField(max_length=50,choices=turnos)
  alumno_grado                   = models.CharField(max_length=10)
  alumno_grupo                   = models.CharField(max_length=10)
  padre_nombre                   = models.CharField(max_length=60)
  padre_paterno                  = models.CharField(max_length=60)
  padre_materno                  = models.CharField(max_length=60)
  padre_lugar_de_nacimiento      = models.CharField(max_length=60)
  padre_curp                     = models.CharField(max_length=60)
  padre_fecha_de_nacimiento      = models.DateField(auto_now=False)
  padre_calle                    = models.CharField(max_length=100)
  padre_numero                   = models.IntegerField(default=0)
  padre_colonia                  = models.CharField(max_length=100)
  padre_cp                       = models.IntegerField(default=0)
  padre_poblacion                = models.CharField(max_length=50)
  padre_municipio                = models.CharField(max_length=50)
  padre_entidad_federativa       = models.CharField(max_length=255)
  padre_telefono_casa            = models.CharField(max_length=255)
  padre_telefono_celular         = models.CharField(max_length=255)
  padre_email                    = models.CharField(max_length=50)
  emergencia_nombre              = models.CharField(max_length=60)
  emergencia_paterno             = models.CharField(max_length=60)
  emergencia_materno             = models.CharField(max_length=60)
  emergencia_lugar_de_nacimiento = models.CharField(max_length=60)
  emergencia_curp                = models.CharField(max_length=60)
  emergencia_fecha_de_nacimiento = models.DateField(auto_now=False)
  emergencia_calle               = models.CharField(max_length=100)
  emergencia_numero              = models.IntegerField(default=0)
  emergencia_colonia             = models.CharField(max_length=100)
  emergencia_cp                  = models.IntegerField(default=0)
  emergencia_poblacion           = models.CharField(max_length=50)
  emergencia_municipio           = models.CharField(max_length=50)
  emergencia_entidad_federativa  = models.CharField(max_length=255)
  emergencia_telefono_casa       = models.CharField(max_length=255)
  emergencia_telefono_celular    = models.CharField(max_length=255)
  emergencia_email               = models.CharField(max_length=50)
  observaciones                  = models.TextField(max_length=255)
  doc_acta                       = models.BooleanField(default=False)
  doc_curp                       = models.BooleanField(default=False)
  doc_fotografias                = models.BooleanField(default=False)
  doc_certificado                = models.BooleanField(default=False)