# -*- coding:UTF-8 -*-
import MySQLdb
import traceback
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

db = MySQLdb.connect(
        host='localhost',
        user='root',
        passwd='046797993',
        db='DVX_TORQUEMEX'
    )

cur  = db.cursor(MySQLdb.cursors.DictCursor)
cur2 = db.cursor(MySQLdb.cursors.DictCursor)
#cur.execute("SELECT * FROM ARTICULOS")

CLASES = {
    'transmision'   : 1,
    'direccion'     : 2,
    'fletes'        : 3,
    'varios'        : 4,
    'materia_prima' : 5,
    'lubricantes'   : 6
}

TIPO_ACTIVACION = {
    'activado'    : 1,
    'existencia'  : 2,
    'desactivado' : 3
}

USUARIOS              = {}
SUBCLASES             = {}
UNIDADES_MEDIDA       = {}
MARCAS_ARTICULOS      = {}
PROVEEDORES           = {}
PROVEEDORES_NOMBRE    = {}
METODOS_PAGO          = {}
CLIENTES              = {}
ARTICULOS             = {}
TRANSMISIONES_DETALLE = {}
FACTURACION           = {}

print "["

print """
{
    "model":"catalogo.clase",
    "pk":1,
    "fields":{
        "descripcion":"Transmision",
        "activo":true
    }
},
"""

print """
{
    "model":"catalogo.clase",
    "pk":2,
    "fields":{
        "descripcion":"Direccion",
        "activo":true
    }
},
"""

print """
{
    "model":"catalogo.clase",
    "pk":3,
    "fields":{
        "descripcion":"Fletes",
        "activo":true
    }
},
"""

print """
{
    "model":"catalogo.clase",
    "pk":4,
    "fields":{
        "descripcion":"Varios",
        "activo":true
    }
},
"""

print """
{
    "model":"catalogo.clase",
    "pk":5,
    "fields":{
        "descripcion":"Materia Prima",
        "activo":true
    }
},
"""

print """
{
    "model":"catalogo.clase",
    "pk":6,
    "fields":{
        "descripcion":"Lubricantes",
        "activo":true
    }
},
"""

cur.execute("SELECT USUARIO.ID,USUARIO.USUARIO,PERSONA.NOMBRE,PERSONA.PATERNO,PERSONA.MATERNO FROM USUARIO,PERSONA WHERE USUARIO.PERSONA_ID=PERSONA.ID")

for row in cur.fetchall():

    dato = """
    {{
        "model": "usuario.usuario",
        "pk": {0},
        "fields": {{
            "username": "{1}",
            "first_name": "{2}",
            "last_name": "{3}",
            "email": "",
            "avatar": null,
            "metodo_autenticacion": "password"
            }}
        }},
    """.format(
            row['ID'],
            row['USUARIO'],
            row['NOMBRE'],
            "%s %s" % (row['PATERNO'],row['MATERNO'])
        )
    
    print dato

cur.execute("SELECT * FROM SUBCLASES")
indice = 0

for row in cur.fetchall():
    indice += 1
    SUBCLASES[str(row['pk_subclase'])] = indice

    indice_clase = CLASES[str(row['clase'])]

    dato = """
    {{
        "model": "catalogo.subclase",
        "pk": {0},
        "fields": {{
            "clase": "{1}",
            "descripcion": "{2}",
            "activo": true
            }}
        }},
    """.format(
            indice,
            indice_clase,
            str(row['pk_subclase']),
        )
    
    print dato

# Unidades de Medida

dato = ""
cur.execute("SELECT * FROM CAT_UNIDADES_MEDIDA")
indice = 0

for row in cur.fetchall():
    indice += 1
    UNIDADES_MEDIDA[str(row['pk_unidad_medida'])] = indice

    dato = """
    {{
        "model": "catalogo.unidad_medida",
        "pk": {0},
        "fields": {{
            "descripcion": "{1}",
            "activo": true
            }}
        }},
    """.format(
            indice,
            str(row['pk_unidad_medida']),
        )
    
    print dato

# Marcas Articulos
dato = ""
cur.execute("SELECT * FROM MARCAS_ARTICULOS")
indice = 0

for row in cur.fetchall():
    indice += 1
    MARCAS_ARTICULOS[str(row['pk_marca'])] = indice

    dato = """
    {{
        "model": "catalogo.marca_articulo",
        "pk": {0},
        "fields": {{
            "descripcion": "{1}",
            "activo": true
            }}
        }},
    """.format(
            indice,
            str(row['pk_marca']),
        )
    
    print dato

