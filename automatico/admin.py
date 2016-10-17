# -*- coding: utf-8 -*-
from django.contrib import admin
from base.utilidades import CustomModelAdmin
# Register your models here.
class cron_autoAdmin(CustomModelAdmin):
  list_display=('concepto','activo')
  list_display_links=('concepto',)
  list_filter=('concepto',)
  search_fields=('concepto',)