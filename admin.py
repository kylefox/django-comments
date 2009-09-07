from django.contrib import admin

from comments.models import *

class CommentAdmin(admin.ModelAdmin):
	radio_fields = {'status': admin.VERTICAL}
	search_fields = ('user', 'body')
	list_display = ('__unicode__', 'email', 'website', 'date', 'status')
	list_filter = ('date', 'status')
	date_hierarchy = 'date'

admin.site.register(Comment, CommentAdmin)