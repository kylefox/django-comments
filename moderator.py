from django.conf import settings
from django.contrib.sites.models import Site

from comments.models import Comment
from comments.akismet import Akismet, APIKeyError

class CommentModerator(object):
	
	def __init__(self):
		self.site = Site.objects.get_current()
	
	def get_comment_status(self, request, comment):
		"Returns either Comment.APPROVED, Comment.MODERATE or Comment.SPAM"
		if request.user.is_authenticated():
			return Comment.APPROVED
		elif self.is_spam(request, comment):
			return Comment.SPAM
		elif self.is_moderated(request, comment):
			return Comment.MODERATE
		else:
			# TODO: Allow default status to be configurable?
			return Comment.APPROVED	
		
	def is_spam(self, request, comment):
		"Indicates whether the given Request and Comment is spam."
		return self.is_akismet_spam(request, comment)
		
	def is_moderated(self, request, comment):
		"Indicates whether the given Request and Comment requires moderation."
		# This is a stub method for now.
		# TODO: Allow user to specify blacklist words..
		# TODO: If 'auto-approve' is False, this should *always* return True.
		return False
		
	def is_akismet_spam(self, request, comment):
		if not hasattr(settings, 'SECRET_AKISMET_KEY'):
			# SECRET_AKISMET_KEY is not set.
			return False
		akismet = Akismet(key=settings.SECRET_AKISMET_KEY,
						blog_url="http://%s" % self.site.domain)
		# Verify API key.
		if akismet.verify_key():
			# Build data according to:
			# http://www.voidspace.org.uk/python/akismet_python.html#comment-check
			akismet_data = {
				'comment_type': 'comment',
				'referrer': request.META.get('HTTP_REFERER', ''),
				'user_ip': comment.ip_address,
				'user_agent':  '',
				'comment_author': comment.name,
				'comment_author_email': comment.email,
				'comment_content': comment.body,
			}
			# If the object receiving the comment has a permalink,
			# provide that to Akismet as well.
			if hasattr(comment.get_content_object(), 'get_absolute_url'):
				akismet_data.update({
					'permalink': comment.get_content_object().get_absolute_url()
				})
			# Send the user's URL to Akismet, if provided.
			if comment.website:
				akismet_data.update({'comment_author_url': comment.website})
			# Check if it's spam.
			return akismet.comment_check(comment.body, data=akismet_data, build_data=True)
		else:
			# SECRET_AKISMET_KEY was provided, but invalid.
			raise APIKeyError(u"Akismet API key is invalid.")
		
moderator = CommentModerator()