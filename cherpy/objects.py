import attr

class SearchFilter(object):
    def __init__(self, text=None, field=None, operator=None, value=None):
        self.field = field
        self.operator = operator
        self.value = value
        self.text = text
        if text:
            self.from_text(text)

    def from_text(self, filter_text):
        """
        takes filter_text, splits it into field, operator and value
        :param String:
        :return:
        """
        field, operator, *value = filter_text.split(' ')
        self.field = field.strip()
        self.operator = operator.strip()
        if len(value) > 1:
            value = ' '.join(value)
        else:
            value = value[0]
        self.value = value.strip()

    def __repr__(self):
        return f"search_filter({self.field}, {self.operator}, {self.value})"

    def to_dict(self):
        return {"field": self.field, "operator": self.operator, "value": self.value}

class searchResponse(object):
    def __init__(self, raw_response):
        self.data = raw_response
        self.busobid = raw_response['busObId']
        self.busobpublicid = raw_response['busObPublicId']
        self.busobrecid = raw_response['busObRecId']

    def field_list(self):
        return sorted(i['name'] for i in self.data['fields'])

    def __getattr__(self, attribute):
        value = None
        for i in self.data['fields']:
            if i['name'].lower() == attribute.lower():
                value = i['value']
                break
        if not value:
            raise AttributeError(f"Attribute {attribute} not found in response")
        return value

class CherwellObjectRecord(object):
    def __init__(self, busobid, recid, busobpublicid=None):
        self.busobid = busobid
        self.recid = recid
        self.busobpublicid = busobpublicid if busobpublicid else ""

    def key_dict(self):
        return {"busObId": self.busobid,
                "busObPublicId": self.busobpublicid,
                "busObRecId": self.recid}


@attr.s
class NameValueExtractor(object):
    """takes a response object and returns a data dict"""
    response = attr.ib()

    def create_dict(self):
        dict_list = []
        data = self.response.json()
        for obj in data["businessObjects"]:
            dict_list.append({field["name"]: field["value"] for field in obj["fields"]})
        return dict_list


class Fields(object):
    def __init__(self, field_dict, record):
        self.__dict__['field_dict'] = field_dict
        # self.__dict__['record'] = record

    def __getattr__(self, item):
        for field in self.__dict__['field_dict']:

            if field['name'].lower() == item.lower():
                return field['value']

    def __setattr__(self, key, value):
        for field in self.__dict__['field_dict']:
            if field['name'].lower() == key.lower():
                field['value'] = value
                field['dirty'] = True
                self.__dict__['record']._object_dict['persist'] = True

class CherwellRecordSet(object):
    def __init__(self, api_response):
        self.api_response = api_response
        self.records = None
        self.load_records()

    def load_records(self):
        self.records = [CherwellRecord(row) for row in self.api_response.json()['businessObjects']]

    def __iter__(self):
        return iter(self.records)

    def __repr__(self):
        return f"<CherwellRecordSet {len(self.records)} records>"

    def items(self):
        return [record.items() for record in self.records]



class CherwellRecord(object):
    def __init__(self, object_dict):
        self._object_dict = object_dict
        self.field = Fields(object_dict['fields'], self)

    def fields(self):
        return [f['name'] for f in self._object_dict['fields']]

    def __repr__(self):
        return f"<CherwellRecord {self._object_dict['busObPublicId']}>"

    def __getattr__(self, item):
        if item not in self._object_dict:
            return self.field.__getattr__(item)
        return self._object_dict[item]

    def items(self):
        return {i['displayName']:i['value'] for i in self._object_dict['fields']}
