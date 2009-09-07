from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.sites.models import Site
from django.conf import settings
from django.template.defaultfilters import striptags, wordwrap
from django.core.mail import EmailMessage
from django.template import RequestContext, Context, loader

from comments.models import *
from comments.forms import *
from comments.moderator import moderator

# Session key to hold user name, email, etc.
USER_INFO_SESSION_KEY = 'USER_COMMENT_INFO'
REMEMBER_USER_SESSION_KEY = 'REMEMBER_USER_COMMENT_INFO'

def submit_comment(request):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            
            # Instantiate the core Comment without saving.
            comment = comment_form.save(commit=False)
            
            # Determine IP Address.
            try:
                comment.ip_address = request.META.get('REMOTE_ADDR',
                    request.META.get('HTTP_X_FORWARDED_FOR', None))
            except: 
                comment.ip_address = None
                
            # Did an authenticated user submit this comment?
            if request.user.is_authenticated():
                comment.user = request.user
                
            # comment.status = moderator.get_comment_status(request, comment)
            comment.status = Comment.APPROVED
            comment.save()
            
            
            # # If the commenter wants to be remembered,
            # # store their details in the session.
            # if comment_form.remember_user():
            #     request.session[USER_INFO_SESSION_KEY] = {
            #         'name': comment.name,
            #         'email': comment.email,
            #         'website': comment.website
            #     }
            #     request.session[REMEMBER_USER_SESSION_KEY] = True
            # else:
            #     # Clear any existing session data.
            #     request.session[USER_INFO_SESSION_KEY] = {
            #         'name': None,
            #         'email': None,
            #         'website': None
            #     }
            #     request.session[REMEMBER_USER_SESSION_KEY] = False
            return HttpResponseRedirect(comment.get_absolute_url())
        else:
            return render_to_response('comments/errors.html', {
                'comment_form': comment_form,
                'allow_comments':True,
            }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))