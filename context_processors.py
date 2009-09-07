# TODO: Refactor this file.
from comments.views import USER_INFO_SESSION_KEY, REMEMBER_USER_SESSION_KEY

def user_info(request):
	"""
	Determines user info for pre-populating the comment form,
	in this order of precedence:
		1) Session cookies with the user info
		2) User object info, if request.user.is_authenticated()
		
	By searching the Session first, we give the User the ability
	to over-ride the information that's stored in their User account.
	"""
	
	name = email = website = None
	remember = request.session.get(REMEMBER_USER_SESSION_KEY, None)
	
	# Remember will be either True, False or None.
	# Assume they they want to be remembered if
	# True or None (not set), ie not False.
	if remember != False:			
		if request.user.is_authenticated():
			name = request.user.first_name
			email = request.user.email
		if USER_INFO_SESSION_KEY in request.session:
			data = request.session[USER_INFO_SESSION_KEY]
			name = data.get('name', name)
			email = data.get('email', email)
			website = data.get('website', website)
	
	return {'user_info': {
		'name': name,
		'email': email,
		'website': website,
		'remember': remember
	}}