#!/usr/bin/python

import MySQLdb
import sys,os
import json
from datetime import datetime
reload(sys)
sys.setdefaultencoding("utf-8")

db_host = "localhost"
db_users = "root"
db_password = "21Divox!="
db_db   = "fbasicas_back"
resultado =''
alumnos = []
padre_obj=[]
conceptos_obj=[]

conn = MySQLdb.connect(
  host= db_host,
  user=db_users,
  passwd=db_password,
  db=db_db)
connector = conn.cursor()

#Se optiene la informacion de los padres

sql_padre="""
SELECT 
PADRE.ID, 
PERSONA.NOMBRE,
PERSONA.PATERNO, 
PERSONA.MATERNO,
PERSONA.LUGAR_NACIMIENTO,
IFNULL(PERSONA.CURP,'N/C') AS CURP,
PERSONA.FECHA_NACIMIENTO,
DIRECCION.CALLE,
DIRECCION.NUMERO,
DIRECCION.COLONIA,
DIRECCION.CP,
DIRECCION.POBLACION,
DIRECCION.ENTIDAD_FEDERATIVA,
DIRECCION.MUNICIPIO 
from PERSONA 
INNER JOIN PADRE on(PERSONA.ID = PADRE.PERSONA_ID) 
INNER JOIN DIRECCION on (PERSONA.DIRECCION_ID = DIRECCION.ID)"""
connector.execute(sql_padre) 
resultado_padre = list(connector.fetchall())

for padre in resultado_padre:
  if str(padre[10]) == '':
    tmp_cp=58200
  else:
    tmp_cp = padre[10]
  obj_padre={
    'model':'catalogo.persona',
    'pk':padre[0],
    'fields':{
      'nombre':padre[1],
      'paterno':padre[2],
      'materno':padre[3],
      'lugar_de_nacimiento':padre[4],
      'curp':padre[5],
      'fecha_de_nacimiento':datetime.strftime(padre[6],"%Y-%m-%d") if str(padre[6])=='NoneType' else datetime.now().strftime("%Y-%m-%d"),
      'calle':padre[7],
      'numero':padre[8],
      'colonia':padre[9],
      'cp':tmp_cp,
      'poblacion':padre[11],
      'municipio':padre[12],
      'entidad_federativa':padre[13],
      'telefono_casa':'',
      'telefono_celular':'',
      'email':'email@email.com',
      'tipo':'0'
    }
  }
  padre_obj.append(obj_padre)

with open('backup/padres.json', 'w') as outfile:
  json.dump(padre_obj, outfile, sort_keys = True, indent = 4,ensure_ascii=False)




# Se optiene informacion sobre los alumnos y sus referencias
sql = """ SELECT 
ALUMNO.ID, 
ALUMNO.FECHA_INGRESO, 
PERSONA.NOMBRE, 
PERSONA.PATERNO, 
PERSONA.MATERNO, 
PERSONA.FECHA_NACIMIENTO, 
PERSONA.LUGAR_NACIMIENTO, 
ALUMNO.MATRICULA, 
ALUMNO.PLAZA, 
ALUMNO.EQUIPO, 
ALUMNO.RAMA, 
ALUMNO.HERMANO, 
ALUMNO.PADRE_ID, 
ALUMNO.PADRE_ID, 
DIRECCION.CALLE, 
DIRECCION.NUMERO, 
DIRECCION.COLONIA, 
DIRECCION.CP, 
DIRECCION.POBLACION, 
DIRECCION.ENTIDAD_FEDERATIVA, 
DIRECCION.MUNICIPIO, 
ALUMNO.STATUS,
ALUMNO_REFERENCIA.REFERENCIA,
ALUMNO_REFERENCIA.DESCRIPCION,
ALUMNO_REFERENCIA.ID
from PERSONA 
INNER JOIN ALUMNO on(PERSONA.ID = ALUMNO.PERSONA_ID) 
INNER JOIN DIRECCION on (PERSONA.DIRECCION_ID = DIRECCION.ID) 
INNER JOIN ALUMNO_REFERENCIA on (ALUMNO.ID = ALUMNO_REFERENCIA.ALUMNO_ID)"""
connector.execute(sql) 
resultado = list(connector.fetchall())

#Se arma json para alumnos y referencias

