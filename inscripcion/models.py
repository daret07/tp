# -*- coding: utf-8 -*-
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
  (u'1',u'Matutino'),
  (u'2',u'Vespertino'),
  (u'3',u'Sabatino'),
)
alumno_plaza=(
  (u'1',u'Morelia CEFOMM'),
  (u'2',u'Otra Escuela'),
)
alumno_rama=(
  (u'1',u'Varonil'),
  (u'2',u'Femenil'),
)
class inscripcion(models.Model):
  fecha_inscripcion              = models.DateField(auto_now=True)
  alumno                         = models.ForeignKey('catalogo.alumno',blank=True,null=True,on_delete=models.SET_NULL)
  categoria                      = models.ForeignKey('catalogo.categoria',blank=True,null=True,on_delete=models.SET_NULL)
  ciclo                          = models.ForeignKey('catalogo.ciclo_escolar',blank=True,null=True,on_delete=models.SET_NULL)
  alumno_nombre                  = models.CharField(max_length=50,verbose_name='Nombre')
  alumno_paterno                 = models.CharField(max_length=50,verbose_name='Apellido Paterno')
  alumno_materno                 = models.CharField(max_length=50,verbose_name='Apellido Materno')
  alumno_fecha_de_nacimiento     = models.DateField(auto_now=False,verbose_name='Fecha Nacimiento')
  alumno_lugar_de_nacimiento     = models.CharField(max_length=50,verbose_name='Lugar de Nacimiento')
  alumno_curp                    = models.CharField(max_length=50,verbose_name='Curp')
  alumno_matricula               = models.CharField(max_length=50,verbose_name='Matricula')
  alumno_plaza                   = models.CharField(max_length=50,choices=alumno_plaza,verbose_name='Plaza')
  alumno_equipo                  = models.IntegerField(verbose_name='Equipo')
  alumno_rama                    = models.CharField(max_length=50,choices=alumno_rama,verbose_name='Rama')
  alumno_calle                   = models.CharField(max_length=100,verbose_name='Calle')
  alumno_no                      = models.CharField(max_length=20,verbose_name='Numero')
  alumno_colonia                 = models.CharField(max_length=100,verbose_name='Colonia')
  alumno_cp                      = models.IntegerField(verbose_name='Codigo Postal')
  alumno_poblacion               = models.CharField(max_length=50,verbose_name='Población')
  alumno_municipio               = models.CharField(max_length=50,verbose_name='Municipio')
  alumno_entidad_federativa      = models.CharField(max_length=50,verbose_name='Entidad Federativa')
  alumno_tel_casa                = models.CharField(max_length=50,verbose_name='Telefono de Casa')
  alumno_tel_celular             = models.CharField(max_length=50,verbose_name='Telefono Celular')
  alumno_email                   = models.CharField(max_length=50,verbose_name='Email')
  alumno_nombre_colegio          = models.CharField(max_length=100,verbose_name='Nombre Colegio')
  alumno_nivel_educativo         = models.CharField(max_length=50,choices=escolar,verbose_name='Nivel Educativo')
  alumno_turno                   = models.CharField(max_length=50,choices=turnos,verbose_name='Turno')
  alumno_grado                   = models.CharField(max_length=10,verbose_name='Grado')
  alumno_grupo                   = models.CharField(max_length=10,verbose_name='Grupo')
  padre_nombre                   = models.CharField(max_length=60,verbose_name='Nombre')
  padre_paterno                  = models.CharField(max_length=60,verbose_name='Apellido Paterno')
  padre_materno                  = models.CharField(max_length=60,verbose_name='Apellido Materno')
  padre_lugar_de_nacimiento      = models.CharField(max_length=60,verbose_name='Lugar de Nacimiento')
  padre_curp                     = models.CharField(max_length=60,verbose_name='Curp')
  padre_fecha_de_nacimiento      = models.DateField(auto_now=False,verbose_name='Fecha de Nacimiento')
  padre_calle                    = models.CharField(max_length=100,verbose_name='Calle')
  padre_numero                   = models.CharField(max_length=20,verbose_name='Numero')
  padre_colonia                  = models.CharField(max_length=100,verbose_name='Colonia')
  padre_cp                       = models.IntegerField(default=0,verbose_name='Codigo Postal')
  padre_poblacion                = models.CharField(max_length=50,verbose_name='Población')
  padre_municipio                = models.CharField(max_length=50,verbose_name='Municipio')
  padre_entidad_federativa       = models.CharField(max_length=255,verbose_name='Entidad Federativa')
  padre_telefono_casa            = models.CharField(max_length=255,verbose_name='Telefono de Casa')
  padre_telefono_celular         = models.CharField(max_length=255,verbose_name='Telefono Celular')
  padre_email                    = models.CharField(max_length=50,verbose_name='Email')
  emergencia_nombre              = models.CharField(max_length=60,verbose_name='Nombre')
  emergencia_paterno             = models.CharField(max_length=60,verbose_name='Apellido Paterno')
  emergencia_materno             = models.CharField(max_length=60,verbose_name='Apellido Materno')
  emergencia_lugar_de_nacimiento = models.CharField(max_length=60,verbose_name='Lugar de Nacimiento')
  emergencia_curp                = models.CharField(max_length=60,verbose_name='Curp')
  emergencia_fecha_de_nacimiento = models.DateField(auto_now=False,verbose_name='Fecha Nacimiento')
  emergencia_calle               = models.CharField(max_length=100,verbose_name='Calle')
  emergencia_numero              = models.CharField(max_length=20,verbose_name='Número')
  emergencia_colonia             = models.CharField(max_length=100,verbose_name='Colonia')
  emergencia_cp                  = models.IntegerField(default=0,verbose_name='Codigo Postal')
  emergencia_poblacion           = models.CharField(max_length=50,verbose_name='Población')
  emergencia_municipio           = models.CharField(max_length=50,verbose_name='Municipio')
  emergencia_entidad_federativa  = models.CharField(max_length=255,verbose_name='Entidad Federativa')
  emergencia_telefono_casa       = models.CharField(max_length=255,verbose_name='Telefono de Casa')
  emergencia_telefono_celular    = models.CharField(max_length=255,verbose_name='Telefono Celular')
  emergencia_email               = models.CharField(max_length=50,verbose_name='Email')
  observaciones                  = models.TextField(max_length=255,verbose_name='Observaciónes')
  doc_acta                       = models.BooleanField(default=False,verbose_name='Acta de Nacimiento(copia)')
  doc_curp                       = models.BooleanField(default=False,verbose_name='CURP')
  doc_fotografias                = models.BooleanField(default=False,verbose_name='Fotografias 4 Tamaño infantil Color')
  doc_certificado                = models.BooleanField(default=False,verbose_name='Certificado Médico')