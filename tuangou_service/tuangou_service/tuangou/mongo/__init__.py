from armory.tank.mongo import ArmoryMongo

conf = {'tuangou': 'mongodb://127.0.0.1/tuangou'}
ArmoryMongo.init_conf(conf)
mongo = ArmoryMongo['tuangou']