# Metodos de Pago
dato = ""
cur.execute("SELECT * FROM CAT_METODO_PAGO")
indice = 0

for row in cur.fetchall():
    indice += 1
    METODOS_PAGO[str(row['pk_metodo'])] = indice

    dato = """
    {{
        "model": "catalogo.metodo_pago",
        "pk": {0},
        "fields": {{
            "descripcion": "{1}",
            "activo": true
            }}
        }},
    """.format(
            indice,
            str(row['pk_metodo'])
        )
    
    print dato

# Clientes
dato = ""
cur.execute("SELECT * FROM CLIENTES")
indice = 0

for row in cur.fetchall():
    indice += 1
    CLIENTES[str(row['pk_rfc']).strip()] = indice

    dato = """
    {{
        "model": "catalogo.cliente",
        "pk": {0},
        "fields": {{
            "rfc": "{1}",
            "razon_social": "{2}",
            "contacto": "{3}",
            "direcciones": [],
            "email": "{4}",
            "telefono": "{5}",
            "activo": true
            }}
        }},
    """.format(
            indice,
            str(row['pk_rfc']).strip(),
            str(row['razon_social']),
            str(row['responsable']),
            str(row['correo']),
            str(row['telefono']).decode('utf-8')
        )
    
    print dato

# Proveedores
dato = ""
cur.execute("SELECT * FROM PROVEEDORES")
indice = 0

for row in cur.fetchall():
    indice += 1
    PROVEEDORES[str(row['pk_rfc'])]                      = indice
    PROVEEDORES_NOMBRE[str(row['nombre_comercial']).strip()] = indice
    
    dato = """
    {{
        "model": "catalogo.proveedor",
        "pk": {0},
        "fields": {{
            "rfc": "{1}",
            "razon_social": "{2}",
            "contacto": "",
            "email": "",
            "telefono": "",
            "direcciones":[],
            "activo": true
            }}
        }},
    """.format(
            indice,
            str(row['pk_rfc']),
            str(row['razon_social']),
        )
    
    print dato

# Grupos de Transmisiones

dato = ""
cur.execute("SELECT * FROM GRUPOS_TRANSMISIONES")

for row in cur.fetchall():
    dato = """
    {{
        "model": "catalogo.grupo_transmision",
        "pk": {0},
        "fields": {{
            "descripcion": "{1}",
            "activo": true
            }}
        }},
    """.format(
            row['pk_grupo'],
            str(row['descripcion']),
        )
    
    print dato

# Grupos de Transmision Detalle
dato = ""
cur.execute("SELECT * FROM TRANSMISIONES_GRUPOS_TRANSMISIONES_REL")
indice = 0

for row in cur.fetchall():
    indice += 1

    TRANSMISIONES_DETALLE[str(row['fk_transmision']).strip()] = indice

    dato = """
    {{
        "model": "catalogo.grupo_transmision_detalle",
        "pk": {0},
        "fields": {{
            "grupo_transmision": "{1}",
            "descripcion": "{2}",
            "activo": true
            }}
        }},
    """.format(
            indice,
            row['fk_grupo'],
            str(row['fk_transmision']),
        )
    
    print dato


# Articulos
dato = ""
cur.execute("SELECT * FROM ARTICULOS")
indice = 0
for row in cur.fetchall():
    indice = indice+1
    ARTICULOS[str(row['pk_articulo']).strip()] = indice
    
    try:
        marca_articulo = MARCAS_ARTICULOS.get(str(row['marca']),"1")
    except:
        marca_articulo = "1"
    
    try:
        subclase = SUBCLASES.get(str(row['fk_subclase']),"1")
    except:
        subclase = "1"

    observacion = ""
    if row['observaciones'] is not None:
        observacion = str(row['observaciones'])
    
    medida = ""
    if row['medida'] is not None:
        medida = str(row['medida'])
    
    retorno_casco = "false"
    if row['retorno_cascos'] == "1":
        retorno_casco = "true"
    
    devolucion = "false"
    if row['devolucion'] == "1":
        devolucion = "true"

    cur2.execute("SELECT * FROM TRANSMISIONES WHERE fk_articulo='%s' " % (str(row['pk_articulo']).strip()))
    transmisiones = []
    for row2 in cur2.fetchall():
        transmisiones.append(TRANSMISIONES_DETALLE[str(row2['tipo']).strip()])

    dato = """
    {{
        "model": "bodega.articulo",
        "pk": {0},
        "fields": {{
            "clave": "{1}",
            "descripcion": "{2}",
            "imagen": null,
            "clase": {3},
            "subclase": {4},
            "requiere_casco": {5},
            "marca": {6},
            "ubicacion_almacen": "{7}",
            "tipo_activacion": {8},
            "maximo_inventario": {9},
            "minimo_inventario": {10},
            "peso": "{11}",
            "precio_default": {12},
            "medida": "{13}",
            "unidad_medida": {14},
            "remate": {15},
            "devolucion": {16},
            "costo": {17},
            "observacion": "{18}",
            "grupos_transmision_detalles": {19}
            }}
        }},
    """.format(
            indice,
            str(row['pk_articulo']),
            unicode(row['descripcion'],errors='replace').decode('utf-8'),
            CLASES[str(row['clase'])],
            subclase,
            retorno_casco,
            marca_articulo,
            str(row['ubicacion']),
            TIPO_ACTIVACION[str(row['activacion'])],
            int(row['maximo_inventario']),
            int(row['minimo_inventario']),
            str(row['peso']),
            float(row['precio_inicial']),
            medida,
            UNIDADES_MEDIDA[str(row['fk_unidad_medida'])],
            'true',
            devolucion,
            float(row['costo_inicial']),
            unicode(str(observacion).decode('utf8','ignore')).replace('"',''),
            json.dumps(transmisiones),
        )
    
    print dato

