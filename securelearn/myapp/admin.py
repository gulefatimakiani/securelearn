from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(tutorial)
admin.site.register(AppAdmin)
admin.site.register(registeredusers)
admin.site.register(comment)
admin.site.register(joke)
admin.site.register(ratetutorial)

