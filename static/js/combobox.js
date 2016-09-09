$.widget("ui.combobox", {
  _create: function() {
    "use strict";
    var self = this,
    select   = this.element.hide(),
    //tamano   = (select.children("option").length < 50) ? 0:2,
    tamano   = 0,
    selected = select.children(":selected"),
    value    = selected.val() ? selected.text() : "";
    
    var ide = $(select).prop("id");
    var grupo = $("<div>").prop("class","input-group").insertAfter(select);
    var input = this.input = $("<input id='input_"+ide+"'>").val(value).autocomplete({
      delay: 0,
      minLength:tamano,
      source: function(request, response) {
        var matcher = new RegExp($.ui.autocomplete.escapeRegex(request.term), "i");
        response(select.children("option").map(function() {
          var text = $(this).text();
          if (this.value && (!request.term || matcher.test(text))) {
            return {
              label: text.replace(
                new RegExp(
                  "(?![^&;]+;)(?!<[^<>]*)(" +
                  $.ui.autocomplete.escapeRegex(request.term) +
                  ")(?![^<>]*>)(?![^&;]+;)", "gi"
              ),
              "<strong>$1</strong>"),
              value: text,
              option: this
            };
          }
        }));
      },
      select: function(event, ui) {
        ui.item.option.selected = true;
        self._trigger("selected", event, {
          item: ui.item.option
        });
        select.trigger("change");
      },
      change: function(event, ui) {
        if (!ui.item) {
          var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex($(this).val()) + "$", "i"),
          valid = false;
          select.children("option").each(function() {
            if ($(this).text().match(matcher)) {
              this.selected = valid = true;
              return false;
            }
          });
          if (!valid) {
            select.val("");
            select.trigger("no_data");
            return false;
          }
        }
      }
    }).addClass('form-control');
    
    $(input).data("ui-autocomplete")._renderItem = function(ul, item) {
      return $("<li></li>").data("item.autocomplete", item).append("<a>" + item.label + "</a>").appendTo(ul);
    };

    $(grupo).append(input);
    $(input).keyup(function(ev) {
      if (ev.keyCode === 13) {
        select.trigger("enter");
      }
    });
    
    this.button = $("<span class='input-group-addon'><i class='fa fa-chevron-down' style='cursor:pointer;'></i>").attr("tabIndex", -1).attr("title", "Mostrar Todo").insertAfter(input).removeClass("ui-corner-all").addClass("ui-corner-right ui-button-icon").click(function() {
      // close if already visible
      if (input.autocomplete("widget").is(":visible")) {
        input.autocomplete("close");
        return;
      }

      //alert("OK");
      // work around a bug (likely same cause as #5265)
      $(this).blur();

      // pass empty string as value to search for, displaying all results
      input.autocomplete("search", "");
      input.focus();

    });
    
    $(select).change(function() {
      var option = $(this).find("option:selected");
      $(input).val($(option).text());
    });
  },

  destroy: function() {
    this.input.remove();
    this.button.remove();
    this.element.show();
    $.Widget.prototype.destroy.call(this);
  },
  autocomplete : function(value) {
    this.element.val(value);
    this.input.val(value);
  },
  open: function(){
    setTimeout(function () {
      $('.ui-autocomplete').css('z-index', 99999999999999);
    }, 0);
  }
});
