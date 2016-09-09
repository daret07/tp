/**
Metodo que detecta la re-carga de un modal, con la finalidad
de que sea totalmente transparente para el programador el
realizar esta operación
**/
function recarga(ev) {
  var contenido = $("#iframe_modal").contents().find("#contenido_modal").html();
  if (contenido !== "") {
    $("#contenido_modal").html(contenido);
  }
}

function modalGenerico(modelo,app){
  var modal_foreignkey = {
    'modal_modelo':modelo,
    'modal_app'   :app,
  }
  showModal('base','modal_generico',modal_foreignkey);
}

function loadCombo(elemento,app,method,pk,parametros){
  var ele = "#"+elemento;
  if( pk == '' ){
    $(ele).val(0)
    $(ele+" option").remove();
  }
  if(parseInt(pk)>=0){
    $.ajax({
      data:{
        'app'          : app,
        'method'       : method,
        'pk'           : pk,
        'parametros'   : parametros,
      }
    }).done(function(ev){
      $(ele+" option").remove();
      $(ele).append($("<option></option>").attr("value","").text("---------"));
      $(ele).find('option:eq(0)').prop('selected', true);
      $.each(ev.response,function(i,value){
        if(value[2] == undefined){
            value[2] = false;
        }
        var option =$("<option></option>")
          .attr("value",value[1])
          .text(value[0])

        if(value[2] == true){
            $(option).prop("selected",true);
        }
        $(ele).append(option);
      });
    });
  }
  $(ele).change();
}

/**
Metodo que permite abrir una ventana modal y mostrarla al usuario
TODO: Esa solución solamente es viable si se usa un solo modal.
Es decir, si es necesario utilizar mas de un modal en una misma pagina
no podremos utilizar dicha opcion.
**/
function showModal(app,modal,extra_params) {
  if (extra_params === undefined) {
    extra_params = {};
  }
  
  var parametros = {
    'app'   : app,
    'popup' : modal
  };
  
  jQuery.extend(parametros,extra_params);
  
  $.ajax({
    'url'      : _homeurl+'modal/',
    'method'   : 'POST',
    'cache'    : false,
    'async'    : true,
    'dataType' : 'html',
    'data'     : parametros,
    'headers':{
      'X-CSRFToken' : _csrf_token,
    }
    }).done(function(ev) {
      var datos = $("#data_modal").html(ev);
      $("#myModal").modal('show');
  });

}

/**
Metodo que permite imprimir formatos
**/
function imprimir(aplicacion,metodo,params) {

  if (params === undefined || params === null) {
    params = {};
  }

  var f = document.createElement("form");
  f.setAttribute('id','form_print');
  f.setAttribute('method','POST');
  f.setAttribute('action',_homeurl+'print/'+aplicacion+'/'+metodo);
  f.setAttribute('target','_blank');

  var i;
  
  i = document.createElement("input");
  i.setAttribute("type","text");
  i.setAttribute("name","csrfmiddlewaretoken");
  i.setAttribute("value",_csrf_token);
  f.appendChild(i);

  $.each(params,function(x,val) {
    i = document.createElement("input");
    i.setAttribute("type","text");
    i.setAttribute("name",x);
    i.setAttribute("value",val);

    f.appendChild(i);

  });

  $("body").append(f);
  $("#form_print").submit();
  $("#form_print").remove();

}

