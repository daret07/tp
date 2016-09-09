/*
 * Libreria que permite agregar y eliminar dinamicamente elementos de inlineformset
 * para Django.
 *
 * Para que la libreria funcione correctamente es necesario tener presente lo
 * siguiente en el codigo:
 *
 * Ejemplo TR.
 * <tr id="{{ elemento.prefix }}-row" class="dynamic-form">
 *
 * Ejemplo Eliminar Fila.
 * <a id="remove-{{ elemento.prefix }}-row" href="javascript:void(0)" class="delete-row">
 * Quitar
 * </a>
 *
 * $(document).ready(function() {
 * $('.add-row').click(function() {
 *   return addForm(this, '<formset>');
 * });
 *
 * $('.delete-row').click(function() {
 *    return deleteForm(this, '<formset>');
 *  })
 * });
 *
 */

function updateElementIndex(el, prefix, ndx) {
  var id_regex = new RegExp('(' + prefix + '-\\d+)');
  var replacement = prefix + '-' + ndx;
  
  if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
  if (el.id) el.id = el.id.replace(id_regex, replacement);
  if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function addForm(btn,parent,prefix) {
  var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
  var row = $(parent).find('.dynamic-form:first').clone(true).get(0);

  $(row).removeAttr('id').insertAfter($(parent).find('.dynamic-form:last')).children('.hidden').removeClass('hidden');
  $(row).children().not(':last').find('input,select,textarea').each(function() {
    updateElementIndex(this, prefix, formCount);
    $(this).val('');
  });
  
  $(row).find(".clean_field").text('');
  $(row).find("td:last").html("<a href='#' class='delete-row'>Quitar</a>");

  /**
  $(row).find('.delete-row').click(function() {
    deleteForm(this,parent, prefix);
  });
  */

  $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
    return false;
}

function deleteForm(btn,parent, prefix) {

  var total_rows = $(parent).find("tr").length;

  if (total_rows == 1) {
    alert("No es posible eliminar esta fila, ya que no se tienen mas por eliminar");
    return false;
  }

  $(btn).parents('.dynamic-form').remove();
  var forms = $(parent).find('.dynamic-form');

  $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);

  for (var i=0, formCount=forms.length; i<formCount; i++) {
    $(forms.get(i)).children().not(':last').children().each(function() {
      updateElementIndex(this, prefix, i);
    });
  }

  return false;
}
