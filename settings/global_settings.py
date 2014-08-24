# vim:sw=3:ts=3:fileencoding=utf-8:list:listchars=tab\:»·,trail\:·:noexpandtab:
# :encoding=utf-8:indentSize=3:tabSize=3:noTabs=false:

ADMINS = [ ]  # a list to which the user_host.py files will append items.  If
              # this is global to your setup, then by all means, add
              # names/emails here.

# NEVER EVER have DEBUG enabled on a production site.  Thus these defaults.
DEBUG = False
TEMPLATE_DEBUG = False


MANAGERS = ADMINS

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
  'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.Loader',
]

TEMPLATE_CONTEXT_PROCESSORS = [
  'django.contrib.messages.context_processors.messages',
]

MIDDLEWARE_CLASSES = [
  'django.middleware.gzip.GZipMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
#  'django.middleware.locale.LocaleMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webui.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'webui.wsgi.application'

INSTALLED_APPS = [
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  # 'django.contrib.sites',
  'django.contrib.messages',
  'django.contrib.staticfiles',

  'process_interface',
]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'filters': {
    'require_debug_false': {
      '()': 'django.utils.log.RequireDebugFalse'
    }
  },
  'handlers': {
    'mail_admins': {
      'level': 'ERROR',
      'filters': ['require_debug_false'],
      'class': 'django.utils.log.AdminEmailHandler'
    }
  },
  'loggers': {
    'django.request': {
      'handlers': ['mail_admins'],
      'level': 'ERROR',
      'propagate': True,
    },
  }
}

CD = {
  'JQUERYBASE'        : '//cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3',
  'CANJS'             : '//cdnjs.cloudflare.com/ajax/libs/can.js/1.1.7',
}
