from django.contrib import admin
from .models import Visitor, Item, Entry
# Register your models here.
admin.site.register(Visitor)
admin.site.register(Item)
admin.site.register(Entry)