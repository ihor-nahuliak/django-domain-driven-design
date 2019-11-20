from ._settings import REQUIREMENTS_APPS, REQUIREMENTS_MIDDLEWARE, DEBUG


if DEBUG:
    REQUIREMENTS_APPS.append('debug_toolbar')
    REQUIREMENTS_MIDDLEWARE.append(
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    )

    def show_toolbar(request):
        if not request.user.is_staff:
            return False
        return bool(DEBUG)

    DEBUG_TOOLBAR_CONFIG = {
        # Toolbar options
        'SHOW_COLLAPSED': True,
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
        # Panel options
        'SQL_WARNING_THRESHOLD': 100,  # ms
    }

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ]
