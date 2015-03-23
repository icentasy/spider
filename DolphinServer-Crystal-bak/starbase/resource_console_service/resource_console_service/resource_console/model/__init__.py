from armory.tank.mongo import ArmoryMongo
from resource_console.api import app


ArmoryMongo.init_app(app)
