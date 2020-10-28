from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
#from ckeditor.fields import RichTextField
from tinymce.models import HTMLField
# Create your models here.

class Post (models.Model):
	title = models.CharField(max_length=50)
	content = HTMLField(blank=True, null=True)
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	picture = models.ImageField(default='default_post.jpg', upload_to='blog_pics')
	Views = models.DecimalField(max_digits=6, decimal_places=0, default=0)
	ReadDuration=models.DecimalField(max_digits=2, decimal_places=0, default=0)
	UpVotes=models.ManyToManyField(User, related_name='blog_posts_upvote')
	DownVotes=models.ManyToManyField(User, related_name='blog_posts_downvote')
	comms_number = models.DecimalField(max_digits=6, decimal_places=0, default=0)


	def __str__ (self):
		return self.title

	@property
	def C_DownVotes(self):
		return self.DownVotes.count()

	@property
	def CountVote(self):
		return self.UpVotes.count()-self.DownVotes.count()

	@property
	def C_UpVotes(self):
		return self.UpVotes.count()

	def get_absolute_url(self):
		return reverse('post-detail',kwargs={'pk':self.pk})

class comment(models.Model):
	comment = models.CharField(max_length=200)
	comm_user = models.ForeignKey(User, on_delete=models.CASCADE)
	comm_post = models.ForeignKey(Post, on_delete=models.CASCADE)
	date_posted = models.DateTimeField(default=timezone.now)

	def __str__ (self):
		return self.comment
	