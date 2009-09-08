from django.contrib import admin

from wall.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'created')

admin.site.register(Post, PostAdmin)


