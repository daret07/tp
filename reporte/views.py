# -*- coding: utf-8 -*-
from django.shortcuts import render
from reporte.forms import (movimientoForm,reporte_saldosForm,ficha_inscricionForm,estado_cuentaForm)
from reporte.models import (movimiento)
from django.contrib import messages
import xlrd
from os.path import join, dirname, abspath
from catalogo.models import concepto,alumno as alm,referencias as ref, ciclo_escolar
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse
from datetime import datetime
# Create your views here.

def vista_movimiento(request,pk=None):
  form_class = movimientoForm 
  obj = None
  referencia_null=False
  if pk is not None: 
    obj = movimiento.objects.get(pk=pk)

  form = form_class(request.POST or None,instance=obj)

  if request.FILES:
    extension_valida = [
      ".xls",
      ".xlsx",
    ]
    file = request.FILES.get('archivo' or None)
    nombre_imagen = file.name

    imagen_valida = False
    for extension in extension_valida:
      if nombre_imagen.lower().endswith(extension):
        imagen_valida = True
        break
    
    if imagen_valida:
      obj = form.save(commit=False)
      obj.archivo = request.FILES.get('archivo' or None)
      obj.save()
      libro = xlrd.open_workbook(obj.archivo.path)
      hojas = libro.sheet_names()
      hoja  = libro.sheet_by_name(hojas[0])
      columnas = hoja.ncols

      if columnas == 10:
        for row_idx in range(0, hoja.ncols):
          label_numero = hoja.cell(0,row_idx).value

          if label_numero.lower() == 'referencia':
            obj.referencia = hoja.cell(1,row_idx).value
            tmp            = int(hoja.cell(1,row_idx).value)
            try:
              ref_tmp        = ref.objects.get(referencia=tmp)
              alumno_tmp     = alm.objects.get(pk=ref_tmp.alumno.pk)
              obj.alumno     = alumno_tmp
              obj.ciclo      = alumno_tmp.ciclo_escolar
            except:
              referencia_null = True
          
          if label_numero.lower() == 'importe':
            obj.monto = hoja.cell(1,row_idx).value

          if label_numero.lower().encode('utf8') == 'numero operación':
            obj.folio = hoja.cell(1,row_idx).value

          if label_numero.lower().encode('utf8') == 'fecha de operación':
            obj.fecha_registro = xlrd.xldate.xldate_as_datetime(hoja.cell(1,row_idx).value, libro.datemode)

      obj.concepto = concepto.objects.get(clave='abono')
      obj.save()
      messages.success(request,"Se ha Guardado la información con éxito")
      form = form_class(instance=obj)
    else:
      messages.success(request,"La extencion del archivo debe de ser xls o xlsx")
      form = form_class(instance=obj)
  elif request.POST and form.is_valid():
    alumno = request.POST.get('alumno')
    referencia = request.POST.get('referencia')
    monto  = request.POST.get('monto')
    if monto != '':
      obj = form.save(commit=False)
      obj.ciclo = ciclo_escolar.objects.get(alumno=alumno)
      obj.save()
      messages.success(request,"Se ha Guardado la información con éxito")
    else:
      messages.error(request,'Se debe de colocar almenos una de las dos opciones, ya se archivo o llenar todos los campos')
    form = form_class(request.POST or None,instance=obj)
  
  if obj:
    if obj.alumno:
      referencia_null = True

  parametros={
    'form'      : form,
    'custom'    : True,
    'obj'       : obj,
    'modulo'    : 'movimiento',
    'nula'      : referencia_null
  }
  return parametros

