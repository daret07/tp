from django.contrib import admin

class ejemploAdmin(admin.ModelAdmin):
    list_display = ('campo','campos2',)
    list_filter = ('campo',)
