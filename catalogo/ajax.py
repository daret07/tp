from catalogo.models import concepto
def get_persona(request):
  from catalogo.models import persona
  _persona = persona.objects.all()

  obj = []
  for item in _persona:
    obj.append((item.nombre,item.pk))

  return obj

def get_concepto(request):
  busca = request.POST.get('busca','').upper()
  conceptos =[]
  concep = ''
  if busca != '':
    concep = concepto.objects.filter(clave__contains=busca)
  for c in concep:
    conceptos.append(c.clave)
  print conceptos

  return conceptos