""" Sample view for group aware projects """

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from uni_form.helpers import FormHelper, Submit, Reset

from wall.models import Post
from wall.forms import WallForm



@login_required
def list(request, group_slug=None, bridge=None, form_class=WallForm):
    
    # If there is a bridge then get the group
    if bridge is not None:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    # If we have a group we fetch the wall from the group
    if group:
        posts = group.content_objects(Post)
    else:
        posts = Post.objects.all()
    
    # check on user authentication or if user is member of a group
    if not request.user.is_authenticated():
        is_member = False
    else:
        is_member = group.user_is_member(request.user)
        
    if is_member:
        if request.method == "POST":
            if request.user.is_authenticated():
                form = form_class(request.user, group, request.POST)
                if form.is_valid():
                    post = form.save(commit = False)
                    post.creator = request.user                                            
                    if group:
                        group.associate(post)
                    post.save()
                    if group:
                        redirect_to = bridge.reverse("wall_list", group)
                    else:
                        redirect_to = reverse("wall_list")
                    return HttpResponseRedirect(redirect_to)
        else:
            form = form_class(request.user, group)     
    else:
        form = None   
    
    return render_to_response("wall/list.html", {
        "group": group,
        "posts": posts,
        "form": form,
        "is_member": is_member
    }, context_instance=RequestContext(request))

def detail(request, slug, group_slug=None, bridge=None):
    
    # If there is a bridge then get the group
    if bridge is not None:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    # If we have a group we fetch the post from the group
    #if group:
    #    posts = group.content_objects(Post)
    #else:
    post = get_object_or_404(Post, slug=slug)
    
    # check on user authentication or if user is member of a group
    if not request.user.is_authenticated():
        is_member = False
    else:
        is_member = group.user_is_member(request.user)
    
    return render_to_response("wall/detail.html", {
        "group": group,
        "post": post,
        "is_member": is_member
    }, context_instance=RequestContext(request))
    
    