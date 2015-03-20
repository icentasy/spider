PROJECT_NAME = 'dolphin_weather'

VERSION_CONTROL = "dolphindeploy.git"

# The Project Role Alias table.
ROLE_ALIAS = {
    'dolphin-weather': 'Dolphin Weather Service',
}

# The project app table
ROLE_APPS_TABLE = {
    'Dolphin Weather Service': ['dolphin_weather'],
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