$(document).ready(function() {

  $.datetimepicker.setLocale('es');

  $.ajaxSetup({
    'url'      : _homeurl+'ajax/',
    'type'     : 'POST',
    'dataType' : 'json',
    'cache'    : false,
    'async'    : true,
    'headers'  : {
      'X-CSRFToken' : _csrf_token,
    }
  });

  $(".date").datetimepicker({
    lang       : 'es',
    format     : 'd/m/Y',
    formatDate : 'd/m/Y',
    timepicker : false
  });

  $(".datetime").datetimepicker({
    lang       : 'es',
    format     : 'd/m/Y h:i:s',
    formatDate : 'd/m/Y h:i:s',
    timepicker : true
  });


  $('.addForeignKey').click(function(ev){
    ev.stopImmediatePropagation();
    var modelo    = $(this).data('modelo');
    var app       = $(this).data('app');
    modalGenerico(modelo,app);
  });

  $('input[type="number"]').attr('type','text')

  $("body").on("keypress",'input',function(e) {
    var cadena = String.fromCharCode(e.which)
    var exp    = RegExp( /^[a-zA-ZáéíóúAÉÍÓÚÑñ0-9\._\-¡\*_\+()\/\%@\#\!\s]/ )
    if( e.charCode == 0  || exp.test(cadena) ){
      if (e.keyCode == 10 || e.keyCode == 13 && !$(this).data('enter'))  {
        e.preventDefault();
      }
      return true;
    }
    return false;
  });

  $("body").on("click",'input',function() {
    $(this).select();
  });


  $("body").on("keypress",".entero",function (e) {
    var valLength = $(this).val().length;
    var maxCount  = $(this).attr('maxlength');
    var cadena    = String.fromCharCode(e.which)
    var exp       = RegExp(/^(\d*)$/);
    if (e.charCode == 0 || exp.test(cadena) ) {
      if(valLength > maxCount){
        $(this).val($(this).val().substring(0,maxCount));
      }
      return true;
    }
    return false;
  });

  $("body").on("keypress",".decimal",function (e) {
    var cadena       = String.fromCharCode(e.which)
    var value        = $(this).val()
    var exp          = /^(\d{0,8})(\.\d{0,2})?$/;
    var pos          = $(this)[0].selectionStart;
    var cadena_final = value.substring(0,pos)+cadena+value.substring(pos);
    
    if( e.charCode == 0 || exp.test(cadena_final)){
      return true;
    }
    return false;
  });

/*
* se utiliza  el delete-row colocando un span en la ultima columna <td> de la fila,
* el orden de los elmentos necesarios es:
* (nombre del ajax) app modelo id_elemento div_o_contenedor_de_formset prefijo_formset
* <span>elimina_relacion venta cotizacion_detalle {{item.instance.id}} #af cotizacion_detalle_set</span>
*/ 
  $("body").on("click",".delete-row",function() {
    var tabla     = $(this).closest('tbody')
    var row       = $(this).closest('tr').last().find('span')
    var elementos = row.text().split(' ')
    var campo     = tabla.find('tr')
    var contador  = 0
    var initial   ='#id_'+elementos[5]+'-INITIAL_FORMS'
    
    if (!confirm("¿Realmente desea eliminar este elemento?")) {
      return false;
    }

    if( campo.length <= 1){
      campo.children().find('input,select,textarea').each(function() {
        $(this).val('');
      });
      campo.find('.clean_field').each(function() {
        $(this).text('');
      });
      return false
    }
    if( row.text() == '' ){
      deleteForm($(this), elementos[4] , elementos[5]);
    }else{
      boton_elimina_elemento($(this),row.text().split(' '))
      $(initial).val($(initial).val()-1)
      deleteForm($(this), elementos[4] , elementos[5]);
    }
  });

  $("body").on("change",".option_search",function(ev) {
    var e = $.Event('keyup');
    e.keyCode = 8;
    $("#search").trigger(e);
  })
  $("body").on("keyup",".busqueda",function(ev) {
    var tabla   = $(this).data('zone');
    var entrada = $(this).val().trim().split(' ')
    var options = $(this).data('option')
    var back    = 0

    if(ev.keyCode == 8){
      back = 1
    }
    if( options != undefined ){
      options = options.split(' ')
      for(item in options){
        var campo = options[item]+' option:selected'
        if($(campo).val() != '' && $(campo).text() != ''){
          entrada.unshift($(campo).text())
        }
      }
    }

    for(item in entrada){
      if(item == 0){
             back = 1
      }else{
        back = 0
      }
      if(entrada[item] != '' || entrada[0].length == 0){
         search(entrada[item].toUpperCase(),tabla,back);
      }
    }

  });
  

});

function search(dato,tabla,back){
  var tabla = tabla.split(' ')
  var tabla_search =tabla[0]+' '+tabla[1]+(!back ? ':visible':'')

  $(tabla_search).each(function () {
    if ($(this).find("input").length ) {
      $(this).toggle($(this).find("input").val().toUpperCase().indexOf(dato) !== -1 || $(this).text().toUpperCase().indexOf(dato) !== -1);
    }else{
      $(this).toggle($(this).text().toUpperCase().indexOf(dato) !== -1);
    }
  });
}


function formato_dinero(cantidad,decimales) {
 "use strict";
 if (decimales === undefined || decimales === null) {
   decimales = 2;
 }
 var tmp = parseFloat(cantidad).toFixed(decimales).replace(/(\d)(?=(\d{3})+\.)/g, '$1, ');
 return tmp;
}

/**
 * Codigo necesario para actualizar el DOM cuando se escribe
 * $(elemento).val('valor')
*/
var originalVal = this.originalVal = $.fn.val;
$.fn.val = function(value) {
  if (value === undefined) {
    return originalVal.call(this);
  }
  else {
    this.attr("value",value);
    return originalVal.call(this,value);
  }
};
