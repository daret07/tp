import MySQLdb
import sys
import datetime
reload(sys)
sys.setdefaultencoding("utf-8")

sys.path.append('/home/daret/fbasicas/dj_fbasicas')
sys.path.append('/home/daret/fbasicas/1.10.1/lib/python2.7/site-packages')

import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","base.settings")
django.setup()

fecha = str(datetime.datetime.now())[:10]

from catalogo.models import concepto,alumno,descuento as decs
from automatico.models import cron_auto
from inscripcion.models import inscripcion
from reporte.models import movimiento
from reporte.views import descuentos

def recargo(definicion):
  recargo_normal_1    = 0
  recargo_normal_1_pk = 0
  tmp_recargo         = 0
  conceptos           = concepto.objects.filter(clave__contains='RECARGO')

  for i in conceptos:
    if str(i.clave) == 'RECARGO1':
      recargo_normal_1 = i.importe
      recargo_normal_1_pk= i.pk

  inscritos           = inscripcion.objects.all()
  
  for insc in inscritos:
    suma = 0
    movs = movimiento.objects.filter(alumno=insc.alumno)
    mensualidad           = concepto.objects.get(clave='MENSUALIDAD')
    mensualidadh          = concepto.objects.get(clave='MENSUALIDADH')
    descuento_tmp         = decs.objects.filter(alumno=insc.alumno)
    desc_tmp              = 0
    tmp_recargo           = 0
    tmp_recargo_id        = 0

    for i in descuento_tmp:
      if 'BECAM' in str(i.concepto.clave):
        desc_tmp = i.monto
    for i in movs:
      if 'ingreso' in i.concepto.tipo:
        suma -= i.monto
      elif 'egreso' in i.concepto.tipo:
        suma += i.monto

    if insc.alumno.hermano_institucion:
      if suma >= ((mensualidadh.importe-desc_tmp) * 2):
        tmp_recargo = 0
        desc_tmp_id = 0
      elif suma >= (mensualidadh.importe-desc_tmp):
        tmp_recargo = 0
        desc_tmp_id = 0
    else:
      if suma >= ((mensualidad.importe-desc_tmp) * 2):
        tmp_recargo = recargo_normal_1
        desc_tmp_id = recargo_normal_1_pk
      elif suma >= (mensualidad.importe-desc_tmp):
        tmp_recargo = recargo_normal_1
        desc_tmp_id = recargo_normal_1_pk
    if tmp_recargo > 0:
      tmp_conceptos = concepto.objects.get(pk=recargo_normal_1_pk)
      movimiento.objects.create(fecha_registro=fecha,
        ciclo=insc.alumno.ciclo_escolar,alumno=insc.alumno,
        concepto=tmp_conceptos,monto=float(tmp_conceptos.importe),descripcion='Movimiento Automatico')
      descuentos(insc.alumno.pk,tmp_conceptos.importe,tmp_conceptos)
  


