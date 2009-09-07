from django.contrib.syndication.feeds import Feed
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model

from comments.models import Comment

class LatestCommentsFeed(Feed):
	"""
	An RSS feed of the latest comments, with three formats available:
		1) All approved comments.
		2) All approved comments for a particular ContentType (ie blog.Post).
		3) All approved comments for a specific object.
	"""
	# TODO: More fully implement the available hooks found at:
	# http://www.djangoproject.com/documentation/syndication_feeds/#feed-class-reference
	# categories, copyright, author_name, author_email, etc.
	
	def __init__(self, *args, **kwargs):
		self.site = Site.objects.get_current()
		super(LatestCommentsFeed, self).__init__(*args, **kwargs)

	def get_object(self, bits):
		# Incoming URLs will have a scheme like this:
		# /feeds/comments/<app>.<model>/  >>  /feeds/comments/blog.Post/
		# /feeds/comments/<app>.<model>/<object.id>  >>  /feeds/comments/blog.Post/42/
		if len(bits) == 0:
			# No extra parameters were provided: return approved comments on *all* objects.
			return None
		if len(bits)  >= 1:
			try:
				# Determine the ContentType
				app_name, model_name = bits[0].split('.')
				content_type = ContentType.objects.get(app_label=app_name, name=model_name)
			except ValueError:
				# Parameters were not in proper format -- raise a 404.
				raise Comment.DoesNotExist
			if len(bits) == 1:
				# User wants a feed for an entire ContentType.
				return content_type
			elif len(bits) == 2:
				try:
					# User wants a feed for a specfic instance of ContentType.
					return content_type.get_object_for_this_type(id=int(bits[1]))
				except ValueError:
					raise Comment.DoesNotExist
		raise Comment.DoesNotExist

	
	def title(self, obj):
		# TODO: Feed title should be configurable.
		if isinstance(obj, ContentType):
			title =  ' on all %s' % unicode(obj.model_class()._meta.verbose_name_plural)
		elif isinstance(obj, Model):
			title =  ' on "%s"' % obj
		elif isinstance(obj, type(None)):
			title = ""
		return "%s: Latest comments%s" % (self.site.name, title)

	def description(self):
		# TODO: Feed description should be configurable.
		# TODO: Comment feed description() should be dynamic
		# based on feed content, similar to title().		
		return "Latest comments %s" % self.site.name

	def link(self):
		return "http://%s/" % (self.site.domain)

	def item_pubdate(self, item):
		return item.date
		
	def items(self, obj):
		# TODO: Number of feed items should be configurable.		
		if isinstance(obj, ContentType):
			comments = Comment.objects.approved_for_content_type(obj)
		elif isinstance(obj, Model):
			comments = Comment.objects.approved_for_object(obj)
		elif isinstance(obj, type(None)):
			comments = Comment.objects.approved()
		return comments[:10]
