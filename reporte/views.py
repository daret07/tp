# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from reporte.forms import (movimientoForm,reporte_saldosForm,ficha_inscricionForm,estado_cuentaForm)
from reporte.models import (movimiento)
from django.contrib import messages
import xlrd
from os.path import join, dirname, abspath
from catalogo.models import concepto,alumno as alm,referencias as ref, ciclo_escolar
from inscripcion.models import inscripcion
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
      obj_1 = form.save(commit=False)
      obj_1.archivo = request.FILES.get('archivo' or None)
      obj_1.save()
      libro = xlrd.open_workbook(obj_1.archivo.path)
      hojas = libro.sheet_names()
      hoja  = libro.sheet_by_name(hojas[0])
      columnas = hoja.ncols
      if columnas >= 10:

        for row in range(1, hoja.nrows):
          obj = movimiento.objects.create()
          for row_idx in range(0, hoja.ncols):
            label_numero = hoja.cell(0,row_idx).value

            if label_numero.lower() == 'referencia':
              obj.referencia = hoja.cell(row,row_idx).value
              tmp            = int(hoja.cell(row,row_idx).value)

              try:
                ref_tmp        = ref.objects.get(referencia=tmp)
                alumno_tmp     = alm.objects.get(pk=ref_tmp.alumno.pk)
                obj.alumno     = alumno_tmp
                obj.ciclo      = alumno_tmp.ciclo_escolar
              except:
                referencia_null = True
            
            if label_numero.lower() == 'importe':
              obj.monto = hoja.cell(row,row_idx).value
            

            if 'numero operaci' in label_numero.lower().encode('utf8'):
              
              obj.folio = int(hoja.cell(row,row_idx).value)

            if label_numero.lower().encode('utf8') == 'fecha de operación':
              obj.fecha_registro = xlrd.xldate.xldate_as_datetime(hoja.cell(row,row_idx).value, libro.datemode)
            obj.concepto = concepto.objects.get(clave='ABONO')
          tmp_objeto = movimiento.objects.filter(folio=obj.folio)

          if not tmp_objeto:
            obj.save()
            monto_calc(obj)
            try:
              alumno_s = alm.objects.get(pk=ref_tmp.alumno.pk)
              descuentos(alumno_s,obj.monto,obj.concepto,alumno_s.ciclo_escolar)
            except:
              tmpes=''
          else:
            obj.delete()
      obj_1.delete()
      form = form_class(instance=obj)
    else:
      messages.success(request,"La extencion del archivo debe de ser xls o xlsx")
      form = form_class(instance=obj)
  elif request.POST and form.is_valid():
    alumno = request.POST.get('alumno')
    referencia = request.POST.get('referencia')
    monto  = request.POST.get('monto')
    anticipo = request.POST.get('anticipo')
    if monto != '':
      obj = form.save(commit=False)
      obj.descripcion = 'Movimiento Manual'
      obj.save()
      descuentos(alumno,obj.monto,obj.concepto,obj.ciclo)
      if int(anticipo)==1:
        monto_calc(obj)
      messages.success(request,"Se ha Guardado la información con éxito")
    else:
      messages.error(request,'Se debe de colocar almenos una de las dos opciones, ya se archivo o llenar todos los campos')
    form = form_class(request.POST or None,instance=obj)
  
  if pk:
    if obj.alumno:
      referencia_null = True

  operacion = request.POST.get('form_action',None)

  if operacion == 'SAVE_AND_OTHER':
    return redirect('crear',app='reporte',modelo='movimiento')
  elif operacion == 'SAVE':
    return redirect('listar',app='reporte',modelo='movimiento')

  form.fields["concepto"].queryset = concepto.objects.exclude(clave__contains="ANTICIPO_")
  parametros={
    'form'      : form,
    'custom'    : True,
    'obj'       : obj,
    'modulo'    : 'movimiento',
    'nula'      : referencia_null
  }
  return parametros


