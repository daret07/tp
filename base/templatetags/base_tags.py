# -*- coding:UTF-8 -*-
from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.assignment_tag()
def crear_tabla(objeto, columnas,model):
  html =''
  columnas = columnas.split()
  if objeto:
    encabezado = '<tr>'
    contenido = ''
    for i in range(int(objeto.values('id').count())):
      contenido += """
                    <tr id="{0}">
                      <td hidden class ="id_row" value="{1}">{1}</td>
                    """.format(str(objeto.values('id')[i]['id']),str(objeto.values('id')[i]['id']))
      for j in columnas:
        if i == 0:
          encabezado += """
                        <th class="th_{0}_{1}">{2}</th>
                        """.format(model,str(j),j[0].upper()+j[1:].replace('_',' '))
          if columnas.index(j) == len(columnas)-1:
            encabezado += """
              <th class="th_{0}" style="width: 80px;">{1}</th>
              """.format('acciones', 'Acciones')
        try:
          contenido += """
                        <td class="td_{0}_{1} "  title="{3}"   >{2}</td>
                        """.format(model,str(j),
                              str(objeto.values(j)[i][j]) if len(str(objeto.values(j)[i][j])) < 12 else str(objeto.values(j)[i][j])[:11]+'...',str(objeto.values(j)[i][j]) )
        except:
          contenido += """<td class="td_{0}_{1}></td>""".format(model,str(j))
      contenido += """
                      <td class="td_acciones" style="width: 80px;">
                          <i class="fa fa-remove btn-eliminar_relacion_{0}" style="cursor:pointer" >&nbsp;&nbsp;</i>
                          <i class="fa fa-pencil btn-editar_relacion_{0}" style="cursor:pointer" data-editar='true'></i>
                      </td>
                    </tr>
                    """.format(model)
    encabezado += '<th></th></tr>'
    html = """
        <table class="table table-striped table-hover table-condensed " style="font-family: verdana;font-size:12px;margin-bottom:0" >
          <thead class="thead-inverse">
              {0}
          </thead>
        </table>
        <div class="table-responsive" id="m2m_table_{2}"  style=" overflow: auto" >
        <table class="table table-striped table-hover table-condensed "  style="font-family: verdana;font-size:12px" >
          <tbody  id="m2m_tbody_{2}" style="overflow-y: auto; ">
              {1}
          </tbody>
        </table>
        </div>
     """.format(encabezado,contenido,model)
  return mark_safe(html)

@register.assignment_tag()
def grupo_transmision_box(objeto,obj_tmp):
  html =''
  list_grupo_transmision = []
  marcado = ''
  if objeto:
    for elemento in obj_tmp.values('grupo_transmision'):
      list_grupo_transmision.append(elemento['grupo_transmision'])
      list_grupo_transmision = list(set(list_grupo_transmision))

    for i in range(int(objeto.values('id').count())):
      if objeto.values('pk')[i]['pk'] in list_grupo_transmision:
        marcado = 'checked'
      else:
        marcado = ''
      html += """
        <div class="checkbox">
          <label><input type="checkbox" class="transmision" value="{0}" {2}>{1}</label>
        </div>
      """.format(objeto.values('pk')[i]['pk'],objeto.values('descripcion')[i]['descripcion'],marcado)
  return mark_safe(html)

@register.assignment_tag()
def object_to_select(objeto=None,columnas='',sub_objetos='',modelo=''):
  from importlib import import_module

  if objeto is None or objeto == '':
    return ''

  if sub_objetos:
    sub_objetos = sub_objetos.split()
    _mod = import_module("%s.models" % sub_objetos[0])

  html ="""
  <select class="form-control select_search" id="select_{0}">'
  <option value="">--------</option>
  """.format(modelo)
  contenido = ''

  for i in range(objeto.values('id').count()):
    for j in columnas.split():
      if sub_objetos:
        if str(j) == str(sub_objetos[2]):
          obj = getattr(_mod,sub_objetos[1])
          pk=objeto.values(j)[i][j]
          if pk :
            obj = obj.objects.get(pk=str(pk))
            contenido += ' ' + str(obj)
        else:
          if type(objeto.values(j)[i][j]) != bool:
            contenido += ' ' + str((objeto.values(j)[i][j]).encode('utf-8'))
          else:
            contenido += ' ' + str((objeto.values(j)[i][j]))
      else:
        if type(objeto.values(j)[i][j]) != bool :
          contenido += ' ' + str((objeto.values(j)[i][j]).encode('utf-8'))
        else:
          contenido += ' ' + str((objeto.values(j)[i][j]))
    html += """
      <option value="{0}">{1}</option>
    """.format(objeto.values('pk')[i]['pk'],contenido)
    contenido = ''
  html += '</select>'
  return mark_safe(html)

@register.assignment_tag()
def tabla_catalogo(objeto, columnas):
  from importlib import import_module
  objeto = objeto.split()
  modelo = objeto
  _mod = import_module("%s.models" % objeto[0])
  objeto = getattr(_mod, objeto[1])
  objeto = objeto.objects.all()
  columnas = columnas.split()
  position = 0
  html =''
  contador = 0
  try:
    encabezado = '<tr>'
    contenido = ''
    for i in range(len(objeto)):
      contenido += """
                    <tr id="{0}">
                      <td hidden class ="id_row" value='{0}' >{0}</td>
                    """.format(objeto[i].id)
      for j in columnas:
        contador +=1
        if i == 0:
          encabezado += """
                        <th class="th_{0}_{1} th_catalogo" data-position="{3}" style="cursor:pointer">
                        <i class="fa fa-sort-amount-desc font-sort"></i>{2}
                        </th>
                        """.format(modelo[1],j,j[0].upper()+j[1:].replace('_',' '),position)
          position += 1
        try:
          contenido += """
                        <td class="td_{0}_{1} td_catalogo_{0}" style="cursor:pointer">{2}</td>
                        """.format(modelo[1],j,getattr(objeto[i], j))
        except:
          contenido += "<td> </td>\n"
      contenido += """
                    </tr>
                    """
    encabezado += '<th></th></tr>'
    html = """

        <table class="table table-bordered table-striped table-hover table-condensed " style="font-family: verdana;font-size:12px" >
          <thead class="thead-inverse">
              {0}
          </thead>
        </table>
        <div class="table-responsive" id="m2m_table_{2}"  style=" overflow: auto; height: 220px" >
        <table class="table table-bordered table-striped table-hover table-condensed " id="table_catalogo_{2}" style="font-family: verdana;font-size:12px" >
          <tbody  id="m2m_tbody_{2}" style="overflow-y: auto; ">
              {1}
          </tbody>
        </table>
        </div>
     """.format(encabezado,contenido,modelo[0])
  except:
    html = ''
  return mark_safe(html)

@register.assignment_tag()
def get_articulo(objeto):
  from bodega.models import articulo
  html = ''
  clave = ''
  if objeto.value():
    obj = articulo.objects.get(pk=objeto.value())
    clave = obj.clave
  html = """
    <input type="text" class="clave_input form-control" value="{0}">
      """.format(clave)
  return mark_safe(html)


@register.assignment_tag()
def iva(var, num , tipo):
  import humanize
  if tipo == 1:
    return humanize.intcomma( '%.2f' % (var / 1.16))
  if tipo == 2:
    return humanize.intcomma( '%.2f'%(var*num) )
  if tipo == 3:
    return humanize.intcomma( '%.2f'%(var + var*num) )
  return var
