import attr


class searchResponse(object):
    def __init__(self, raw_response):
        self.data = raw_response
        self.busobid = raw_response['busObId']
        self.busobpublicid = raw_response['busObPublicId']
        self.busobrecid = raw_response['busObRecId']

    def field_list(self):
        return sorted(i['name'] for i in self.data['fields'])

    def __getattr__(self, attribute):
        for i in self.data['fields']:
            if i['name'].lower() == attribute.lower():
                return i['value']


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