def monto_calc(obj):
  from django.utils import timezone
  import datetime
  tmp_concepto = concepto.objects.filter(clave='MENSUALIDAD')
  for item_tmp in tmp_concepto:
    if float(item_tmp.importe) == float(obj.monto):
      pass
    else:
      try:
        tmp_anticipo = concepto.objects.filter(importe=obj.monto)
        if tmp_anticipo:
          for item_anticipo in tmp_anticipo:
            tmp_beca_anticipo = concepto.objects.filter(clave__contains='ANTICIPO_%s'%item_anticipo.clave)
            for item_beca in tmp_beca_anticipo:
              calculo_mensualidad           = (float(obj.monto) + float(item_beca.importe))/float(item_tmp.importe)
              calculo_divicion_mensualidad  = float(obj.monto)/calculo_mensualidad
              calculo_divicion_bca          = float(item_beca.importe)/calculo_mensualidad
              count                         = 0
              date_count                    = obj.fecha_registro
              while count < calculo_mensualidad:
                if count == 0:
                  movimiento.objects.filter(pk=obj.pk).update(concepto=item_anticipo,monto=calculo_divicion_mensualidad,descripcion=item_anticipo.descripcion)
                  movimiento.objects.create(
                  folio=str(obj.folio)+'_A',
                  fecha_registro=date_count,
                  referencia=obj.referencia,
                  ciclo=obj.ciclo,
                  alumno=obj.alumno,
                  concepto=item_beca,
                  monto=calculo_divicion_bca,
                  descripcion=item_beca.descripcion)
                else:
                  date_count=fecha(date_count,count)
                  movimiento.objects.create(
                    folio=str(obj.folio)+'_A',
                    fecha_registro=date_count,
                    referencia=obj.referencia,
                    ciclo=obj.ciclo,
                    alumno=obj.alumno,
                    concepto=item_anticipo,
                    monto=calculo_divicion_mensualidad,
                    descripcion=item_anticipo.descripcion)
                  movimiento.objects.create(
                    folio=str(obj.folio)+'_A',
                    fecha_registro=date_count,
                    referencia=obj.referencia,
                    ciclo=obj.ciclo,
                    alumno=obj.alumno,
                    concepto=item_beca,
                    monto=calculo_divicion_bca,
                    descripcion=item_beca.descripcion)
                count = count + 1
        else:
          
          tmp_1_mes         = float(obj.monto)-float(item_tmp.importe)
          tmp_anticipo_mes  = concepto.objects.filter(importe=tmp_1_mes).exclude(clave__contains='ANTICIPO_')
          
          if tmp_anticipo_mes:

            movimiento.objects.filter(pk=obj.pk).update(monto=item_tmp.importe)
          
            for tmp_mes in tmp_anticipo_mes:
          
              tmp_beca_anticipo_mes = concepto.objects.filter(clave__contains='ANTICIPO_%s'%tmp_mes.clave)
              if tmp_beca_anticipo_mes:

                for item_mes_tmp in tmp_beca_anticipo_mes:

                  date_count=fecha(obj.fecha_registro,1)
                  print date_count
                  try:
                    movimiento.objects.create(
                      folio=str(obj.folio)+'_A',
                      fecha_registro=date_count,
                      referencia=obj.referencia,
                      ciclo=obj.ciclo,
                      alumno=obj.alumno,
                      concepto=tmp_mes,
                      monto=tmp_mes.importe,
                      descripcion=tmp_mes.descripcion)

                    movimiento.objects.create(
                      folio=str(obj.folio)+'_A',
                      fecha_registro=date_count,
                      referencia=obj.referencia,
                      ciclo=obj.ciclo,
                      alumno=obj.alumno,
                      concepto=item_mes_tmp,
                      monto=item_mes_tmp.importe,
                      descripcion=item_mes_tmp.descripcion)
                  except Exception as e:
                    print e
          else:
            pass
      except:
        pass



def fecha(date,count):
  import datetime
  fec = ''
  y = date.year
  m = date.month
  d = date.day
  if m == 12 and count == 0:
    m = m
  elif m == 12 and count >0:
    m = 1
    y = date.year + 1
  else:
    m = m+1

  fec = datetime.datetime(y,m,d)
  return fec



def descuentos(alumno,monto,concepto,ciclo):
  from catalogo.models import descuento, alumno as alm
  from reporte.models import movimiento
  tip_tmp        = ''
  ciclo_tmp      = ''
  monto_tmp      = ''
  alumno_tmp     = alm.objects.get(pk=alumno)
  desc           = descuento.objects.filter(alumno=alumno,activo=True)
  f_i = datetime.now()
  for i in desc:
    tip_tmp = i.tipo_descuento
    if i.concepto == concepto:
      if tip_tmp:
        monto_tmp = -(float(monto)*(float(i.monto)/100))
      else:
        monto_tmp = -float(i.monto)
      movimiento.objects.create(fecha_registro=(datetime.strptime(str(f_i)[:10],"%Y-%m-%d").strftime("%Y-%m-%d")),
      ciclo=ciclo,alumno=alumno_tmp,concepto=i.concepto,monto=monto_tmp,descripcion='Movimiento de Beca')
  parametros={
  'mensaje':True
  }
  return parametros


def vista_ficha_inscripcion(request,pk=None):
  from catalogo.models import ciclo_escolar,categoria
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
    elif tmp_categoria == '' and tmp_ciclo == '':
      inscripcion_filtro = inscripcion.objects.all()

    form = ficha_inscricionForm(request.POST)
  parametros={
    'ciclo'      : ciclo,
    'categoria'  : categ,
    'inscripcion': inscripcion_filtro,
    'form'       : form
  }
  return parametros

