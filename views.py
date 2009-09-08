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
def add(request, group_slug = None, bridge = None,
                form_class=WallForm, 
                template_name='wall/add.html'):
    
    """Add a new repository to a group or to the whole list"""
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    if group:
        group_base = bridge.group_base_template()
    else:
        group_base = None
    
    if not request.user.is_authenticated():
        is_member = False
    else:
        if group:
            is_member = group.user_is_member(request.user)
        else:
            is_member = True
    
    if request.method == "POST":
        if request.user.is_authenticated():
            form = form_class(request.user, group, request.POST)
            if form.is_valid():
                post = form.save(commit = False)
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
        
    helper = FormHelper()
    submit = Submit('submit','submit')
    helper.add_input(submit)
    
    return render_to_response(template_name, {
        "group": group,
        "is_member": is_member,
        "form": form,
        "group_base": group_base,
        "helper": helper
    }, context_instance = RequestContext(request))


def list(request, group_slug=None, bridge=None):
    
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
    
    return render_to_response("wall/list.html", {
        "group": group,
        "posts": posts,
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
    
    