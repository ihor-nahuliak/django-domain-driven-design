from ._settings import *  # noqa
from ._languages import *  # noqa
from ._templates import *  # noqa
from ._django_db import *  # noqa
from ._django_auth import *  # noqa
from ._oauth2_provider import *  # noqa
from ._rest_framework import *  # noqa
from ._debug_toolbar import *  # noqa
from ._django_nose import *  # noqa


INSTALLED_APPS = REQUIREMENTS_APPS + PROJECT_APPS
MIDDLEWARE = REQUIREMENTS_MIDDLEWARE + PROJECT_MIDDLEWARE
