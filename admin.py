from django.contrib import admin

from wall.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'creator', 'created')

admin.site.register(Dance, DanceAdmin)


