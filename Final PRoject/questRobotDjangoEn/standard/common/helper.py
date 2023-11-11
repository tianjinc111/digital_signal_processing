import json
import decimal
from django.http import HttpResponse


# json encoder
class JsEncoder(json.JSONEncoder):
    '''
    customer json encoder
    '''
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(JsEncoder, self).default(o)


def jsonResponse(code=1, msg='error', data=None, page=None):
    '''
    format json
    :param code:
    :param msg:
    :param data:
    :param page:
    :return:
    '''
    if data is None:
        data = []
    if page is None:
        page = []
    return HttpResponse(json.dumps({"code": code, "msg": msg, "data": data, "count": page}, cls=JsEncoder))
