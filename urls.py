from django.conf.urls.defaults import *
from comments.views import submit_comment

urlpatterns = patterns('',
	url(r'^submit/$', submit_comment, name="submit-comment"),
)