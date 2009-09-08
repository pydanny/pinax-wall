from django import forms
from django.utils.translation import ugettext as _

from wall.models import Post

class WallForm(forms.ModelForm):
    """Form for adding a new sample object
    
    """
    def __init__(self, user, group, *args, **kwargs):
        self.user = user
        self.group = group
        
        super(SampleForm, self).__init__(*args, **kwargs)
    
    def save(self, commit = True):
        return super(SampleForm, self).save(commit)
    
    class Meta:
        model = Post
        fields = ('title')
    
    def clean(self):
        self.check_group_membership()
        return self.cleaned_data
    
    def check_group_membership(self):
        group = self.group
        if group and not self.group.user_is_member(self.user):
            raise forms.ValidationError(_("You must be a member to create wall entries"))