def vista_ficha_inscripcion(request,pk=None):
  from catalogo.models import ciclo_escolar,categoria
  from inscripcion.models import inscripcion
  from django.db.models import Q
  ciclo = ciclo_escolar.objects.all()
  categ = categoria.objects.all()
  inscripcion_filtro = None
  tmp_ciclo =''
  tmp_categoria=''
  form = ficha_inscricionForm()
  if request.POST:
    
    if request.POST.get('ciclo'):
      tmp_ciclo     = ciclo_escolar.objects.get(pk=request.POST.get('ciclo'))
    
    if request.POST.get('categoria'):
      tmp_categoria = categoria.objects.get(pk=request.POST.get('categoria'))

    if tmp_categoria != '' and tmp_ciclo != '':
      inscripcion_filtro   = inscripcion.objects.filter(ciclo=tmp_ciclo,categoria=tmp_categoria)
    elif tmp_categoria == '' and tmp_ciclo != '':
      inscripcion_filtro   = inscripcion.objects.filter(ciclo=tmp_ciclo)
    elif tmp_categoria != '' and tmp_ciclo == '':
      inscripcion_filtro   = inscripcion.objects.filter(categoria=tmp_categoria)
    form = ficha_inscricionForm(request.POST)
  parametros={
    'ciclo'      : ciclo,
    'categoria'  : categ,
    'inscripcion': inscripcion_filtro,
    'form'       : form
  }
  return parametros

def vista_reporte_referencia(request,pk=None):
  refe = ref.objects.all()
  parametros={'referencias':refe}
  return parametros

def vista_reporte_saldos(request,pk=None): 
  from reporte.models import movimiento
  alumnos =''
  reporte =[]
  form = reporte_saldosForm
  total = 0
  fecha_inicio = datetime.strptime(str(datetime.now())[:10],"%Y-%m-%d").strftime("%d/%m/%Y")
  fecha_fin    = datetime.strptime(str(datetime.now())[:10],"%Y-%m-%d").strftime("%d/%m/%Y")
  
  if request.POST:
    f_i = request.POST.get('desde', datetime.now())
    f_f = request.POST.get('hasta', datetime.now())
    ciclo_existe = False
    fecha_inicio = datetime.strptime(str(f_i),"%d/%m/%Y").strftime("%Y-%m-%d")
    fecha_fin    = datetime.strptime(str(f_f),"%d/%m/%Y").strftime("%Y-%m-%d")
    ciclo_tmp    = request.POST.get('ciclo')
    if len(ciclo_tmp)>0:
      ciclo   = ciclo_escolar.objects.get(pk=request.POST.get('ciclo'))
      ciclo_existe=True
    if ciclo_existe:
      alumnos = alm.objects.filter(fecha_de_ingreso__range=(fecha_inicio,fecha_fin),ciclo_escolar=ciclo)
    else:  
      alumnos = alm.objects.filter(fecha_de_ingreso__range=(fecha_inicio,fecha_fin))
    for i in alumnos:
      movimientos=movimiento.objects.filter(alumno=i)  
      suma = 0
      for a in movimientos:
        if str(a.concepto.tipo) == 'ingreso':
          suma += a.monto
          total += a.monto
        elif str(a.concepto.tipo) == 'egreso':
          suma -= a.monto
          total -= a.monto
      reporte.append((i.matricula,i.nombre+' '+i.paterno+' '+i.materno, i.fecha_de_nacimiento,suma,i.estatus))
    form = reporte_saldosForm(request.POST or None)
  else:
    form = reporte_saldosForm(initial={'desde':fecha_inicio,'hasta':fecha_fin})
  parametros={'reporte':reporte,'form':form,'total':total}
  return parametros

def vista_deudores(request,pk=None):
  from django.db.models import Count, Sum
  alumno = movimiento.objects.values('alumno').distinct()
  deudores_tmp=[]
  deudores =[]
  total = 0
  for i in alumno:
    tmp= i['alumno']
    movimientos=movimiento.objects.filter(alumno=tmp)
    suma = 0
    for a in movimientos:
      if str(a.concepto.tipo) == 'ingreso':
        suma += a.monto
        total += a.monto
      elif str(a.concepto.tipo) == 'egreso':
        suma -= a.monto
        total -= a.monto
    if suma < 0:
      deudores_tmp.append((i['alumno'],suma))
  for i in deudores_tmp:
    alumno_tmp=alm.objects.get(pk=i[0])
    deudores.append((alumno_tmp.matricula,alumno_tmp.nombre,alumno_tmp.fecha_de_nacimiento,float(i[1])))
  parametros={'saldo':deudores,'total':total}
  return parametros

