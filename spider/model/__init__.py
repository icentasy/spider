from armory.tank.mysql import ArmoryOrm

conf = {"db": "mysql://root:123456@localhost:3306/tuangou?charset=utf8",
        "DEBUG": False}
orm = ArmoryOrm()
orm.init_conf(conf)