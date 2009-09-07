from datetime import datetime
from django.conf import settings
from django.db import models
from django.template.defaultfilters import striptags
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.auth.models import User
from comments.managers import CommentManager

class Comment(models.Model):

    NEW = "NEW"
    APPROVED = "APPROVED"
    NOT_APPROVED = "NOT_APPROVED"
    SPAM = "SPAM"

    COMMENT_STATUS_CHOICES = (
        (NEW, "New"),
        (APPROVED, "Approved"),
        (NOT_APPROVED, "Not approved"),
        (SPAM, "Spam"),
    )

    objects = CommentManager()

    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = GenericForeignKey()

    ip_address = models.IPAddressField(blank=True, null=True)
    date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, blank=True, null=True, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True, verify_exists=True)
    comments = models.TextField(u"Comments")
    status = models.CharField(max_length=100, choices=COMMENT_STATUS_CHOICES, default=APPROVED)

    def __unicode__(self):
        return "%s: %s..." % (self.name, self.comments[:50])

    def get_absolute_url(self):
        return u"%s#comment-%s" % (self.content_object.get_absolute_url(), self.id)
        
    def save(self, *args, **kwargs):
        self.comments = striptags(self.comments)
        super(Comment, self).save(*args, **kwargs)

    class Meta:
        ordering = ('date',)