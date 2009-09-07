from datetime import datetime
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from comments.managers import CommentManager

class Comment(models.Model):
	
	APPROVED = "APPROVED"
	MODERATE = "MODERATE"
	SPAM = "SPAM"
	
	COMMENT_STATUS_CHOICES = (
		(APPROVED, "Approved"),
		(MODERATE, "Moderated"),	
		(SPAM, "Spam"),
	)
	
	objects = CommentManager()
	content_type = models.ForeignKey(ContentType)
	object_id = models.IntegerField()
	site = models.ForeignKey(Site)
	ip_address = models.IPAddressField(blank=True, null=True)
	date = models.DateTimeField(default=datetime.now)
	user = models.ForeignKey(User, blank=True, null=True, editable=False)
	name = models.CharField(max_length=100)
	email = models.EmailField()
	website = models.URLField(blank=True, verify_exists=True)
	body = models.TextField(u"Comments")
	status = models.CharField(max_length=100, choices=COMMENT_STATUS_CHOICES, default=APPROVED)
		
	def __unicode__(self):
		return '%s on "%s"' % (self.name, self.get_content_object())

	def get_absolute_url(self):
		# A bit of a hack: Since we can't guarantee
		# the content_object has a get_absolute_url() method, 
		# return an empty string if get_absolute_url() doesn't exist.
		try:
			return u"%s#comment-%s" % (self.get_content_object().get_absolute_url(), self.id)
		except AttributeError:
			return u''
		
		
	def get_content_object(self):
		"""
		Returns the object that this comment is a comment on. Returns None if
		the object no longer exists.
		"""
		from django.core.exceptions import ObjectDoesNotExist
		try:
			return self.content_type.get_object_for_this_type(pk=self.object_id)
		except ObjectDoesNotExist:
			return None

	def object_title(self):
		return unicode(self.get_content_object())
	object_title.short_description = u'title'
	
	def response_to(self):
		return u'[%s] %s' % (self.content_type.name.capitalize(), self.object_title())
		
	class Meta:
		ordering = ('-date',)
