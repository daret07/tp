"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include,url
from django.contrib import admin
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'',include([
	    url(r'^adm/', admin.site.urls),
	    url(r'^$',views.index,name='index'),
	    url(r'^login', views.login,name='login'),
	    url(r'^logout', views.logout,name='logout'),
	    url(r'^web/(?P<app>\w+)/(?P<modelo>\w+)/delete/(?P<pk>\d+)$', views.eliminar,name='eliminar'),
	    url(r'^web/(?P<app>\w+)/(?P<modelo>\w+)/listar', views.listar,name='listar'),
	    url(r'^web/(?P<app>\w+)/(?P<modelo>\w+)/(?P<pk>\d+)', views.editar,name='editar'),
	    url(r'^web/(?P<app>\w+)/(?P<modelo>\w+)', views.editar,name='crear'),
	    
	    url(r'^print/(?P<app>\w+)/(?P<metodo>\w+)$',views.imprimir, name='imprimir'),
	    url(r'^modal/', views.modal,name='modal'),
	    url(r'^ajax/$', views.ajax,name='ajax'),
    ]))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
