from openclass.api import OpenClassAPI

class OpenClass(OpenClassAPI):
	"""
		OpenClass class handles API specific calls, invoking the OpenClassAPI for 
		authentication and actual requests

		Example: get course info.

		>>> oc = OpenClass()
		>>> r = oc.get_course(8303682)
		>>> r 
		{ 'courseTitle': 'Math 51', 'courseCode': 'MATH 51', ......... }
	"""

	# If we need to set any static-ish variables, do it here.

	"""
		OpenClass

		Purpose: makes requests to the OpenClass API

		Returns: __init__ functions can't return anything! hehehehe

		Required parameters:
			- admin_email: email of OpenClass admin
			- admin_pw:    password of OpenClass admin
			- api_key:     OpenClass API key

		Optional parameters:
			- auth_token:    authentication token (if you cached it)
			- refresh_token: refresh token (if you cached it)
	"""
	def __init__(
		self,
	 	admin_email,
	 	admin_pw,
		api_key,
		auth_token    = None,
		refresh_token = None,
		debug 		  = False
	):
		super(OpenClass, self).__init__(admin_email, admin_pw, api_key, auth_token, refresh_token, debug)

	# ====================================================
	# use these, heavily
	# ====================================================

	def get_person(self, institution_slug, openclass_user_id):
		return self.make_request('GET', self._get_person_url(institution_slug, openclass_user_id))

	def get_memberships(self, user):
		pass

	def get_course(self, openclass_course_id):
		return self.make_request('GET', self._get_course_url(openclass_course_id))

	'''
		create_course

		Required parameters:
			- data: dictionary

				Required elements in data dictionary:
					- institutionId: string
					- courseTitle:   string < 50 chars

		Optional parameters here: http://code.pearson.com/openclass/apis/course-sections/course-sections-resources/uri-course-sections_x
	'''
	def create_course(self, data):
		return self.make_request('POST', self._get_create_course_url(), data = data)

	def update_course(self, openclass_course_id, data):
		return self.make_request('PUT', self._get_update_course_url(openclass_course_id), data = data)

	def delete_course(self, openclass_course_id):
		return self.make_request('DELETE', self._get_course_url(openclass_course_id))

	def get_course_assignments(self, institution_slug, openclass_course_id):
		pass

	def get_courseroles(self):
		return self.make_request('GET', self._get_courseroles_url())

	# ====================================================
	# all the urls that the above functions use
	# ====================================================

	def _get_person_url(self, institution_slug, openclass_user_id):
		return '{}/campus/institutions/{}/enrollments/sis/{}'.format(self.BASE_API_URL, institution_slug, openclass_user_id)

	def _get_courseroles_url(self):
		return '{}/v1/campus/courseroles'.format(self.BASE_API_URL)

	def _get_course_url(self, openclass_course_id):
		return '{}/v1/campus/coursesections/{}'.format(self.BASE_API_URL, openclass_course_id)

	def _get_create_course_url(self):
		return '{}/v1/campus/coursesections'.format(self.BASE_API_URL)

	def _get_update_course_url(self, openclass_course_id):
		return '{}/v1/campus/coursesections/{}'.format(self.BASE_API_URL, openclass_course_id)

