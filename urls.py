""" Sample urls file for group aware projects """

from django.conf.urls.defaults import *

urlpatterns = patterns("",
    url(r'^create/$', 'wall.views.add', name="wall_add"),
    url(r"^$", "wall.views.list", name="wall_list"),
    url(r"^(?P<id>[-\w]+)/$", "wall.views.detail", name="wall_detail"),
)


# stick this into your groups/dances urls.py:

#urlpatterns += bridge.include_urls('sample_group_aware_app.urls',
#                r'^dance/(?P<group_slug>[-\w]+)/samples/')