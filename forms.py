from django import forms
from comments.models import Comment

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name', 'email', 'website', 'body', 'object_id', 'content_type')
		
	remember_me = forms.BooleanField(required=False)
	# TODO: Add "Email followup comments" field.
		
	def __init__(self, *args, **kwargs):
			super(CommentForm, self).__init__(*args, **kwargs)
			self.fields['object_id'].widget = forms.HiddenInput()
			self.fields['content_type'].widget = forms.HiddenInput()
			
	def remember_user(self):
		return self.cleaned_data.get('remember_me')