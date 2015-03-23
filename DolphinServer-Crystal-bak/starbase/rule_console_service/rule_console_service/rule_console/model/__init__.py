from armory.tank.mongo import ArmoryMongo
from rule_console.api import app


ArmoryMongo.init_app(app)
