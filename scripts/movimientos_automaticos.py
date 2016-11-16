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
from automatico.models import cron_auto,pronto_pago,recargo_pago,excendente
from inscripcion.models import inscripcion
from reporte.models import movimiento
from reporte.views import descuentos
from django.utils import timezone
from django.db.models import Sum

def mensualidad(cron):
  alumnos     = inscripcion.objects.all()
  mensualidad = pronto_pago.objects.filter(padre=cron)
  for mensual in mensualidad:
    for i in alumnos:
      if i.alumno.estatus == True:
        tmp = decs.objects.filter(alumno=i.alumno,activo=True,concepto=mensual.beca)
        movimiento.objects.create(
        fecha_registro=timezone.now(),
        ciclo=i.alumno.ciclo_escolar,
        alumno=i.alumno,
        concepto=mensual.beca,
        monto=mensual.beca.importe,
        descripcion=mensual.beca.descripcion)
        for tmp_desc in tmp:
          if tmp_desc.tipo_descuento == '0':
            sum_tmp = (float(mensual.beca.importe) * (float(tmp_desc.monto)/100))
            movimiento.objects.create(
              fecha_registro=timezone.now(),
              ciclo=i.alumno.ciclo_escolar,
              alumno=i.alumno,
              concepto=tmp_desc.concepto,
              monto=-(float(mensual.beca.importe) * (float(tmp_desc.monto)/100)),
              descripcion=tmp_desc.descripcion)
          elif tmp_desc.tipo_descuento == '1':
            movimiento.objects.create(
              fecha_registro=timezone.now(),
              ciclo=i.alumno.ciclo_escolar,
              alumno=i.alumno,
              concepto=tmp_desc.concepto,
              monto=-float(tmp_desc.monto),
              descripcion=tmp_desc.descripcion)


def recargos(cron):
  alumnos     = inscripcion.objects.all()
  mensualidad = recargo_pago.objects.filter(padre=cron,activo=True)
  for i in mensualidad:
    for alm in alumnos:
      if alm.alumno.estatus == True:
        suma_tmp = 0
        movs = movimiento.objects.filter(alumno=alm.alumno)
        for movs_tmp in movs:
          if movs_tmp.concepto.tipo == 'I':
            suma_tmp+=movs_tmp.monto
          elif movs_tmp.concepto.tipo == 'E':
            suma_tmp-=movs_tmp.monto

        if suma_tmp < -(float(i.cantidad_debe)*float(i.concepto.importe)+float(i.diferencia)):
          try:
            movimiento.objects.create(
            fecha_registro=timezone.now(),
            ciclo=alm.alumno.ciclo_escolar,
            alumno=alm.alumno,
            concepto=i.aplica,
            monto=float(i.aplica.importe),
            descripcion=i.aplica.descripcion)
          except Exception as e:
            print e
        
        
def excede(cron):
  alumnos     = inscripcion.objects.all()  
  excende_tmp = excendente.objects.filter(activo=True)
  debe = 0
  for i in alumnos:
    if i.alumno.estatus == True:
      ingreso   = movimiento.objects.filter(concepto__tipo = 'I',alumno=i.alumno)
      total_ingreso = ingreso.aggregate(total = Sum('monto'))['total'] 
      if not total_ingreso:
        total_ingreso = 0

      egreso = movimiento.objects.filter(concepto__tipo = 'E',alumno=i.alumno)
      total_eso = egreso.aggregate(total = Sum('monto'))['total'] 
      if not total_eso:
        total_eso = 0
      
      debe = total_eso-total_ingreso
      for excedent_f in excende_tmp:
        if 0 > debe and debe >= (-1*int(excedent_f.monto)):
          try:
            movimiento.objects.create(
            fecha_registro=timezone.now(),
            ciclo=i.alumno.ciclo_escolar,
            alumno=i.alumno,
            concepto=excedent_f.concepto_exc,
            monto=float(-1*debe),
            descripcion=excedent_f.concepto_exc.descripcion)
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
          elif i.tipo == '3':
            print 'exedente'
            excede(i)
