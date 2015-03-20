from armory.tank.mysql import ArmoryOrm
from tuangou.api import app


orm = ArmoryOrm()
orm.init_app(app)
