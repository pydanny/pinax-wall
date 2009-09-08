""" Sample model for group aware projects """

from django.db import models

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class Post(models.Model):

    # Sample text fields below
    text = models.TextField()
        
    # The following three fields are required for being group aware
    object_id = models.IntegerField(null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    group = generic.GenericForeignKey("object_id", "content_type")
    
    class Meta:
        verbose_name_plural = "Post"    
        
    def __unicode__(self):
        return self.title       

    # permalink/get_absolute_url
    @models.permalink
    def get_absolute_url(self, group = None):
        kwargs = {"id": self.id}
        if group:
            return group.content_bridge.reverse("post_detail", group, kwargs)
        return reverse("post_detail", kwargs = kwargs)
    

