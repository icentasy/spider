import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("DolphinService LogParse")

def init_log(log_path='./log/parse.log', maxB=10 * 1024 * 1024, bc=5, level=logging.DEBUG):
    Rthandler = RotatingFileHandler(
        log_path, maxBytes=int(maxB), backupCount=int(bc))
    formatter = logging.Formatter(
        '[%(process)d]%(asctime)s %(levelname)s %(message)s')
    Rthandler.setFormatter(formatter)
    logger.addHandler(Rthandler)
    logger.setLevel(int(level))
    logger.info("log init complete!")