def vista_reporte_referencia(request,pk=None):
  refe = ref.objects.all().prefetch_related('alumno')
  referes=[]
  for i in refe:
    referes.append((i.alumno.pk,i.referencia,i.descripcion,str(i.alumno.ant)+str(i.alumno.matricula),i.alumno.nombre+' '+i.alumno.paterno+' '+i.alumno.materno,i.alumno.fecha_de_nacimiento,i.alumno.estatus))
  parametros={'referencias':referes}
  return parametros

def vista_reporte_saldos(request,pk=None): 
  from django.db.models import Sum
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
      alumnos = alm.objects.filter(ciclo_escolar=ciclo)
    else:
      alumnos = alm.objects.all()
    for al in alumnos:

      suma = 0
      total_ingreso = 0
      total_eso = 0
      if ciclo_existe:
        ingreso = movimiento.objects.filter(fecha_registro__range=(fecha_inicio,fecha_fin),ciclo=ciclo,concepto__tipo = 'I',alumno=al)
        total_ingreso = ingreso.aggregate(total = Sum('monto'))['total'] 
        if not total_ingreso:
          total_ingreso = 0

        egreso = movimiento.objects.filter(fecha_registro__range=(fecha_inicio,fecha_fin),ciclo=ciclo,concepto__tipo = 'E',alumno=al)
        total_eso = egreso.aggregate(total = Sum('monto'))['total'] 
        if not total_eso:
          total_eso = 0
        
        suma = total_eso-total_ingreso
        total += suma
      else:
        ingreso = movimiento.objects.filter(fecha_registro__range=(fecha_inicio,fecha_fin),concepto__tipo = 'I',alumno=al)
        total_ingreso = ingreso.aggregate(total = Sum('monto'))['total'] 
        if not total_ingreso:
          total_ingreso = 0

        egreso = movimiento.objects.filter(fecha_registro__range=(fecha_inicio,fecha_fin),concepto__tipo = 'E',alumno=al)
        total_eso = egreso.aggregate(total = Sum('monto'))['total'] 
        if not total_eso:
          total_eso = 0
    
        suma = total_eso-total_ingreso
        total += suma

      reporte.append((al.ant+al.matricula.zfill(4) ,al.nombre+' '+al.paterno+' '+al.materno, al.fecha_de_nacimiento,suma,al.estatus,al.pk))
    form = reporte_saldosForm(request.POST or None)
  else:
    form = reporte_saldosForm(initial={'desde':fecha_inicio,'hasta':fecha_fin})
  parametros={'reporte':reporte,'form':form,'total':total}
  return parametros

def vista_deudores(request,pk=None):
  from django.db.models import Sum
  alumno = movimiento.objects.values('alumno').distinct()
  ciclo = ciclo_escolar.objects.all()
  valor = 0
  total = 0
  deudores_ciclo=[]
  deudores =[]
  for ciclos in ciclo:
    for alms in alumno:
      total_I= 0
      total_E= 0
      movis_i = movimiento.objects.filter(alumno= alms['alumno'],ciclo=ciclos).prefetch_related('concepto')
      for i in movis_i:
        if str(i.concepto.tipo) == 'I':
          total_I += i.monto
        if str(i.concepto.tipo) == 'E':
          total_E += i.monto

      total += float(total_E)
      if (float(total_I)-float(total_E))<0:
        deudores_ciclo.append((alms,float(total_I)-float(total_E),ciclos),)

  for deu in deudores_ciclo:
    alumno_tmp=alm.objects.get(pk=deu[0]['alumno'])
    deudores.append((alumno_tmp,alumno_tmp.pk,float(deu[1]),deu[2]))
  parametros={'saldo':deudores,'total':total,'ciclo':ciclo}
  return parametros

