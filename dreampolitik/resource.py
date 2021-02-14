from .exception import Error


class ResourceCollection(dict):
    def __init__(self, resource_dict=None):
        if resource_dict:
            super(ResourceCollection, self).__init__(resource_dict)

    def __add__(self, other):
        result = ResourceCollection()    
        for res_id in self:
            if res_id in other:
                res_amount = self[res_id] + other[res_id]
            else:
                res_amount = self[res_id]
            result[res_id] = res_amount
        for res_id in other:
            if res_id not in self:
                result[res_id] = other[res_id]
        return result

    def __sub__(self, other):
        result = ResourceCollection()
        for res_id, amount in other.items():
            diff = self[res_id] - amount
            # TODO: Check for a negative value
            result[res_id] = diff
        for res_id in self:
            if res_id not in other:
                result[res_id] = self[res_id]
        return result
            
    def __gt__(self, other):
        gt_cmp = lambda res_x, res_y: res_x > res_y
        return self._res_cmp(other, gt_cmp)

    def __ge__(self, other):
        ge_cmp = lambda res_x, res_y: res_x >= res_y
        return self._res_cmp(other, ge_cmp)

    def __lt__(self, other):
        return other > self

    def __le__(self, other):
        return other >= self

    def _res_cmp(self, other, cmp_fn):
        """ Used for implementing the arithmetic comparison operators """
        result = True
        for res_id in other:
            if res_id in self:
                if not cmp_fn(self[res_id], other[res_id]):
                    result = False
                    break
            else:
                result = False
                break
        return result

class ResourceArithmeticError(Error):
    def __init__(self, message):
        self.message = message
