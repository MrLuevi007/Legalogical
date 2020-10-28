from django.forms import ModelForm 
from .models import comment, Post
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.generic import (
	CreateView,
	UpdateView
)
from django.contrib.auth.mixins import (LoginRequiredMixin,
	UserPassesTestMixin
)

class CreateNewComment(ModelForm) :
	comment = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Add new comment...'}))
	class Meta:
		model=comment
		fields =['comment']
	def form_valid(self,form):
		form.instance.comm_user = self.request.user
		form.instance.comm_post = self.request.post
		return super().form_valid(form)


