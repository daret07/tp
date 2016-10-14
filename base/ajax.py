# -*- coding:UTF-8 -*-


def elimina_relacion(request):
  from importlib import import_module
  app            = request.POST['app_elemento']
  model          = request.POST['model']
  pk             = request.POST['pk']
  resultado      = {'elimino':'True'}
  try:
    _mod           = import_module("%s.models" % app)
  except :
    resultado = {'elimino':'False'}
  try:
    obj           = getattr(_mod,model)
    obj           = obj.objects.get(pk=pk)
    obj.delete()
  except :
    resultado = {'elimino':'False'}
  return resultado
