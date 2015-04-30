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
    'MOBILE_REDIRECT_URL': 'http://www.bozzuto.com/apartments/communities/64-mariner-bay-at-annapolis-towne-centre',
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
        '--cover-package=spark101.apps.account.tests,spark101.apps.videos.tests,spark101.apps.portal.tests',
        '--cover-xml',
        '--cover-xml-file=%s/coverage.xml' % results_base_dir,
        '--verbosity=2',
        '--with-xunit',
        '--xunit-file=%s/nosetests.xml' % results_base_dir,
    ]
}

settings.configure(**params)

from django_nose import NoseTestSuiteRunner

runner = NoseTestSuiteRunner()

failures = runner.run_tests(['mobile_redirect'])

if failures:
    sys.exit(failures)