for i in resultado:
  if i[11]=='N':
    tmp_hermano='0'
  else:
    tmp_hermano='1'
  i= list(i)
  if i[21] =='B':
    tmp_status = '0'
  else:
    tmp_status = '1'
  if i[17] == '.':
    tmp_cp=58200
  else:
    tmp_cp=i[17]
  obj = {
    'model':'catalogo.alumno',
    'pk':i[0],
    'fields':{
      'fecha_de_ingreso':datetime.strftime(i[1],"%Y-%m-%d"),
      'nombre':i[2],
      'paterno':i[3],
      'materno':i[4],
      'fecha_de_nacimiento':datetime.strftime(i[5],"%Y-%m-%d") if str(i[5])=='NoneType' else datetime.now().strftime("%Y-%m-%d"),
      'lugar_de_nacimiento':i[6],
      'ant':'16',
      'matricula':str(i[7]).zfill(4),
      'plaza':i[8],
      'equipo':i[9],
      'rama':i[10],
      'hermano_institucion':tmp_hermano,
      'padre':i[12],
      'emergencia':i[13],
      'calle':i[14],
      'no':i[15],
      'colonia':i[16],
      'cp':tmp_cp,
      'poblacion':i[18],
      'municipio':i[19],
      'entidad_federativa':i[20],
      'estatus':tmp_status,
      'ciclo_escolar':'6'
    }
  }
  obj_referencia={
    'model':'catalogo.referencias',
    'pk':i[24],
    'fields':{
      'alumno':i[0],
      'referencia':i[22].strip(),
      'descripcion':i[23].strip().upper(),
    }
  }
  alumnos.append(obj)
  alumnos.append(obj_referencia)

with open('backup/data.json', 'w') as outfile:
  json.dump(alumnos, outfile, sort_keys = True, indent = 4,ensure_ascii=False)


#Se optendran todos los conceptos
sql="""
SELECT 
CAT_CONCEPTO.ID,
CAT_CONCEPTO.CLAVE,
CAT_CONCEPTO.NOMBRE,
CAT_CONCEPTO.DESCRIPCION,
CAT_CONCEPTO.TIPO,
CAT_CONCEPTO.PERIODICIDAD,
CAT_CONCEPTO.IMPORTE,
CAT_CONCEPTO.FORMULA,
CAT_CONCEPTO.STATUS
FROM CAT_CONCEPTO"""

connector.execute(sql) 
concepto = list(connector.fetchall())

for i in concepto:
  if i[8] == 'A':
    tmp_status='1'
  else:
    tmp_status='0'

  obj_concepto={
    'model':'catalogo.concepto',
    'pk':i[0],
    'fields':{
      'clave':i[1],
      'nombre':i[2],
      'descripcion':i[3],
      'tipo':i[4],
      'tipo_de_cargo':i[5],
      'importe':i[6],
      'formula':i[7],
      'estatus':tmp_status,
      }
    }
  conceptos_obj.append(obj_concepto)

with open('backup/data_concepto.json', 'w') as outfile:
  json.dump(conceptos_obj, outfile, sort_keys = True, indent = 4,ensure_ascii=False)


# se obtiene la informacion de las categorias

sql_categoria="""
SELECT 
CATEGORIA.ID,
CATEGORIA.NOMBRE,
CATEGORIA.DESCRIPCION,
CATEGORIA.CUPO_MAXIMO,
CATEGORIA.STATUS
FROM CATEGORIA"""

connector.execute(sql_categoria) 
categoria = list(connector.fetchall())
categoria_obj=[]
for i in categoria:
  if i[4] =='A':
    tmp_estatus ='1'
  elif i[4] =='B':
    tmp_estatus ='0'
  else:
    tmp_estatus ='0'
  obj_categoria={
  'model':'catalogo.categoria',
  'pk':i[0],
  'fields':{
      'nombre':i[1],
      'descripcion':i[2],
      'cupo_maximo':i[3],
      'estatus':tmp_estatus,
      'ciclo_escolar':'6',
    }
  }
  categoria_obj.append(obj_categoria)
with open('backup/data_categoria.json', 'w') as outfile:
  json.dump(categoria_obj, outfile, sort_keys = True, indent = 4,ensure_ascii=False)


