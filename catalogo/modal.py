# -*- coding:UTF-8 -*-
from catalogo.forms import personaForm
from catalogo.models import persona
from django.contrib import messages
def persona_modal(request,pk=None):
  form_class = personaForm
  obj = None
  saves = False
  if pk is not None:
    obj = persona.objects.get(pk=pk)
  if request.POST:
    tipo = request.POST.get('met' or None)
    if tipo == None:
      form = form_class(request.POST or None,instance=obj)
    else:
      form = form_class()

  if request.POST and form.is_valid():
    obj = form.save(commit=False)
    obj.tipo = request.POST.get('tipo')
    obj.save()
    saves=True

  parametros={
    'form'    : form,
    'obj'     : obj,  
    'modulo'  : 'persona',
    'tipo'    : tipo,
    'custom'  : True,
    'saves'   : saves,
  }
  return parametros