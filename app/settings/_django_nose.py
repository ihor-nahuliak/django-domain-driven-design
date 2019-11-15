from ._settings import INSTALLED_APPS


INSTALLED_APPS.append('django_nose')

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-doctest',
    '--doctest-tests',
    '--with-timer',
    '--timer-warning=300ms',
    '--timer-fail=error',
    '--cover-erase',
    '--with-coverage',
    '--cover-package=app',
    '--cover-html',
    '--cover-html-dir=.coverage.html',
]