#sacar todos los inscritos
sql_inscritos="""
SELECT
IFNULL(alm.ID,''),
alm.FECHA,
IFNULL(ALUMNO.ID,''),
IFNULL(alm.CATEGORIA_ID,''),
IFNULL(PERSONA.NOMBRE,''),
IFNULL(PERSONA.PATERNO,''),
IFNULL(PERSONA.MATERNO,''),
PERSONA.FECHA_NACIMIENTO,
IFNULL(PERSONA.LUGAR_NACIMIENTO,''),
IFNULL(PERSONA.CURP,''),
IFNULL(ALUMNO.MATRICULA,''),
IFNULL(ALUMNO.PLAZA,''),
IFNULL(ALUMNO.EQUIPO,''),
IFNULL(ALUMNO.RAMA,''),
IFNULL(DIRECCION.CALLE,''),
IFNULL(DIRECCION.NUMERO,''),
IFNULL(DIRECCION.COLONIA,''),
IFNULL(DIRECCION.CP,''),
IFNULL(DIRECCION.POBLACION,''),
IFNULL(DIRECCION.ENTIDAD_FEDERATIVA,''),
IFNULL(DIRECCION.MUNICIPIO,''),
IFNULL(alm.ESCUELA,''),
IFNULL(alm.NIVEL_EDUCATIVO,''),
IFNULL(alm.TURNO,''),
IFNULL(alm.GRADO,''),
IFNULL(alm.GRUPO,''),
IFNULL(ALUMNO.PADRE_ID,''),
IFNULL(ALUMNO.REFERENCIA_EMERGENCIA_ID,''),
IFNULL(alm.OBSERVACIONES,''),
IFNULL(alm.DOC_ACTA_NACIMIENTO,''),
IFNULL(alm.DOC_CURP,''),
IFNULL(alm.DOC_FOTOGRAFIA,''),
IFNULL(alm.DOC_CERTIFICADO,'')
FROM ALUMNO_FORMATO_INSCRIPCION AS alm INNER JOIN ALUMNO ON (ALUMNO.ID=alm.ALUMNO_ID) 
INNER JOIN PERSONA ON (PERSONA.ID=ALUMNO.PERSONA_ID) 
INNER JOIN DIRECCION ON (PERSONA.DIRECCION_ID = DIRECCION.ID)"""

connector.execute(sql_inscritos) 
inscrito = list(connector.fetchall())
inscrito_obj=[]

