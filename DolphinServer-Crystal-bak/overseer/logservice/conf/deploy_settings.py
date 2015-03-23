PROJECT_NAME = 'Broodling'

VERSION_CONTROL = 'dolphindeploy.git'

ROLE_ALIAS = {
    'dolphinstat_role' : "Broodling",
}

ROLE_APPS_TABLE = {
    'Broodling' : [ 'Broodling' ],
}

BUILD_HANDLER_CONFIG = (
    'dolphindeploy.handlers.ConfigurationFileHandler',
)