def vista_estado_cuenta(request,pk=None):
  from base import settings
  from django.db.models import Sum
  form = estado_cuentaForm
  algo =None
  if request.POST:
    response = HttpResponse(content_type='application/pdf')
    logo =str(settings.BASE_DIR)+ str('/static/images/fmonarca2.jpg')
    logoback =str(settings.BASE_DIR)+ str('/static/images/fmonarcaB.jpg')
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
    
    total_men =0
    total_abon = 0
    total_total = 0

    total_ingreso=0
    total_eso=0
    debe=0
    saldo_mensual=0

    if alumno_temp:
      alumno_pdf = alm.objects.get(pk=alumno_temp)
      movimiento_pdf = ref.objects.filter(alumno=alumno_pdf)

      ingreso = movimiento.objects.filter(concepto__tipo = 'I',alumno=alumno_pdf)
      total_ingreso = ingreso.aggregate(total = Sum('monto'))['total'] 
      if not total_ingreso:
        total_ingreso = 0

      egreso = movimiento.objects.filter(concepto__tipo = 'E',alumno=alumno_pdf)
      total_eso = egreso.aggregate(total = Sum('monto'))['total'] 
      if not total_eso:
        total_eso = 0
      
      debe = total_eso-total_ingreso


    #total a pagar saldo anterior y saldo actual
    abono_c_total = 0
    cargo_c_total = 0
    total_total_total = 0

    #calculo del saldo del mes seleccionado

    movs_mes = movimiento.objects.filter(alumno=alumno_pdf,fecha_registro__month=mes,fecha_registro__year=anio).prefetch_related('concepto')

    if movs_mes:
      for i in movs_mes:
        if str(i.concepto.tipo) == 'E':
          saldo_mensual += i.monto
        if str(i.concepto.tipo) == 'I':
          saldo_mensual -= i.monto
    # calculo del mes anterior

    saldo_mensual_ant = 0
    mes_ant = mes_anterior(mes,anio)
    movs_mes_ant = movimiento.objects.filter(alumno=alumno_pdf,fecha_registro__month=mes_ant['mes'],fecha_registro__year=mes_ant['anio']).prefetch_related('concepto')
    saldo_mensual_ant = 0
    if movs_mes_ant:
      for i in movs_mes_ant:
        if str(i.concepto.tipo) == 'E':
          saldo_mensual_ant += i.monto
        if str(i.concepto.tipo) == 'I':
          saldo_mensual_ant -= i.monto

    # Referencia
    if alumno_temp:
      if movimiento_pdf:
        for movi in movimiento_pdf:
          if 'principal' in movi.descripcion.encode('utf-8').lower():
            refere = 'Referencia: '+movi.referencia
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
    p.drawImage(logo,50,715,160,70)
    p.drawImage(logoback,100,315,430,260)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(225 , 730, "ESTADO DE CUENTA INTEGRAL")
    p.setFont("Helvetica", 8)
    p.drawString(50 , 670, alumno)
    p.drawString(50 , 660, ciclo)
    p.drawString(50 , 650, padre)
    p.drawString(50 , 640, refere)
    p.drawString(350 , 670, fecha)
    p.drawString(350 , 660, 'Total a pagar: $'+str(saldo_mensual))
    p.drawString(350 , 650, antes_de)
    p.setFont("Helvetica", 6)
    p.drawString(350 , 640, intereses)
    p.setFont("Helvetica", 8)
    p.drawString(50 , 620, 'Resumen Informativo')
    p.drawString(50 , 610, 'Saldo Anterior: $'+str(saldo_mensual_ant))
    p.drawString(50 , 600, 'Mes Actual: $'+str(saldo_mensual))
    p.drawString(250 , 590, 'Cargos del Mes')
    p.drawString(70 , 580, 'Fecha')
    p.drawString(120 , 580, 'Concepto')
    p.drawString(430 , 580, 'ABONO')
    p.drawString(500 , 580, 'CARGO')
    num_tmp = 580
    for i in movs_mes:
      num_tmp -= 10
      fecha = datetime.strptime(str(i.fecha_registro),"%Y-%m-%d").strftime("%d/%m/%Y")
      if str(i.concepto.tipo)=='E':
        p.drawString(500 , num_tmp, '$ '+str(i.monto))
        p.drawString(430 , num_tmp, '$ 0.0')
      if str(i.concepto.tipo)=='I':
        p.drawString(500 , num_tmp, '$ 0.0')
        p.drawString(430 , num_tmp, '$ '+str(i.monto))
      p.drawString(60 , num_tmp, fecha)
      p.drawString(120 , num_tmp, i.concepto.descripcion)

    

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

def mes_anterior(mes,anio):
  anio_a = 0
  mes_a  = 0
  if int(mes) == 1:
    mes_a = 12
    anio_a = int(anio) - 1
  else:
    mes_a = int(mes) - 1
    anio_a=anio
  return {
  'mes' :mes_a,
  'anio':anio_a,
  }


def listado_movimiento(request):
  abono      = 0
  cargo      = 0
  diferencia = 0
  abonos = movimiento.objects.all().prefetch_related('concepto')
  for i in abonos:
    try:
      if 'I' == str(i.concepto.tipo):
        abono += i.monto
      if 'E' == str(i.concepto.tipo):
        cargo += i.monto
    except:
      cargo +=0
      abono +=0
  diferencia = abono - cargo
  return {'abono':abono,'cargo':cargo,'diferencia':diferencia}