def mensual(definicion):
  alumno_hermano=[]
  alumno_sin_hermano=[]
  hijo_trabajador=[]
  alm = alumno.objects.all()
  #se optienen los conceptos de mensualidad
  mens = concepto.objects.get(clave='MENSUALIDAD')
  mensh = concepto.objects.get(clave='MENSUALIDADH')
  cuota_normal     = mens.importe
  cuota_normal_id  = mens.pk
  cuota_hermano    = mensh.importe
  cuota_hermano_id = mensh.pk
  
  # Se traen todos los alumnos insritos
  inscritos = inscripcion.objects.filter(fecha_inscripcion__lte=fecha)

  #Se separan los que tienen hermanos y los que no tienen hermanos inscritos
  for i in inscritos:
    if i.alumno.hermano_institucion:
      alumno_hermano.append(i)
    else:
      alumno_sin_hermano.append(i)
  
  #Se realizan los cargos de mensualidad dependiendo de si tiene o no hermanos inscritos

  for sin in alumno_sin_hermano:
    movimiento.objects.create(fecha_registro=fecha,
      ciclo=sin.alumno.ciclo_escolar,alumno=sin.alumno,
      concepto=mens,monto=float(cuota_normal),descripcion='Movimiento Automatico')
    descuentos(sin.alumno.pk,cuota_normal,mens)
  for con in alumno_hermano:
    movimiento.objects.create(fecha_registro=fecha,
      ciclo=con.alumno.ciclo_escolar,alumno=con.alumno,
      concepto=mensh,monto=float(cuota_hermano),descripcion='Movimiento Automatico')
    descuentos(con.alumno.pk,cuota_hermano,mensh)

  recargo_normal_2      = 0
  recargo_normal_2_id   = 0
  recargo_normal_3      = 0
  recargo_normal_3_id   = 0

  recargo_hermano_2     = 0
  recargo_hermano_2_id  = 0
  recargo_hermano_3     = 0
  recargo_hermano_3_id  = 0

  conceptos = concepto.objects.filter(clave__contains='RECARGO')

  for i in conceptos:

    if str(i.clave) == 'RECARGO2':
      recargo_normal_2      = i.importe
      recargo_normal_2_id   = i.pk
    if str(i.clave) == 'RECARGO3':
      recargo_normal_3      = i.importe
      recargo_normal_3_id   = i.pk
    if str(i.clave) == 'RECARGOH2':
      recargo_hermano_2      = i.importe
      recargo_hermano_2_id   = i.pk
    if str(i.clave) == 'RECARGOH3':
      recargo_hermano_3      = i.importe
      recargo_hermano_3_id   = i.pk
  

  for sin in alumno_sin_hermano:
    suma = 0
    movs = movimiento.objects.filter(alumno=sin.alumno)
    descuento_tmp = decs.objects.filter(alumno=sin.alumno)
    desc_tmp=0
    for i in descuento_tmp:
      if 'BECAM' in str(i.concepto.clave):
        desc_tmp = i.monto
    for i in movs:
      if 'ingreso' in i.concepto.tipo:
        suma -= i.monto
      elif 'egreso' in i.concepto.tipo:
        suma += i.monto
    if suma >=((mensh.importe+desc_tmp) * 2):
      recargo_tmp(recargo_normal_2_id,sin,recargo_normal_2)
    if suma >=((mensh.importe+desc_tmp) * 3):
      recargo_tmp(recargo_normal_3_id,sin,recargo_normal_3)
  
  for con in alumno_hermano:
    suma = 0
    movs = movimiento.objects.filter(alumno=con.alumno)
    descuento_tmp = decs.objects.filter(alumno=con.alumno)
    desc_tmp=0
    for i in descuento_tmp:
      if 'BECAM' in i.concepto:
        desc_tmp = i.monto
    for i in movs:
      if 'ingreso' in i.concepto.tipo:
        suma -= i.monto
      elif 'egreso' in i.concepto.tipo:
        suma += i.monto
    if suma >=((mensh.importe-desc_tmp) * 2):
      recargo_tmp(recargo_hermano_2_id,con,recargo_hermano_2)
    if suma >=((mensh.importe-desc_tmp) * 3):
      recargo_tmp(recargo_hermano_3_id,con,recargo_hermano_3)

  
def recargo_tmp(con,alumno,importe):
  concep = concepto.objects.get(pk=con)
  tmp    = 'Automatico: '+str(concep.nombre)
  if importe>0:
    movimiento.objects.create(fecha_registro=fecha,
      ciclo=alumno.alumno.ciclo_escolar,alumno=alumno.alumno,
      concepto=concep,monto=float(importe),descripcion=tmp)

try:
  resl = cron_auto.objects.filter(activo=True)
  for i in resl:
    if int(i.cron) == 0:
      #mensual(i.definicion)
    elif int(i.cron) == 1:
      print i.definicion
      #recargo(i.definicion)  
except Exception, e:
  print e
