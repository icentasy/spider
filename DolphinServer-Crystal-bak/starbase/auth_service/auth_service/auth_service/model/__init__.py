from armory.tank.mongo import ArmoryMongo
from auth_service.settings import MONGO_CONFIG

ArmoryMongo.init_conf(MONGO_CONFIG)
