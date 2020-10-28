import re
from django.utils.html import strip_tags
from .models import Post, comment

def get_read_time(html_string):
	word_string = strip_tags(html_string)
	matchwords = re.findall(r'\w+',word_string)
	count=len(matchwords)
	readtime = round(count/200)
	return readtime
	
