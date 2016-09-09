from django.conf import settings

def custom_context(self):
  app    = self.session.get('app',None)
  modelo = self.session.get('modelo',None)

  parametros = {
    'app'               : app,
    'modelo'            : modelo,
    'project_name'      : settings.PROJECT_NAME,
    'project_name_mini' : settings.PROJECT_NAME_MINI
  }

  try:
    from navegacion.models import menu
    obj = menu.objects.all().prefetch_related('hijos','padre').order_by('nivel')
    nav = []
    for item in obj:
      modelo_tmp = []
      menu_tmp = {}
      menu_tmp['pk']      = item.pk
      menu_tmp['padre']   = item.padre.pk if item.padre else ''
      menu_tmp['nombre']  = item.nombre

      arreglo = []
      for data in item.hijos.all():
        arreglo.append(
          {
            'app':     data.app,
            'modelo':  data.modelo,
            'permiso': self.user.has_perm(data.permiso),
            'icono':   data.icono,
            'nombre':  data.nombre,
            'listar':  data.listar,
          }

        )

      menu_tmp['hijos']   = arreglo
      menu_tmp['permiso'] = self.user.has_perm(item.permiso)
      menu_tmp['app']     = item.app
      menu_tmp['modelo']  = item.modelo
      menu_tmp['icono']   = item.icono
      menu_tmp['listar']  = item.listar

      for item_tmp in  menu_tmp['hijos']:
        modelo_tmp.append(item_tmp['modelo'])

      menu_tmp['hijos_ids'] = modelo_tmp
      menu_tmp['hijo_permisos']  =  False

      for hijo in item.hijos.all():
        # Si no se especifica permiso, se toma como pagina valida
        if self.user.has_perm(hijo.permiso) :
          menu_tmp['hijo_permisos']  = True
          break

      nav.append(menu_tmp)

    parametros['paginas'] = nav
  except  :
    pass

  try:
    from notificacion.views import get_notificaciones
    parametros['notificaciones'] = get_notificaciones(self)
  except:
    pass

  return parametros
