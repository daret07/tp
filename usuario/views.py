# -*- coding:UTF-8 -*-
from django.shortcuts import render
from django.contrib import messages
from base.utilidades import obtener_listado_admin
from usuario.models import usuario
from django.shortcuts import redirect

# Create your views here.
def vista_usuario(request,pk=None):
  from usuario.forms import usuarioForm

  parametros = {
    'custom' : True,
  }
  
  try:
    obj = usuario.objects.get(pk=pk)
  except:
    obj = None

  form = usuarioForm(request.POST or None,request.FILES or None,instance=obj)

  if form.is_valid():
    clave              = form.cleaned_data['clave']
    clave_confirmacion = form.cleaned_data['clave_confirmacion']
    if pk is None:
      if clave == clave_confirmacion:
        obj = form.save(commit = False)
        obj.set_password(clave)
        obj.save()
        form = usuarioForm(instance = obj)
        messages.info(request,'Se ha guardado con éxito la información.')
      else:
        form.add_error('clave','Las claves son incorrectas, por favor reviselo.')
    else:
      print request.POST['groups']
      obj = form.save()
      messages.info(request,'Se ha guardado con éxito la información.')

  parametros['form'] = form
  parametros['obj']  = obj

  return parametros

def vista_perfil(request,pk=None):
  from django.contrib.contenttypes.models import ContentType
  from django.contrib.auth.models import Permission
  
  all_permisos = Permission.objects.exclude(
    content_type__app_label__in=('admin','auth','contentypes','log','sessions','base','navegacion',)
  )
  
  arreglo_permiso = ["add","change","delete"]

  for tmp in all_permisos:
    a = tmp.codename.split('_')
    if not a[0] in arreglo_permiso:
        arreglo_permiso.append(a[0])

  arreglo_permiso = arreglo_permiso

  parametros = {
    'modelos'        : ContentType.objects.exclude(app_label__in=('admin','auth','contenttypes','log','sessions','base','navegacion',)),
    'grupo_permisos' : arreglo_permiso
  }

  return parametros

def vista_restablecer_clave(request,pk=None):
    from django.contrib.auth.forms import SetPasswordForm
    
    try:
        obj = usuario.objects.get(pk=pk)
    except:
        obj = None
    
    form = SetPasswordForm(obj,request.POST or None)
    
    if request.POST and form.is_valid():
        obj = form.save()
        messages.info(request,'Se ha cambiado la contraseña exitosamente.')
        return redirect('editar',app='usuario',modelo='usuario',pk=pk)
    
    parametros = {
        'custom' : True,
        'form'   : form,
        'obj'    : obj,
    }

    return parametros

def Print_print_test(request,app=None,modelo=None):
  return {}
