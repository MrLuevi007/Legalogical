from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post, comment
from .utils import get_read_time
from django.views.generic import (ListView,  
	CreateView,
	UpdateView,
	DeleteView
)
from django.contrib.auth.mixins import (LoginRequiredMixin,
	UserPassesTestMixin
)
from django.contrib.auth.decorators import login_required
from .forms import CreateNewComment
from django.contrib import messages
from users.models import Profile
from django.urls import reverse_lazy

def resource(request):	
	return render(request, 'blog/resource.html')

def contact(request):	
	return render(request, 'blog/about.html')

def DetailView(request,pk):
	post = Post.objects.get(id=pk)
	Guy=request.user
	post.ReadDuration = get_read_time(post.content)
	post.Views +=1 
	post.save()
	votes = post.C_UpVotes-post.C_DownVotes
	if post.UpVotes.filter(username=request.user.username):
		Up=1
	else:
		Up=0
	if post.DownVotes.filter(username=request.user.username):
		Down=1
	else:
		Down=0
	comm_form = CreateNewComment()	
	if request.method == 'POST'	:
		comm_form = CreateNewComment(request.POST)
		if comm_form.is_valid():
			if request.user.is_authenticated:
				com = comm_form.save(commit=False)
				com.comm_post = post
				com.comm_user = Guy
				com.save()
				messages.success(request,f'Your comment has been posted')		
				return redirect('post-detail',pk=post.id)
	Au=0
	post.comms_number=comment.objects.filter(comm_post=post).count()
	post.save()
	if request.user.is_authenticated:
		if not request.user.is_anonymous:
			Au=1 if request.user.profile.creator else 0
	content = {
	'Post'	:	post,
	'Votes'	:	votes,
	'Up'	:	Up,
	'Down'	:	Down,
	'comm'	:	comm_form,
	'comms'	:	comment.objects.filter(comm_post= post).order_by('-date_posted'),
	'Au'	:	Au
	}
	return render(request, 'blog/post_detail.html',content)

@login_required
def UpVote(request,pk):
	post = get_object_or_404(Post,id= pk)
	post.UpVotes.add(request.user)
	post.DownVotes.remove(request.user)
	post.save()
	return redirect('post-detail',pk=post.id)

@login_required
def DownVote(request,pk):
	post = get_object_or_404(Post,id= pk)
	post.UpVotes.remove(request.user)
	post.DownVotes.add(request.user)
	post.save()
	return redirect('post-detail',pk=post.id)

@login_required
def NoVote(request,pk):
	post = get_object_or_404(Post,id= pk)
	post.UpVotes.remove(request.user)
	post.DownVotes.remove(request.user)
	post.save()
	return redirect('post-detail',pk=post.id)

class AllPostListView (ListView) :
	model = Post 
	ordering = ['-date_posted']
	paginate_by = 5

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query:
			object_list = self.model.objects.filter(content__icontains=query)
		else:
			object_list = self.model.objects.all()
		return object_list

class PostListView (ListView) :
	model = Post 
	template_name = 'blog/home.html'
	context_object_name = 'Post'
	ordering = ['-date_posted']
	
class PostCreateView (LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title','content','picture']

	def form_valid(self,form):
		form.instance.author = self.request.user
		if self.request.user.profile.creator:
			return super().form_valid(form)
		else:
			return redirect('blog-home')



class PostUpdateView (LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title','content','picture']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author :
			return True
		False


class PostDeleteView (LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = "/"

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author :
			return True
		False


#for comments


class CommentDeleteView (LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = comment

	def test_func(self):
		comment = self.get_object()
		if self.request.user == comment.comm_user :
			return True
		False
	
	def get_success_url(self):
		pk=self.kwargs['pk']
		return reverse_lazy('post-detail', kwargs={'pk': pk})