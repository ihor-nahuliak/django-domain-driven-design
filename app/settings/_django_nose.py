import sys

from ._settings import REQUIREMENTS_APPS


REQUIREMENTS_APPS.append('django_nose')

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


if sys.version_info[:2] == (3, 8):
    TEST_TIMEOUT_MS = 1000  # Python 3.8 makes the code too slow...
else:
    TEST_TIMEOUT_MS = 300


NOSE_ARGS = [
    '--with-doctest',
    '--doctest-tests',
    '--with-timer',
    f'--timer-warning={TEST_TIMEOUT_MS}ms',
    '--timer-fail=error',
    '--cover-erase',
    '--with-coverage',
    '--cover-package=app',
    '--cover-html',
    '--cover-html-dir=.coverage.html',
]
