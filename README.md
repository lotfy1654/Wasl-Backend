# waslBackendProject
 
# myproject


1- 
pip install whitenoise gunicorn
pip freeze > requirements.txt
python manage.py collectstatic



    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this after SecurityMiddleware
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ALLOWED_HOSTS = ['your-app-name.up.railway.app', '127.0.0.1', 'localhost']


create -----> Procfile
add->->  web: gunicorn myproject.wsgi



create ---> static.json
add ->.> {
  "routes": {
    "/static/*": "staticfiles/*"
  }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Ensure this points to the directory with your custom static files (if any)
]

STATIC_ROOT = BASE_DIR / "staticfiles"



ALLOWED_HOSTS = ['127.0.0.1', 'localhost' , '52.72.118.195']

DEBUG = True







----

CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_SECURE = False  # For development; set to True when using HTTPS in production
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'  # or 'Strict' for stricter enforcement


-----
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_SECURE = False  # For development; set to True for HTTPS in production


----
CORS_ALLOW_ALL_ORIGINS = True




-- 
pip install -r requirements.txt
gunicorn myproject.wsgi