for i in inscrito:
  sql_tmp ="""SELECT 
    PERSONA.NOMBRE,
    PERSONA.PATERNO,
    PERSONA.MATERNO,
    PERSONA.FECHA_NACIMIENTO,
    PERSONA.LUGAR_NACIMIENTO,
    IFNULL(PERSONA.CURP,''),
    DIRECCION.CALLE,
    DIRECCION.NUMERO,
    DIRECCION.COLONIA,
    DIRECCION.CP,
    DIRECCION.POBLACION,
    DIRECCION.ENTIDAD_FEDERATIVA,
    DIRECCION.MUNICIPIO
    FROM PERSONA INNER JOIN DIRECCION ON (PERSONA.DIRECCION_ID = DIRECCION.ID)
    WHERE PERSONA.ID={0}
  """.format(i[26])
  connector.execute(sql_tmp) 
  padre = list(connector.fetchall())
  
  if i[29] == 'S':
    tmp_insc = '1'
  else:
    tmp_insc = '0'
  if i[30] == 'S':
    tmp_curp = '1'
  else:
    tmp_curp = '0'
  if i[31] == 'S':
    tmp_fot = '1'
  else:
    tmp_fot = '0'
  if i[32] == 'S':
    tmp_cer = '1'
  else:
    tmp_cer = '0'

  if str(i[23]) == 'Matutino':
    turno_tmp = '1'
  else:
    turno_tmp = '2'
  obj_inscripcion={
    'model':'inscripcion.inscripcion',
    'pk':i[0],
    'fields':{
      'fecha_inscripcion':datetime.strftime(i[1],"%Y-%m-%d"),
      'alumno':i[2],
      'categoria':i[3],
      'ciclo':'6',
      'alumno_nombre':i[4],
      'alumno_paterno':i[5],
      'alumno_materno':i[6],
      'alumno_fecha_de_nacimiento':datetime.strftime(i[7],"%Y-%m-%d") if str(i[7])=='NoneType' else datetime.now().strftime("%Y-%m-%d"),
      'alumno_lugar_de_nacimiento':i[8],
      'alumno_curp':i[9],
      'alumno_matricula':i[10],
      'alumno_plaza':i[11],
      'alumno_equipo':i[12],
      'alumno_rama':i[13],
      'alumno_calle':i[14],
      'alumno_no':i[15],
      'alumno_colonia':i[16],
      'alumno_cp':i[17] if str(i[17]) != '.' else 58000,
      'alumno_poblacion':i[18],
      'alumno_municipio':i[29],
      'alumno_entidad_federativa':i[20],
      'alumno_tel_casa':'',
      'alumno_tel_celular':'',
      'alumno_email':'',
      'alumno_nombre_colegio':i[21],
      'alumno_nivel_educativo':i[22],
      'alumno_turno':turno_tmp,
      'alumno_grado':i[24],
      'alumno_grupo':i[25],
      'padre_nombre':padre[0][0] if padre else '',
      'padre_paterno':padre[0][1] if padre else '',
      'padre_materno':padre[0][2] if padre else '',
      'padre_lugar_de_nacimiento':padre[0][4] if padre else '',
      'padre_curp':padre[0][5] if padre else '',
      'padre_fecha_de_nacimiento':datetime.strftime(padre[0][3],"%Y-%m-%d") if padre else datetime.now().strftime("%Y-%m-%d"),
      'padre_calle':padre[0][6] if padre else '',
      'padre_numero':padre[0][7] if padre else '',
      'padre_colonia':padre[0][8] if padre else '',
      'padre_cp':padre[0][9] if padre else 58200,
      'padre_poblacion':padre[0][10] if padre else '',
      'padre_municipio':padre[0][11] if padre else '',
      'padre_entidad_federativa':padre[0][12] if padre else '',
      'padre_telefono_casa':'',
      'padre_telefono_celular':'',
      'padre_email':'',
      'emergencia_nombre':padre[0][0]if padre else '',
      'emergencia_paterno':padre[0][1]if padre else '',
      'emergencia_materno':padre[0][2]if padre else '',
      'emergencia_lugar_de_nacimiento':padre[0][4]if padre else '',
      'emergencia_curp':padre[0][5]if padre else '',
      'emergencia_fecha_de_nacimiento':datetime.strftime(padre[0][3],"%Y-%m-%d")if padre else datetime.now().strftime("%Y-%m-%d"),
      'emergencia_calle':padre[0][6]if padre else '',
      'emergencia_numero':padre[0][7]if padre else '',
      'emergencia_colonia':padre[0][8]if padre else '',
      'emergencia_cp':padre[0][9]if padre else 58200,
      'emergencia_poblacion':padre[0][10]if padre else '',
      'emergencia_municipio':padre[0][11]if padre else '',
      'emergencia_entidad_federativa':padre[0][12]if padre else '',
      'emergencia_telefono_casa':'',
      'emergencia_telefono_celular':'',
      'emergencia_email':'',
      'observaciones':i[28],
      'doc_acta':tmp_insc,
      'doc_curp':tmp_curp,
      'doc_fotografias':tmp_fot,
      'doc_certificado':tmp_cer,
    }
  }
  inscrito_obj.append(obj_inscripcion)
with open('backup/inscritos.json', 'w') as outfile:
  json.dump(inscrito_obj, outfile, sort_keys = True, indent = 4,ensure_ascii=False)


#obtener todos los movimientos

sql_movimiento="""
SELECT 
MOVIMIENTO.ID,
MOVIMIENTO.FECHA,
ALUMNO.ID,
CAT_CONCEPTO.ID,
MOVIMIENTO.NO_OPERACION,
MOVIMIENTO.REFERENCIA,
MOVIMIENTO.MONTO,
CAT_CONCEPTO.DESCRIPCION
FROM MOVIMIENTO INNER JOIN CAT_CONCEPTO on (MOVIMIENTO.CAT_CONCEPTO_ID = CAT_CONCEPTO.ID) 
INNER JOIN ALUMNO ON (MOVIMIENTO.ALUMNO_ID = ALUMNO.ID)
"""
connector.execute(sql_movimiento) 
mov = list(connector.fetchall())
movimientos_obj =[]
for i in mov:
  obj_movimientos={
  'model':'reporte.movimiento',
  'pk':i[0],
  'fields':{
  'fecha_registro':datetime.strftime(i[1],"%Y-%m-%d"),
  'ciclo':'6',
  'alumno':i[2],
  'concepto':i[3],
  'folio':i[4],
  'referencia':i[5],
  'monto':i[6],
  'archivo':'',
  'descripcion':i[7],
    }
  }
  movimientos_obj.append(obj_movimientos)
with open('backup/movimientos.json', 'w') as outfile:
  json.dump(movimientos_obj, outfile, sort_keys = True, indent = 4,ensure_ascii=False)
