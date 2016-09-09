from django import template

register = template.Library()

@register.assignment_tag()
def dentro_menu(seccion,modelo):
  if modelo is None:
    return False
  try:
    if modelo in seccion['hijos_ids']:
      return True
  except:
    return False

  return False
