

  /******************************
  **'fields_types' son los tipos de campos que se necesitan buscar y moficiar para error 'input,select'
  **'input_main' es una expresion regular ejemplo -> [id^="id_proveedor_articulo_set-"][id$="-clave_articulo"]
  ** que corresponde a todos los id que contienen un elemento extra entre las dos expresiones
  **'num_delete'  es el numero de elementos necesarios para que se elimine la fila
  **'num_error' es el numero de elementos necesarios para que marque como error la fila
  **'ev' es el evento para que no se genere submit
  **'error_field' es el id o class donde se coloca el mensaje de error ejemplo '#empty_field_proveedor'
  *******************************
  */
function search_empty_field(ev,input_main,num_delete,num_error,fields_types,error_field){
  var full_fields = 0
  $(input_main).each(function(){
    var row = $(this).closest("tr");
    var empties = 0
    row.find(fields_types).each(function(){
      if($.trim($(this).val()).length == 0){empties += 1;}
    });
    if(empties >= num_delete){
        deleteForm(row.find('td'),'#af', 'venta_detalle_set');
    }else if( empties >= num_error ){
      row.find(fields_types).css("border","1px solid red");
      full_fields = 1
      ev.preventDefault();
    }else{
      row.find(fields_types).css("border","");
    }
  });
  if( full_fields == 0 ){
    $(error_field).empty()
    return true
  }else{
    $(error_field).empty()
    $(error_field).append("<span style='color:red'><b> Es necesario llenar todos los campos </b></span>")
    return false
  }
}

function boton_accion(elemento,pk_model,ajax_data){
  if (confirm('¿Deseas eliminar el elemento?')) {
    var row = elemento.closest("tr");
    var $pk = row.find(".id_row").text();
    elemento.closest("tr").hide()
    var $pk_model = pk_model;
    $.ajax({
        data: {
          'method'        : ajax_data[0],
          'app'           : ajax_data[1],
          'app_relacion'  : ajax_data[2],
          'model'         : ajax_data[3],
          'model_relacion': ajax_data[4],
          'pk'            : $pk_model,
          'pk_relacion'   : $pk,
          'campo'         : ajax_data[5],
          'elimina_objeto': ajax_data[6],
        }
    }).done(function (response) {
    });
  }
  return false;
}

function boton_elimina_elemento(elemento, ajax_data){
    $.ajax({
        data: {
          'method'        : ajax_data[0],
          'app'           : 'base',
          'app_elemento'  : ajax_data[1],
          'model'         : ajax_data[2],
          'pk'            : ajax_data[3],
        }
    }).done(function (response) {
    });
}

function fix_table(fields,size,prefix,delete_size){
  var i = 0
  if(delete_size == 1){
    $.each(fields,function(){
      var td =".td_"+prefix+"_"+fields[i]
      var th =".th_"+prefix+"_"+fields[i]
      $(td).removeAttr( 'style' );
      $(th).removeAttr( 'style' );
      i ++;
    });
  }else{
    $.each(fields,function(){
      var td =".td_"+prefix+"_"+fields[i]
      var th =".th_"+prefix+"_"+fields[i]
      $(td).css('width',$(th).width()+parseInt(size[i]))
      $(th).css('width',$(td).width())
      i ++;
    });
  }
}

function fix_table_porcent(fields,size,prefix,delete_size){
  var i = 0
  var tbody ="#m2m_tbody_"+prefix
  var size_table = $(tbody).width()
  if(delete_size == 1){
    $.each(fields,function(){
      var td =".td_"+prefix+"_"+fields[i]
      var th =".th_"+prefix+"_"+fields[i]
      $(td).removeAttr( 'width' );
      $(th).removeAttr( 'width' );
      i ++;
    });
  }else{
    $.each(fields,function(){
      var td =".td_"+prefix+"_"+fields[i]
      var th =".th_"+prefix+"_"+fields[i]

      $(td).attr('width',size_table*parseFloat(size[i]))
      $(th).attr('width',size_table*parseFloat(size[i]))
      i ++;
    });
  }
}

function currency(num,decimal){
   "use strict";
   if(decimal === undefined || decimal === null) {
     decimal = 2;
   }
   var tmp = parseFloat(num).toFixed(decimal).replace(/(\d)(?=(\d{3})+\.)/g, '$1, ');
   return '$ '+tmp;
}

function invert_currency(elements){
  $(elements).each(function(i,val) {
    $(this).val($(this).val().replace(",","").replace("$","").replace(/ /g,''))
  });

}