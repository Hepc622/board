import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj) == Decimal:
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)

