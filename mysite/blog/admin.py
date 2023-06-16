from django.contrib import admin

from .models import Post, Comment


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'title', 'text')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'text')
    list_filter = ('post',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

