from django import template

register = template.Library()

@register.assignment_tag()
def get_pk(modelo,permiso):
  from django.contrib.auth.models import Permission
  listado = Permission.objects.filter(content_type__model=modelo,codename__contains=permiso)
  if listado.count() > 0:
    return listado[0].pk
  
  return ''

@register.assignment_tag()
def permiso_grupo(grupo,modelo,permiso):
  from django.contrib.auth.models import Permission
  if grupo is None:
    return ''

  listado = Permission.objects.filter(content_type__model=modelo,codename__contains=permiso)
  if listado.count() > 0:
    if listado[0].group_set.filter(pk=grupo).count() > 0:
      return 'checked'

  return ''

"""
Templatetag, que permite saber si un usuario tiene permiso sobre un menu
en especifico, este permiso muestra todos los permisos que se han asignado
los permisos que no se hayan asignado se tomaran como validos
"""
@register.assignment_tag()
def tiene_permiso(user,pag):
  # Si la pagina, es la padre, revisa que minimo un hijo tenga opcion.
  if pag['padre'] is None:
    total_permisos = 0
    for hijo in pag.hijos.all():
      # Si no se especifica permiso, se toma como pagina valida
      if not hijo.permiso:
        total_permisos += 1
      elif user.has_perm(hijo.permiso):
        total_permisos += 1
    # Si tiene minimo un permiso, es valido
    if total_permisos > 0:
      return True
  else:
    # Si no contiene nada en los permisos
    if not pag.permiso:
      return True

    return user.has_perm(pag.permiso)

  return False
