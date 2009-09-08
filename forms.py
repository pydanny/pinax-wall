from django import forms
from django.utils.translation import ugettext as _

from uni_form.helpers import FormHelper, Submit, Reset

from wall.models import Post

class WallForm(forms.ModelForm):
    """Form for adding a new wall post
    """
    
    title = forms.CharField(widget=forms.Textarea())
    
    # Attach a formHelper to your forms class.
    helper = FormHelper()

    # Add in a class and id
    helper.form_id = 'wall-form'
    helper.form_class = 'main-form'

    # add in a submit and reset button
    submit = Submit('post','Post')
    helper.add_input(submit)
    
    def __init__(self, user, group, *args, **kwargs):
        self.user = user
        self.group = group
        
        super(WallForm, self).__init__(*args, **kwargs)
    
    def save(self, commit = True):
        return super(WallForm, self).save(commit)
    
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