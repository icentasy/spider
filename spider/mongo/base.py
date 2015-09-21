from spider.mongo import mongo

def add(col, data):
    if hasattr(mongo, col):
        getattr(mongo, col).insert(data)
        return True
    else:
        return False


def get(col, cond=None):
    if hasattr(mongo, col):
        return getattr(mongo, col).find(cond)
    else:
        return None


def mongo_update(col, cond, data):
    if hasattr(mongo, col):
        getattr(mongo, col).update(cond, {"$addToSet":data}, upsert=False, multi=False)
        return True
    else:
        return False


def is_exists(col, cond):
    if hasattr(mongo, col):
        if getattr(mongo, col).find_one(cond):
            return True
    return False