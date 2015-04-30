import os
import sys
from django.conf import settings

DIRNAME = os.path.dirname(__file__)

results_base_dir = os.environ.get('CIRCLE_TEST_REPORTS', os.path.join(DIRNAME, '.test_results'))

params = {
    'DEBUG': True,
    'INSTALLED_APPS': [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'mobile_redirect',
    ],
    'MIDDLEWARE_CLASSES': [
        'mobile_redirect.middleware.MobileRedirectMiddleware',
    ],
    'MOBILE_REDIRECT_URL': 'https://github.com/ryanbagwell/django-mobile-redirect',
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'circle_test',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': '127.0.0.1',
        }
    },
    'NOSE_ARGS': [
        '--with-coverage',
        '--cover-package=mobile_redirect.tests',
        '--cover-xml',
        '--cover-xml-file=%s/coverage.xml' % results_base_dir,
        '--with-xunit',
        '--xunit-file=%s/nosetests.xml' % results_base_dir,
    ],
    'ROOT_URLCONF': 'mobile_redirect.tests.urls',
}

settings.configure(**params)

from django_nose import NoseTestSuiteRunner

runner = NoseTestSuiteRunner()

failures = runner.run_tests(['mobile_redirect'])

if failures:
    sys.exit(failures)
