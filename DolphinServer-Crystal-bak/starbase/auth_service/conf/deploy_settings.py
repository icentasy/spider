PROJECT_NAME = 'auth_service'

VERSION_CONTROL = "dolphindeploy.git"

# The Project Role Alias table.
ROLE_ALIAS = {
    'auth-service': 'Auth service',
}

# The project app table
ROLE_APPS_TABLE = {
    'Auth service': ['auth_service'],
}

# Extra extension to search
EXTRA_EXT_PATTERN = (
    '.conf',
    '.cfg',
    '.xml',
    '.csv',
    '.nginx'
)

# Extra file name to search
EXTRA_CONF_NAME_PATTERN = (
    'settings2.py',
    'version'
)

# Disuse compressor
BUILD_HANDLER_CONFIG = (
    'dolphindeploy.handlers.ConfigurationFileHandler',
)
