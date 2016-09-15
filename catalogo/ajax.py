def get_persona(request):
  from catalogo.models import persona
  _persona = persona.objects.all()

  obj = []
  for item in _persona:
    obj.append((item.nombre,item.pk))

  return obj