# Componentes - Articulos
dato = ""
cur.execute("SELECT * FROM ARTICULOS_COMPUESTOS_SELF")
indice = 0

for row in cur.fetchall():
    indice = indice+1
    
    componente = ""
    try:
        componente = ARTICULOS[str(row['fk_componente']).strip()]
    except:
        componente = ARTICULOS[str(row['fk_componente']).strip().upper()]

    dato = """
    {{
        "model": "bodega.componente",
        "pk": {0},
        "fields": {{
            "componentes": "{1}",
            "articulos": "{2}",
            "cantidad": "{3}"
            }}
        }},
    """.format(
            indice,
            ARTICULOS[str(row['fk_articulo']).strip()],
            componente,
            int(float(row['cantidad'])),
        )
    
    print dato

# Proveedores - Articulos
dato = ""
cur.execute("SELECT * FROM ARTICULOS_PROVEEDORES_REL")
indice = 0

for row in cur.fetchall():
    indice = indice+1
    
    tmp_articulo = ""
    try:
        tmp_articulo = ARTICULOS[str(row['fk_articulo']).strip()]
    except:
        continue

    dato = """
    {{
        "model": "bodega.proveedor_articulo",
        "pk": {0},
        "fields": {{
            "proveedor": "{1}",
            "articulo": "{2}",
            "clave_articulo": "{3}",
            "activado":true
            }}
        }},
    """.format(
            indice,
            PROVEEDORES[str(row['fk_rfc']).strip()],
            tmp_articulo,
            str(row['id']).strip(),
        )
    
    print dato

# Cotizacion
dato = ""
cur.execute("SELECT * FROM ORDENES")
for row in cur.fetchall():
    tmp_cliente = 1
    try:
      tmp_cliente = CLIENTES[str(row['cliente']).strip()]
    except:
      pass

    dato = """
    {{
        "model": "venta.cotizacion",
        "pk": {0},
        "fields": {{
            "fecha": "{1}",
            "usuario_id": "{2}",
            "cliente_id": "{3}",
            "metodo_pago_id": "1",
            "subtotal": "{4}",
            "iva": "{5}",
            "total": "{6}",
            "activo": true
            }}
        }},
    """.format(
            row['pk_orden'],
            row['fecha'],
            row['vendedor'],
            tmp_cliente,
            0,
            0,
            0
        )
    
    print dato

# Cotizacion Detalle
dato = ""
cur.execute("SELECT * FROM ARTICULOS_ORDENES_REL")
indice = 0
for row in cur.fetchall():
    indice = indice+1
    
    tmp_articulo = 1
    try:
      tmp_articulo = ARTICULOS[str(row['fk_articulo']).strip()]
    except:
      pass

    dato = """
    {{
        "model": "venta.cotizacion_detalle",
        "pk": {0},
        "fields": {{
            "cotizacion_id": "{1}",
            "articulo_id": "{2}",
            "cantidad": "{3}",
            "precio_unitario": "{4}",
            "importe": "{5}"
            }}
        }},
    """.format(
            indice,
            row['fk_orden'],
            tmp_articulo,
            row['cantidad'],
            row['precio_final'],
            0
        )
    
    print dato

# Ventas
dato = ""
cur.execute("SELECT * FROM VENTAS")

