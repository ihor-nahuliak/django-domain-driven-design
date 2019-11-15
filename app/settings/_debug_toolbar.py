from ._settings import REQUIREMENTS_APPS, REQUIREMENTS_MIDDLEWARE, DEBUG


if DEBUG:
    REQUIREMENTS_APPS.append('debug_toolbar')
    REQUIREMENTS_MIDDLEWARE.append(
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    )
