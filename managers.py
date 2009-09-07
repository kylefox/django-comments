from django.db import models
from django.contrib.sites.models import Site

class CommentManager(models.Manager):
	"""
	Manager that provides abilities to get approved / moderation / spam comments.
	By default, comments are ordered by date with the most recent first.
	If you want to display them with the oldest first (such as in a template),
	use the .reverse() method on the QuerySet.
	"""
		
	def approved_for_object(self, obj):
		"Returns all the approved comments on the given object"
		from django.contrib.contenttypes.models import ContentType
		content_type=ContentType.objects.get(app_label=obj._meta.app_label, name=obj._meta.module_name)
		return self.approved().filter(object_id=obj.pk, content_type=content_type)
	
	def approved_for_content_type(self, content_type):
		"Returns all the approved comments on the given ContentType"
		from django.contrib.contenttypes.models import ContentType
		return self.approved().filter(content_type=content_type)
		
	def approved(self):
		"Returns comments that have been approved (are public)."
		from comments.models import Comment
		return self.get_query_set().filter(status=Comment.APPROVED)

	def awaiting_moderation(self):
		"Returns comments that are awaiting moderation."
		from comments.models import Comment
		return self.get_query_set().filter(status=Comment.MODERATE)
		
	def spam(self):
		"Returns comments that have been marked as spam."
		from comments.models import Comment
		return self.get_query_set().filter(status=Comment.SPAM)