""" Sample model for group aware projects """

import datetime

from django.db import models

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


class Post(models.Model):

    # Sample text fields below
    title = models.CharField(max_length=140)
    creator = models.ForeignKey(User, verbose_name=_('creator'), related_name="%(class)s_created")
    created = models.DateTimeField(_('created'), default=datetime.datetime.now)    
        
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
    

