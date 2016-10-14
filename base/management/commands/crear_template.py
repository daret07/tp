# -*- coding:UTF-8 -*-
from django.core.management.base import BaseCommand, CommandError
from importlib import import_module
import os,shutil

class Command(BaseCommand):
  help = 'Comando que permite crear automaticamente el template <modelo>_crear.html en base a un modelo'

  def add_arguments(self, parser):
    parser.add_argument('app', type=str)
    parser.add_argument('modelo', type=str)

  def handle(self, *args, **options):
    app = options['app']
    mod = options['modelo']
    
    self.stdout.write('-------------')
    self.stdout.write('Analizando APP %s' % app)
    self.stdout.write('-------------')

    try:
      _app = import_module('%s.models' % app)
      if hasattr(_app,mod):
        _html = """
        {% extends 'core/crear.html' %}
        {% block extra_head %}
          {{ block.super }}
        {% endblock %}
        {% block contenido %}
        """
        _mod = getattr(_app,mod)()
        _fields = _mod._meta.fields
        
        for field in _fields:
          _html += """
            <div class='row'>
              <div class='col-lg-2 xxi form.{0}.errors xxe error xxf'>xxa form.{0}.label xxc</div>
             <div class='col-lg-4'>xxa form.{0} xxc</div>
            </div>

          """.format(field.name)
        _html += "{% endblock %}"

        # Revisar si existe un template existente
        archivo_template = '%s/templates/%s_crear.html' % (app,mod)
        if os.path.isfile(archivo_template):
          # ya existe template preguntar si desea sobreescribir.
          respuesta = raw_input("Ya existe un el siguiente template: %s, ¿desea sobreescribirlo? [n/Y] " % (archivo_template))
          if respuesta == "Y":
            self.stdout.write('Escribiendo: %s' % (archivo_template))
            shutil.move('%s' % (archivo_template),'%s.back' % (archivo_template))
            archivo = open('%s' % (archivo_template), 'w')
            archivo.write(_html)
            archivo.close()
        else:
            archivo = open('%s' % (archivo_template), 'w')
            archivo.write(_html)
            archivo.close()

      else:
        self.stdout.write('-------------')
        self.stdout.write('ERROR: No se encontro modelo: %s' % mod)
        self.stdout.write('-------------')
    except Exception as e:
      self.stdout.write('-------------')
      self.stdout.write('ERROR: No fue posible analizar APP: %s' % app)
      self.stdout.write('-------------')
