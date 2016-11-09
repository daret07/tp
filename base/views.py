# -*- coding:UTF-8 -*-
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.forms import modelform_factory
from importlib import import_module
from django.conf import settings
from base.utilidades import obtener_listado_admin
from django.contrib.auth import (
    authenticate,
    login as login_django,
    logout as logout_django,
)
import json,traceback
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect

@login_required
def index(request):
    parametros = {}

    for app in settings.INSTALLED_APPS:
        if app not in [
                        'django.contrib.admin',
                        'django.contrib.auth',
                        'django.contrib.contenttypes',
                        'django.contrib.sessions',
                        'django.contrib.messages',
                        'django.contrib.staticfiles',
                        'base',
                        'navegacion'
                        ]:
            try:
                _view_gen = import_module("%s.views" % app)
                if hasattr(_view_gen,'main_index'):
                    parametros.update(getattr(_view_gen,'main_index')(request))
            except:
                pass
    
    return TemplateResponse(request,'core/dashboard.html',parametros)

def login(request):
    from base.forms import LoginForm

    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data['usuario']
        password = form.cleaned_data['contrasena']
        
        try:
            user = authenticate(username=username, password=password)
        except:
            form.add_error('usuario','Usuario y/o contraseña incorrectos, verifiquelo e intente nuevamente.')
            user = None

        if user is not None:
            if user.is_active:
                login_django(request, user)
                return redirect('index')
            else:
                form.add_error('usuario','El usuario se encuentra inactivo, contacte con su administrador.')
        else:
            if not form._errors.has_key('usuario'):
                form.add_error('usuario','Usuario y/o contraseña incorrectos, verifiquelo e intente nuevamente.')
                
    return TemplateResponse(request,'core/login.html',{'form':form})

def logout(request):
    logout_django(request)
    return redirect('index')

@login_required
def listar(request,app,modelo):
    request.session['app']    = app
    request.session['modelo'] = modelo
    
    parametros = {}

    try:
        _mod      = import_module("%s.models" % app)
        _modAdmin = import_module("%s.admin" % app)

        _app = import_module("%s.views" % app)

        # Revisar si existe una especificación de vista para el modelo.
        if hasattr(_app,'listado_%s' % modelo):
            tmp_extra = getattr(_app,'listado_%s' % modelo)(request)
            if type(tmp_extra) is dict:
                parametros.update(tmp_extra)
            else:
                return tmp_extra

        if hasattr(_mod,modelo) and hasattr(_modAdmin,"%sAdmin" % modelo):

            _model            = getattr(_mod,modelo)
            _modelAdmin       = getattr(_modAdmin,'%sAdmin' % modelo)

            res_obtener_list = obtener_listado_admin(request,_model,_modelAdmin)
            if type(res_obtener_list) is HttpResponse:
                return res_obtener_list
            else:
                parametros.update(res_obtener_list)
            parametros['obj'] = _model

        else:

            return TemplateResponse(request,[
                '%s_listar.html' % modelo,
                'core/404.html',
                ],parametros)

    except Exception as e:
        if settings.DEBUG:
            traceback.print_exc()

        return TemplateResponse(request,[
            '%s_listar.html' % modelo,
            'core/404.html'
            ],parametros)

    return TemplateResponse(request,[
            '%s_listar.html' % modelo,
            'core/listar.html'
            ],parametros)

def obtener_form(app,modelo,request,parametros,pk=None):

    _app  = import_module("%s.views" % app)
    _mod  = None
    _form = None
    obj   = None

    # Revisar si existe una especificación de vista para el modelo.
    if hasattr(_app,'vista_%s' % modelo):
        tmp_extra = getattr(_app,'vista_%s' % modelo)(request,pk)
        if type(tmp_extra) is dict:
            parametros.update(tmp_extra)
        else:
            return tmp_extra
    
    # Carga el modelo
    try:
        _mod = import_module("%s.models" % app)
        _mod = getattr(_mod,modelo)
        obj  = _mod()

        # Instanciar objeto si existe.
        if pk:
            try:
                obj = _mod.objects.get(pk=pk)
            except:
                obj = _mod.objects.none()
        try:
            _form = import_module("%s.forms" % app)
            _form = getattr(_form,"%sForm" % modelo)
        except Exception as e:
            if settings.DEBUG:
                traceback.print_exc()
           
            _form = modelform_factory(_mod,fields='__all__')
    except:
        if settings.DEBUG:
            traceback.print_exc()

    return (_form,obj,parametros)

