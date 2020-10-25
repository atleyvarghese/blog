# coding=utf-8
from django.contrib import admin

from apps.posts.models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 3


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'created_at', 'updated_at', )
    inlines = (CommentInline, )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('get_post_title', 'get_comment', 'author', 'created_at', 'updated_at', )

    def get_comment(self, obj):
        return obj.comment[:10]

    def get_post_title(self, obj):
        return obj.post.title

    get_comment.short_description = "comment"
    get_post_title.short_description = "Post"


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)