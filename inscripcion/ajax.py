from catalogo.models import alumno
from inscripcion.models import inscripcion
def get_alumno(request):
  al = ''
  params=''
  pk = request.POST.get('id',None)
  cicl_esc = None
  ciclo_tmp = 0
  if pk:
    al    = alumno.objects.get(pk=pk)
    cicl_esc = inscripcion.objects.filter(alumno=al)
  if cicl_esc:
    ciclo_tmp = al.ciclo_escolar.pk

  params={
  'fecha_de_ingreso'    :al.fecha_de_ingreso,
  'nombre'              :al.nombre,   
  'paterno'             :al.paterno,
  'ciclo'               :ciclo_tmp,
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
  return params

def get_categoria(request):
  from catalogo.models import categoria as categ
  from inscripcion.models import inscripcion
  cat       = request.POST.get('cat')
  categoria = categ.objects.get(pk=cat)
  alumnos   = inscripcion.objects.filter(categoria=categoria)
  inscritos = len(alumnos)
  maximo    = categoria.cupo_maximo
  parametros={
  'inscrito':inscritos,
  'cupo':maximo,
  }
  return parametros


def get_categoria_ciclo(request):
  from catalogo.models import categoria
  ciclo = request.POST.get('ciclo')
  categoria_list =[]
  categ = categoria.objects.filter(ciclo_escolar=ciclo)
  for i in categ:
    alumnos   = inscripcion.objects.filter(categoria=i)
    inscritos = len(alumnos)
    maximo    = i.cupo_maximo
    if inscritos < maximo:
      categoria_list.append(i.pk)
  parametros={
   'categoria':categoria_list
   }
  return parametros





