def vista_estado_cuenta(request,pk=None):
  from base import settings
  form = estado_cuentaForm
  algo =None
  if request.POST:
    response = HttpResponse(content_type='application/pdf')
    logo =str(settings.BASE_DIR)+ str('/static/images/fmonarca2.png')
    alumno_temp = request.POST.get('alumno' or None)
    ciclo_temp  = request.POST.get('ciclo_escolar' or None)
    mes         = request.POST.get('mes' or None)
    anio        = request.POST.get('anio' or None)
    alumno_pdf = None
    ciclo_pdf = None
    padre = ''
    alumno=''
    ciclo = ''
    refere = ''
    monto = ''
    total_men =0
    total_abon = 0
    total_total = 0
    if alumno_temp:
      alumno_pdf = alm.objects.get(pk=alumno_temp)
      movimiento_pdf = ref.objects.filter(alumno=alumno_pdf)
      if movimiento_pdf:
        for i in movimiento_pdf:
          if 'principal' in i.descripcion.lower():
            refere = 'Referencia: '+i.referencia
            mov = movimiento.objects.filter(alumno=alumno_pdf)
            for i in mov:
              if 'mens' in str(i.concepto).lower():
                total_men += i.monto
              if 'abon' in str(i.concepto).lower():
                total_abon += i.monto
            total_total = total_men-total_abon
            if total_total < 0:
              total_total = 0
        monto  = 'Total a Pagar: $'+str(total_total)
        monto_2 = str(total_total)
      else:
        messages.error(request,'El Alumno no tiene ninguna referencia asignada')
        parametros={
          'form':form,
        }
        return parametros
    if alumno_pdf:
      alumno    = 'Nombre Alumno: '+alumno_pdf.nombre+' '+alumno_pdf.paterno+' '+alumno_pdf.materno
      padre     = 'Nombre Padre:  '+alumno_pdf.padre.nombre+' '+alumno_pdf.padre.paterno+' '+alumno_pdf.padre.materno
      ciclo     = 'Ciclo Escolar: '+alumno_pdf.ciclo_escolar.clave
      fecha     = 'Fecha de Emision: '+datetime.strptime(str(datetime.now())[:10],"%Y-%m-%d").strftime("%d/%m/%Y")
      antes_de  = 'Pagar antes de: 10/'+ mes+'/'+anio
      intereses = '(Para no Generar Intereses)'
    response['Content-Disposition'] = 'attachment; filename="'+alumno_pdf.nombre+' '+alumno_pdf.paterno+' '+alumno_pdf.materno+'.pdf"'
    buffer = BytesIO()
    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 12)
    p.drawImage(logo,50,715,80,80)
    p.drawImage(logo,170,415,280,280)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(225 , 730, "ESTADO DE CUENTA INTEGRAL")
    p.setFont("Helvetica", 8)
    p.drawString(50 , 670, alumno)
    p.drawString(50 , 660, ciclo)
    p.drawString(50 , 650, padre)
    p.drawString(50 , 640, refere)
    p.drawString(350 , 670, fecha)
    p.drawString(350 , 660, monto)
    p.drawString(350 , 650, antes_de)
    p.setFont("Helvetica", 6)
    p.drawString(350 , 640, intereses)
    p.setFont("Helvetica", 8)
    p.drawString(50 , 620, 'Resumen Informativo')
    p.drawString(50 , 610, 'Saldo Anterior')
    p.drawString(50 , 600, 'Mes Actual: $'+monto_2)
    p.drawString(350 , 620, 'Cargos del Mes')
    p.drawString(250 , 610, 'Fecha')
    p.drawString(320 , 610, 'Concepto')
    p.drawString(430 , 610, 'Abono')
    p.drawString(500 , 610, 'Cargo')
    num_tmp = 610
    for i in mov:
      num_tmp -= 10
      fecha = datetime.strptime(str(i.fecha_registro),"%Y-%m-%d").strftime("%d/%m/%Y")
      if str(i.concepto.tipo)=='egreso':
        p.drawString(500 , num_tmp, '$ '+str(i.monto))
        p.drawString(430 , num_tmp, '$ 0.0')
      if str(i.concepto.tipo)=='ingreso':
        p.drawString(500 , num_tmp, '$ 0.0')
        p.drawString(430 , num_tmp, '$ '+str(i.monto))
      p.drawString(250 , num_tmp, fecha)
      p.drawString(320 , num_tmp, i.concepto.descripcion)

    

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    form = estado_cuentaForm(request.POST or None)
    return response
  parametros={
  'form':form,
  }
  return parametros