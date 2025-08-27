from django.contrib import admin
from .models import Todo

# Register your models here.
class Designing(admin.ModelAdmin):
    list_display=('Title','due_date')
admin.site.register(Todo,Designing)
