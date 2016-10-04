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

def recargo():
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
try:
  resl = cron_auto.objects.filter(activo=True)
  for i in resl:
    if int(i.cron) == 1:
      recargo()  
except Exception, e:
  print e