@login_required
def editar(request,app,modelo,pk=None):
    operacion = request.POST.get('form_action',None)

    request.session['app']    = app
    request.session['modelo'] = modelo

    parametros   = {}
    try:
        _obtener_form = obtener_form(app,modelo,request,parametros,pk)
        (_form,obj,parametros) = _obtener_form
        if not parametros.has_key('custom'):
            form  = _form(request.POST or None,request.FILES or None,instance=obj)
            if form.is_valid():
                obj = form.save()
                messages.info(request,'Se ha guardado con éxito la información.')
                
                if operacion == 'SAVE_AND_OTHER':
                    return redirect('crear',app=app,modelo=modelo)
                elif operacion == 'SAVE':
                    return redirect('listar',app=app,modelo=modelo)


            parametros['form']   = form
            parametros['obj']    = obj
        else:
            if settings.DEBUG:
                print "------"
                print "La operacion se realiza desde la vista."
                print "APP: %s" % app
                print "Modelo: %s" % modelo
                print "Vista: vista_%s()" % modelo
                print "------"
    except Exception as e:
        if settings.DEBUG:
            traceback.print_exc()

        tmp_retorno = _obtener_form
        if type(tmp_retorno) in [HttpResponse,HttpResponseRedirect]:
            return tmp_retorno

        return TemplateResponse(request,[
            '%s_crear.html' % modelo,
            'core/404.html'
            ],parametros)
    return TemplateResponse(request,[
        '%s_crear.html' % modelo,
        'core/crear.html'
        ],parametros)

@login_required
def eliminar(request,app,modelo,pk):
    
    parametros = {}

    try:
        _mod = import_module("%s.models" % app)
        _mod = getattr(_mod,modelo)
        obj  = _mod()
        obj = _mod.objects.get(pk=pk)

        parametros['obj']             = obj

    except Exception as e:
        return TemplateResponse(request,'core/404.html')
    
    if request.POST:
        obj.delete()
        return redirect('listar',app=app,modelo=modelo)

    return TemplateResponse(request,'core/confirmar_eliminar.html',parametros)

def modal(request):
    app   = request.POST.get('app',None)
    popup = request.POST.get('popup',None)

    parametros = {
        'app'   : app,
        'modal' : popup,
    }
    # Carga el modal
    try:
        _mod = import_module("%s.modal" % app)
    except:
        _mod = None

    if hasattr(_mod,'%s' % popup):
        tmp_extra = getattr(_mod,'%s' % popup)(request)
        parametros.update(tmp_extra);

    return TemplateResponse(request,['modales/%s.html' % popup ,'core/modal_404.html'],parametros)

@login_required
def ajax(request):

    app    = request.POST.get('app',None)
    metodo = request.POST.get('method',None)
    result = {
            'response' : None,
            'success'  : True
            }

    try:
        _mod = import_module("%s.ajax" % app)
        if hasattr(_mod,metodo):
            _res = getattr(_mod,metodo)(request)
            result['response'] = _res
        else:
            result['response'] = 'Metodo no Válido'
            result['success']  = False
    except Exception as e:
        print e
        result['success']  = False
        result['response'] = str(e)

    return JsonResponse(result,safe=False)

@login_required
def imprimir(request,app,metodo):

    parametros = {}

    try:
        vista_ = import_module("%s.views" % app)
        _mod = hasattr(vista_,'Print_%s' % metodo)
        if _mod:
            _func = getattr(vista_,'Print_%s' % metodo,None)
            _res = _func(request)
            parametros.update(_res)
    except Exception,e:
        pass

    return TemplateResponse(request,'formatos/%s.html' % (metodo),parametros)
