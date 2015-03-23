PROJECT_NAME = 'rule_console'

VERSION_CONTROL = "dolphindeploy.git"

# The Project Role Alias table.
ROLE_ALIAS = {
    'rule-console': 'Rule console service',
}

# The project app table
ROLE_APPS_TABLE = {
    'Rule console service': ['rule_console_service'],
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
