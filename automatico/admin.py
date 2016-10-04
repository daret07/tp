# -*- coding: utf-8 -*-
from django.contrib import admin
from base.utilidades import CustomModelAdmin
# Register your models here.
class cron_autoAdmin(CustomModelAdmin):
  list_display=('cron','definicion','activo')
  list_display_links=('cron',)
  list_filter=('cron',)
  search_fields=('cron',)