for row in cur.fetchall():
    tmp_cliente = 1
    try:
      tmp_cliente = CLIENTES[str(row['fk_rfc']).strip()]
    except:
      pass
    
    tmp_metodo_pago = 1
    try:
      tmp_metodo_pago = METODOS_PAGO[str(row['fk_metodo_pago']).strip()]
    except:
      pass
    
    tmp_entrego = row['entrego'] 
    if not tmp_entrego:
      tmp_entrego = 0

    dato = """
    {{
        "model": "venta.venta",
        "pk": {0},
        "fields": {{
            "fecha": "{1}",
            "usuario": "{2}",
            "cliente": "{3}",
            "metodo_pago": "{4}",
            "cotizacion_id": null,
            "observacion": "{5}",
            "subtotal": "{6}",
            "iva": "{7}",
            "total": "{8}",
            "recibi": "{9}",
            "cambio": "0",
            "activo": true
            }}
        }},
    """.format(
            row['pk_venta'],
            row['timestamp'],
            row['vendedor'],
            tmp_cliente,
            tmp_metodo_pago,
            row['observaciones'],
            row['subtotal'],
            row['iva'],
            row['total'],
            tmp_entrego
        )
    
    print dato

# Venta Detalle
dato = ""
cur.execute("SELECT * FROM ARTICULOS_VENTAS_REL")
indice = 0

for row in cur.fetchall():
    indice = indice+1
    
    importe = row['cantidad']*row['precio']
    
    tmp_articulo = ""
    try:
        tmp_articulo = ARTICULOS[str(row['fk_articulo']).strip()]
    except:
        tmp_articulo = ARTICULOS[str(row['fk_articulo']).strip().upper()]

    dato = """
    {{
        "model": "venta.venta_detalle",
        "pk": {0},
        "fields": {{
            "venta": "{1}",
            "articulo": "{2}",
            "cantidad": "{3}",
            "precio_unitario": "{4}",
            "importe": {5},
            "entrega": "{6}",
            "activo": true
            }}
        }},
    """.format(
            indice,
            row['fk_venta'],
            tmp_articulo,
            row['cantidad'],
            row['precio'],
            importe,
            row['entregado']
        )
    
    print dato

# Ingresos
dato = ""
cur.execute("SELECT * FROM INGRESOS")
for row in cur.fetchall():
    dato = """
    {{
        "model": "bodega.ingreso",
        "pk": {0},
        "fields": {{
            "fecha": "{1}",
            "usuario":"{2}",
            "no_factura": "{3}",
            "proveedor": "{4}",
            "clase": "{5}",
            "subclase": {6},
            "total_factura": "{7}",
            "total_articulos": "{8}",
            "total_id": "{9}",
            "activo": true
            }}
        }},
    """.format(
            row['pk_ingreso'],
            row['fecha'],
            row['fk_usuario'],
            row['no_factura'],
            PROVEEDORES_NOMBRE[str(row['fk_proveedor']).strip()],
            1,
            1,
            0,
            int(row['no_articulos']),
            0
        )
    
    print dato

# Ingresos Detalle
dato = ""
cur.execute("SELECT * FROM LOTES")
indice = 0
for row in cur.fetchall():
    indice = indice+1
    
    tmp_cantidad = row['costo']
    if not tmp_cantidad:
        tmp_cantidad = 0

    dato = """
    {{
        "model": "bodega.ingreso_detalle",
        "pk": {0},
        "fields": {{
            "ingreso": "{1}",
            "articulo": "{2}",
            "cantidad": "{3}",
            "precio_unitario": "{4}",
            "restantes": {5}
            }}
        }},
    """.format(
            indice,
            row['fk_ingreso'],
            ARTICULOS[str(row['fk_articulo']).strip()],
            row['total'],
            tmp_cantidad,
            row['cantidad']
        )
    
    print dato

