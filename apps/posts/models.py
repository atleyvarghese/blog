# coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractTracker(models.Model):
    """
    Tracker model to log the timestamp
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(AbstractTracker):
    """
    Model to store Blog details
    """
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'))
    publish_date = models.DateTimeField(_('Publish Date'))
    author = models.CharField(_('Author'), max_length=255)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['-created_at']

    def __str__(self):
        return '{} by {}'.format(self.title, self.author)


class Comment(AbstractTracker):
    """
    Model to store Comment Made By Users To Blog
    """
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField(_('Comment'))
    author = models.CharField(_('Author'), max_length=255)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-created_at']

    def __str__(self):
        return 'Comment on {} by {}'.format(self.post.title, self.author)
