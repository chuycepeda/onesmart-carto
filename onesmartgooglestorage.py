"""

	HANDLING GOOGLE CLOUD STORAGE


"""
class CloudStorageMediaHandler(webapp2.RequestHandler):	
	"""
		Route should be like:
			app = webapp2.WSGIApplication([
			 (r'/media/(?P<file_name>[\w.]{0,256})', CloudStorageMediaHandler),
			], debug=True)

		URL to serve will be like:
			"/media/{{ file }}"
	"""
	from google.appengine.api import app_identity
	import cloudstorage
	import mimetypes
	from google.appengine.api import images
	from google.appengine.ext import blobstore

	def _get_urls_for(self, file_name):
		user = users.get_current_user()
		if user is None:
			return
		bucket_name = app_identity.get_default_gcs_bucket_name()
		path = os.path.join('/', bucket_name, user.user_id(), file_name)
		real_path = '/gs' + path
		key = blobstore.create_gs_key(real_path)
		try:
			# size=0 parameter will make the CDN serve the original image.
			url = images.get_serving_url(key, size=0)
			thumbnail_url = images.get_serving_url(key, size=150, crop=True)
		except images.TransformationError, images.NotImageError:
			url = "http://storage.googleapis.com{}".format(path)
			thumbnail_url = None
		return file_name, url, thumbnail_url


	#uploading
	def post(self):
		user = users.get_current_user()
		bucket_name = app_identity.get_default_gcs_bucket_name()
		uploaded_file = self.request.POST.get('uploaded_file')
		file_name = getattr(uploaded_file, 'filename', None)
		file_content = getattr(uploaded_file, 'file', None)
		real_path = ''
		if file_name and file_content:
			content_t = mimetypes.guess_type(file_name)[0]
			real_path = os.path.join('/', bucket_name, user.user_id(), file_name)
			# if we want file to be publicly accesed, add after content_type 'options={'x-goog-acl': 'public-read'}'
			with cloudstorage.open(real_path, 'w', content_type=content_t) as f:
				f.write(file_content.read())
			name, url, thumbnail_url = self._get_urls_for(file_name)

	#serving
	def get(self, file_name):
		user = users.get_current_user()
		bucket_name = app_identity.get_default_gcs_bucket_name()
		content_t = mimetypes.guess_type(file_name)[0]
		real_path = os.path.join('/', bucket_name, user.user_id(), file_name)
		try:
			with cloudstorage.open(real_path, 'r') as f:
				self.response.headers.add_header('Content-Type',content_t)
				self.response.out.write(f.read())
		except cloudstorage.errors.NotFoundError:
			self.abort(404)




"""

	PERFORMANCE DATASTORE

		Tips:
			Add explicit (indexed = False) to ndb models' properties that doesn't need and index, speeding up writing operations
			Add modules when there's a lot of traffic calling for async background work:
				(1) at app.yaml add "module: default"
				(2) at root folder add dispatch.yaml file with following contents:
					dispatch:
						-	url: "*/backend"
						 	module: backend
						- 	url: "*/*"
						 	module: default
				(3) at root folder add backend.yaml equivalent to app.yaml but with specified handlers and "module: backend"
				(4) at root folder add backend_main.py equivalent to main.py but with specified routes files for backend, i.e. route:
					app = webapp2.WSGIApplication([
							(r'/backend', BackendCronJob),
							], debug=True)

	
"""
class PerformanceDatastore(webapp2.RequestHandler):
	@ndb.tasklet
	def _my_method(self, entities):
		for entity in entities:
			_ent = yield entity.get_async()
			try:
				#do something
			except Exception as e:
				#do something
				pass


	def get(self):
		params = {}

		"""
			mapping: much more efficient using tasklets than doing a simple for loop
		"""
		my_entities = MyModel.query(MyModel.prop == 'my_param').map(self._my_method)



		"""
			asynchronous loading
		"""
		my_entities = MyModel.query(MyModel.prop == 'my_param').fetch_async()

		#do some parallel work here
		
		params['my_entities'] = my_entities.get_result()


"""

	HANDLING GOOGLE CLOUD SQL
		Tips:
			Create tables is recommended only from MySQL client at cloud shell console


"""