# Factura
dato = ""
cur.execute("SELECT * FROM FACTURA")
indice = 0
for row in cur.fetchall():
    indice = indice+1
    
    cadena = "%s%s%s" % (row['e_rfc'],row['folio'],row['serie'])
    FACTURACION[cadena] = indice

    tmp_total = row['total']
    if not tmp_total:
        tmp_total = 0
    
    tmp_descuento = row['descuento']
    if not tmp_descuento:
        tmp_descuento = 0
    
    tmp_tipo_cambio = row['tipo_cambio']
    if not tmp_tipo_cambio:
        tmp_tipo_cambio = 0
    
    tmp_condiciones_pago = row['condiciones_pago']
    if not tmp_condiciones_pago:
        tmp_condiciones_pago = ""
    
    tmp_e_cp = row['e_cp']
    if not tmp_e_cp:
        tmp_e_cp = ""
    
    tmp_r_cp = row['r_cp']
    if not tmp_r_cp:
        tmp_r_cp = ""
    
    tmp_e_nointerior = row['e_nointerior']
    if not tmp_e_nointerior:
        tmp_e_nointerior = ""
    
    tmp_r_localidad = row['r_localidad']
    if not tmp_r_localidad:
        tmp_r_localidad = ""
    
    tmp_r_nointerior = row['r_nointerior']
    if not tmp_r_nointerior:
        tmp_r_nointerior = ""
    
    tmp_observaciones = row['observaciones']
    if not tmp_observaciones:
        tmp_observaciones = ""

    dato = """
    {{
        "model": "facturacion.factura",
        "pk": {0},
        "fields": {{
            "version": "{1}",
            "tipo_comprobante": "{2}",
            "fecha": "{3}",
            "folio": "{4}",
            "serie": "{5}",
            "no_certificado": "{6}",
            "subtotal": "{7}",
            "descuento": "{8}",
            "total": "{9}",
            "moneda": "{10}",
            "tipo_cambio": "{11}",
            "metodo_pago": "{12}",
            "num_cta": "{13}",
            "condiciones_pago": "{14}",
            "forma_pago": "{15}",
            "lugar_expedicion": "{16}",
            "regimen_fiscal": "{17}",
            "e_nombre": "{18}",
            "e_rfc": "{19}",
            "e_calle":"{20}",
            "e_cp": "{21}",
            "e_colonia": "{22}",
            "e_estado": "{23}",
            "e_localidad": "{24}",
            "e_municipio": "{25}",
            "e_noexterior": "{26}",
            "e_nointerior": "{27}",
            "e_pais": "{28}",
            "r_nombre": "{29}",
            "r_rfc": "{30}",
            "r_calle":"{31}",
            "r_cp": "{32}",
            "r_colonia": "{33}",
            "r_estado": "{34}",
            "r_localidad": "{35}",
            "r_municipio": "{36}",
            "r_noexterior": "{37}",
            "r_nointerior": "{38}",
            "r_pais": "{39}",
            "fecha_timbrado": null,
            "uuid": null,
            "certificado_sat": null,
            "fecha_cancelacion": null,
            "acuse_cancelado": null,
            "observaciones": "{40}",
            "estado": {41}
            }}
        }},
    """.format(
            indice,
            row['version'],
            row['tipo_comprobante'],
            row['fecha'],
            row['folio'],
            row['serie'],
            row['no_certificado'],
            row['subtotal'],
            tmp_descuento,
            tmp_total,
            row['moneda'],
            tmp_tipo_cambio,
            row['metodo_pago'],
            row['num_cta'],
            tmp_condiciones_pago,
            row['forma_pago'],
            row['lugar_expedicion'],
            row['regimen_fiscal'],
            row['e_nombre'],
            row['e_rfc'],
            row['e_calle'],
            tmp_e_cp,
            row['e_colonia'],
            row['e_estado'],
            row['e_localidad'],
            row['e_municipio'],
            row['e_noexterior'],
            tmp_e_nointerior,
            row['r_pais'],
            row['r_nombre'],
            row['r_rfc'],
            row['r_calle'],
            tmp_r_cp,
            row['r_colonia'],
            row['r_estado'],
            tmp_r_localidad,
            row['r_municipio'],
            row['r_noexterior'],
            tmp_r_nointerior,
            row['r_pais'],
            tmp_observaciones,
            1
        )
    
    print dato

# Factura Detalle
dato = ""
cur.execute("SELECT * FROM FACTURA_DETALLE")
indice = 0
for row in cur.fetchall():
    indice = indice+1
    
    cadena = "%s%s%s" % (row['rfc'],row['folio'],row['serie'])
    
    tmp_precio_unitario = row['precio_unitario']
    if tmp_precio_unitario is None:
      tmp_precio_unitario = 0.0

    dato = """
    {{
        "model": "facturacion.factura_detalle",
        "pk": {0},
        "fields": {{
            "factura": "{1}",
            "cantidad": "{2}",
            "descripcion": "{3}",
            "unidad_medida": "{4}",
            "no_identificacion": "{5}",
            "precio_unitario": "{6}",
            "importe": "{7}"
            }}
        }},
    """.format(
            indice,
            FACTURACION[cadena],
            int(row['cantidad']),
            str(row['descripcion']),
            str(row['unidad_medida']),
            str(row['no_identificacion']),
            tmp_precio_unitario,
            row['total']
        )
    
    print dato

print "]"
