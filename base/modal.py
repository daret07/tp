def testing(request):
  from django.utils import timezone

  parametros = {
    'mensaje' : 'Alejandro Ambriz',
    'hora'    : timezone.now(),
  }
  
  return parametros

def modal_generico(request):
  from base.views import obtener_form
  from importlib import import_module
  from django.conf import settings
  import traceback

  parametros = {}

  modal_app      = request.POST.get('modal_app',None)
  modal_modelo   = request.POST.get('modal_modelo',None)
  guardado       = request.POST.get('guardado',"")
  app            = request.POST.get('app',None)
  popup          = request.POST.get('popup',None)

  form = None
  obj      = None
  try:
    _form,obj,parametros = obtener_form(modal_app,modal_modelo,request,parametros)
    parametros['se_guardo'] = 'false'
    if guardado == "true":
      form = _form(request.POST or None,request.FILES or None,instance=obj,prefix='modal')
      if form.is_valid():
        obj = form.save()
        parametros['pk']           = obj.pk
        parametros['se_guardo'] = 'true'
    else:
      form = _form(prefix='modal')
  except Exception as e:
    if settings.DEBUG:
      traceback.print_exc()

  nombre_base = '%s.html'%modal_modelo

  parametros['nombre_base']  = nombre_base
  parametros['form']         = form
  parametros['modal_modelo'] = modal_modelo
  parametros['modal_app']    = modal_app
  parametros['app']          = app
  parametros['popup']        = popup
  parametros['obj']          = obj

  return parametros
