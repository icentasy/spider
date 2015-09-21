from tuangou.mongo import mongo


def get(col, cond=None):
    if hasattr(mongo, col):
        return getattr(mongo, col).find_one(cond)
    else:
        return None


def is_exists(col, cond):
    if hasattr(mongo, col):
        if getattr(mongo, col).find_one(cond):
            return True
    return False