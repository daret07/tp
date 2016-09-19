from catalogo.models import alumno
def get_alumno(request):
  al = ''
  params=''
  pk = request.POST.get('id',None)
  if pk:
    al    = alumno.objects.get(pk=pk)
  params={
  'fecha_de_ingreso'    :al.fecha_de_ingreso,
  'nombre'              :al.nombre,   
  'paterno'             :al.paterno,
  'ciclo'               :al.ciclo_escolar.pk,
  'materno'             :al.materno,
  'fecha_de_nacimiento' :al.fecha_de_nacimiento,
  'lugar_de_nacimiento' :al.lugar_de_nacimiento,
  'matricula'           :al.matricula,
  'plaza'               :al.plaza,
  'equipo'              :al.equipo,
  'rama'                :al.rama,
  'hermano_institucion' :al.hermano_institucion,
  'padre'               :{'p_nombre':al.padre.nombre,
                          'p_paterno':al.padre.paterno,
                          'p_materno':al.padre.materno,
                          'p_lugar_de_nacimiento':al.padre.lugar_de_nacimiento,
                          'p_curp':al.padre.curp,
                          'p_fecha_de_nacimiento':al.padre.fecha_de_nacimiento,
                          'p_calle':al.padre.calle,
                          'p_numero':al.padre.numero,
                          'p_colonia':al.padre.colonia,
                          'p_cp':al.padre.cp,
                          'p_poblacion':al.padre.poblacion,
                          'p_municipio':al.padre.municipio,
                          'p_entidad_federativa':al.padre.entidad_federativa,
                          'p_telefono_casa':al.padre.telefono_casa,
                          'p_telefono_celular':al.padre.telefono_celular,
                          'p_email':al.padre.email,
                          'p_tipo':al.padre.tipo,},
  'emergencia'          :{
                          'em_nombre':al.emergencia.nombre,
                          'em_paterno':al.emergencia.paterno,
                          'em_materno':al.emergencia.materno,
                          'em_lugar_de_nacimiento':al.emergencia.lugar_de_nacimiento,
                          'em_curp':al.emergencia.curp,
                          'em_fecha_de_nacimiento':al.emergencia.fecha_de_nacimiento,
                          'em_calle':al.emergencia.calle,
                          'em_numero':al.emergencia.numero,
                          'em_colonia':al.emergencia.colonia,
                          'em_cp':al.emergencia.cp,
                          'em_poblacion':al.emergencia.poblacion,
                          'em_municipio':al.emergencia.municipio,
                          'em_entidad_federativa':al.emergencia.entidad_federativa,
                          'em_telefono_casa':al.emergencia.telefono_casa,
                          'em_telefono_celular':al.emergencia.telefono_celular,
                          'em_email':al.emergencia.email,
                          'em_tipo':al.emergencia.tipo,
                          },
  'calle'               :al.calle,
  'no'                  :al.no,
  'colonia'             :al.colonia,
  'cp'                  :al.cp,
  'poblacion'           :al.poblacion,
  'municipio'           :al.municipio,
  'entidad_federativa'  :al.entidad_federativa,
  'estatus'             :al.estatus,
  }
  print params
  return params



































