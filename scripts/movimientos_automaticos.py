#!/var/www/html/1.10.1/bin/python2.7
import sys
import datetime
import time
from imp import reload
reload(sys)
sys.setdefaultencoding("utf-8")

sys.path.append('/var/www/html/dj_fbasicas')
sys.path.append('/var/www/html/1.10.1/lib/python2.7/site-packages')

import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE","base.settings")
django.setup()

from catalogo.models import concepto,alumno,descuento as decs
from automatico.models import cron_auto,pronto_pago,recargo_pago
from inscripcion.models import inscripcion
from reporte.models import movimiento
from reporte.views import descuentos
from django.utils import timezone
def mensualidad(cron):
  alumnos     = alumno.objects.filter(estatus=True)
  mensualidad = pronto_pago.objects.filter(padre=cron)
  for mensual in mensualidad:
    for i in alumnos:
      tmp = decs.objects.filter(alumno=i,activo=True,concepto=mensual.beca)
      for tmp_desc in tmp:
        if tmp_desc.tipo_descuento == '0':
          sum_tmp = (float(mensual.beca.importe) * (float(tmp_desc.monto)/100))
          movimiento.objects.create(
            fecha_registro=timezone.now(),
            ciclo=i.ciclo_escolar,
            alumno=i,
            concepto=tmp_desc.concepto,
            monto=-(float(mensual.beca.importe) * (float(tmp_desc.monto)/100)),
            descripcion=tmp_desc.descripcion)
        elif tmp_desc.tipo_descuento == '1':
          movimiento.objects.create(
            fecha_registro=timezone.now(),
            ciclo=i.ciclo_escolar,
            alumno=i,
            concepto=tmp_desc.concepto,
            monto=-float(tmp_desc.monto),
            descripcion=tmp_desc.descripcion)
      movimiento.objects.create(
      fecha_registro=timezone.now(),
      ciclo=i.ciclo_escolar,
      alumno=i,
      concepto=mensual.beca,
      monto=mensual.beca.importe,
      descripcion=mensual.beca.descripcion)


def recargos(cron):
  alumnos     = alumno.objects.filter(estatus=True)
  mensualidad = recargo_pago.objects.filter(padre=cron,activo=True)
  for i in mensualidad:
    for alm in alumnos:
      suma_tmp = 0
      movs = movimiento.objects.filter(alumno=alm)
      for movs_tmp in movs:
        if movs_tmp.concepto.tipo == 'I':
          suma_tmp+=movs_tmp.monto
        elif movs_tmp.concepto.tipo == 'E':
          suma_tmp-=movs_tmp.monto

      if suma_tmp < -(float(i.cantidad_debe)*float(i.concepto.importe)+float(i.diferencia)):
        try:
          movimiento.objects.create(
          fecha_registro=timezone.now(),
          ciclo=alm.ciclo_escolar,
          alumno=alm,
          concepto=i.aplica,
          monto=float(i.aplica.importe),
          descripcion=i.aplica.descripcion)
        except Exception as e:
          print e
        
        
        
        
        

crons = cron_auto.objects.filter(activo=True)
actual = datetime.datetime.now()
cron_actual=[]  
hora = actual.strftime("%H")

cron_actual.append(str(int(actual.strftime("%M"))))
cron_actual.append(str(int(hora)))
cron_actual.append(str(int(actual.strftime("%d"))))
cron_actual.append(str(int(actual.strftime("%m"))))
cron_actual.append('*')
for i in crons:
  cron_verificar = (i.definicion).split(' ')
  if cron_actual[0] in cron_verificar[0]:
    if cron_actual[1] in cron_verificar[1]:
      if cron_actual[2] in cron_verificar[2]:
        if cron_actual[3] in cron_verificar[3]:
          if i.tipo == '1':
            print 'mensual'
            mensualidad(i)
          elif i.tipo == '2':
            print 'pago'
            recargos(i)
