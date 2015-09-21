import sys
sys.path.append("../../")
from spider.model.city import City
from spider.model.deal import Deal
from spider import model
from spider.model import orm

def save_list(content_list):
    try:
        orm.session.add_all(content_list)
        orm.session.flush()
        return True
    except Exception as e:
        return False

def update(table, data, cond_name):
    res = table.__class__.query.filter(getattr(table.__class__, cond_name) == getattr(table, cond_name))
    res.update(data)
    if res.first():
        return res.first().id
    else:
        return None


def insert(data):
    orm.session.add(data)
    orm.session.flush()
    return data.id
    
def get_city_from_mysql():
    return City.query.all()

if __name__ == '__main__':
    pass
    # # for i in get_city_from_mysql():
    # #     print i.id
    # t = City(None, '0', None, None)
    # # t_list = [t]
    # t1 = City(None, '0', "02", "02")
    # # t_list.append(t1)
    # insert(t1)
    # # save_list(t_list)
    # update_deal(t, {"first_char":2})