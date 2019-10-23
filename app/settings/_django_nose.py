from ._settings import INSTALLED_APPS


INSTALLED_APPS.append('django_nose')

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-doctest',
    '--doctest-tests',
    '--cover-erase',
    '--with-coverage',
    '--cover-package=app',
    '--cover-html',
    '--cover-html-dir=.coverage.html',
]
