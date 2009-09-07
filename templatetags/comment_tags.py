from django import template
from django.contrib.contenttypes.models import ContentType

from comments.forms import CommentForm
from comments.models import Comment

register = template.Library()

@register.inclusion_tag('comments/comment_form.html', takes_context=True)
def comment_form(context, obj):

    initial={
        'object_id':obj.id,
        'content_type':ContentType.objects.get(app_label=obj._meta.app_label,name=obj._meta.module_name).id
    }
    # 
    # if context['user_info']['remember'] != False:
    #     initial.update({
    #         'name': context['user_info']['name'],
    #         'email': context['user_info']['email'],
    #         'website': context['user_info']['website'],
    #         'remember_me': True,
    #     })
    if context['user'].is_authenticated():
        initial.update({
            'name': context['user'].get_full_name(),
            'email': context['user'].email,
        })
        
    comment_form = CommentForm(initial=initial)

    return {'comment_form':comment_form}

@register.tag
def get_approved_comments(parser, token):
    """
    {% get_approved_comments for <object> as <varname> %}
    """
    bits = token.split_contents()
    if len(bits) != 5 or bits[1] != 'for' or bits[3] != 'as':
        raise template.TemplateSyntaxError("Incorrect syntax for 'get_approved_comments'.  Correct format is '{% get_approved_comments for <object> as <varname> %}'")
    return ApprovedCommentsNode(bits[2], bits[4])

class ApprovedCommentsNode(template.Node):

    def __init__(self, obj, varname):
        self.obj = template.Variable(obj)
        self.varname = varname

    def render(self, context):
        context[self.varname] = Comment.objects.approved_for_object(self.obj.resolve(context))
        return u''
