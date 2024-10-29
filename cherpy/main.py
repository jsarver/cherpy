import csv
import json
import os
import requests
import attr
from loguru import logger
import sys

from cherpy.auth import create_headers_dict

service_methods = {'getbusinessobjectsummary': {"url": "/api/V1/getbusinessobjectsummary/busobname"},
                   'getquicksearchresults': {"url": "/api/V1/getquicksearchresults"},
                   'getsearchresults': {"url": "/api/V1/getsearchresults"},
                   'getbusinessobjecttemplate': {"url": "/api/V1/getbusinessobjecttemplate"},
                   'savebusinessobjectbatch': {"url": "/api/V1/savebusinessobjectbatch"},
                   'login': {"url": "/token"}
                   }


@attr.s
class ServiceRequest(object):
    client = attr.ib()
    service_method = attr.ib()

    @property
    def action_url(self):
        return "{host}/{url}".format(host=self.client.host, url=self.lookup_service_url(self.service_method))

    @property
    def headers(self):
        return create_headers_dict(self.client.access_token)

    def lookup_service_url(self, name):
        s = service_methods.get(name)
        if not s:
            return "/api/V1/{}".format(name)
        return s['url']


@attr.s
class Fields(object):
    _fields = attr.ib()

    def __attrs_post_init__(self):
        if self._fields:
            for d in self._fields:
                setattr(self, d["name"].lower(), d)

    def __iter__(self):
        for i in self._fields:
            return i


def init_fields(field_dict):
    return Fields(field_dict)


@attr.s
class ObjectSchema(object):
    busObId = attr.ib()
    name = attr.ib()
    displayName = attr.ib(default=None)
    firstRecIdField = attr.ib(default=None)
    fieldDefinitions = attr.ib(default=None, converter=init_fields)
    gridDefinitions = attr.ib(default=None)
    group = attr.ib(default=None)
    groupSummaries = attr.ib(default=None)
    lookup = attr.ib(default=None)
    major = attr.ib(default=None)
    recIdFields = attr.ib(default=None)
    relationships = attr.ib(default=None)
    stateFieldId = attr.ib(default=None)
    states = attr.ib(default=None)
    supporting = attr.ib(default=None)
    field_template = attr.ib(default=None)
    _fields = attr.ib(default=None)

    def add_field_template(self, template_data):
        """
        Takes data from gettemplateupadteethod and adds it to the 
        field attribute
        :param template_data: 
        :return: 
        """
        self._fields = {f['name'].lower(): f for f in template_data['fields']}

    @property
    def fields(self):
        return self._fields

    def get_field_info_by_name(self, field_name):
        return self.fields[field_name.lower().replace(' ', '')].copy()

    def get_fieldId(self, field_name):
        field = getattr(self.fieldDefinitions, field_name.lower())
        return field['fieldId']

    def create_field_list(self, field_names):
        """
        returns a list of field ids for the field_names provided
        used when trying to limit the number of fields returned when querying cherwell
        :param field_names:
        :return:
        """
        field_list = [self.get_fieldId(f).split('FI:')[1] for f in field_names]
        return field_list


def create_field_template(object_template, field_dict):
    fields = []
    for f in field_dict:
        field_template = object_template.get_field_info_by_name(f)
        field_template['value'] = field_dict[f]
        field_template['dirty'] = "true"
        fields.append(field_template)
    return fields

def create_save_request(object_schema, data_dict):
    logger.info("Creating save request for {}".format(object_schema))
    logger.debug(data_dict)
    d = data_dict
    save_request = {}
    save_request['busObId'] = object_schema.busObId
    save_request['busObRecId'] = d.pop('RecID')
    save_request['fields'] = []
    for f in d:
        field_template = object_schema.get_field_info_by_name(f)
        field_template['value'] = d[f]
        field_template['dirty'] = "true"
        save_request['fields'].append(field_template)
    return save_request


def create_save_requests(object_schema, data_dict):
    request_list = []
    logger.info("Creating save request for {}".format(object_schema))
    for d in data_dict:
        save_request = {}
        save_request['busObId'] = object_schema.busObId
        recid = d.get('RecID')
        if recid:
            save_request['busObRecId'] = d.pop('RecID')
        save_request['fields'] = []
        for f in d:
            field_template = object_schema.get_field_info_by_name(f)
            field_template['value'] = d[f]
            field_template['dirty'] = "true"
            save_request['fields'].append(field_template)
        request_list.append(save_request)
    return {"saveRequests": request_list}


def create_delete_requests(object_schema, data_dict):
    request_list = []
    for d in data_dict:
        delete_request = {}
        delete_request['busObId'] = object_schema.busObId
        delete_request['busObPublicId'] = d.pop('busObPublicId') if d.get('busObPublicId') else ""
        delete_request['busObRecId'] = d.pop('busObRecId')

        request_list.append(delete_request)
    return {"deleteRequests": request_list}


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


def get_object_info(client, object_name=None, object_id=None):
    if all([object_name is None, object_id is None]):
        raise ValueError("Must provide object_name or object_id")
    param_field = "busobname" if object_name else "busobid"
    param_value = object_name if object_name else object_id
    url = "{0}/api/V1/getbusinessobjectsummary/{field}/{value}".format(client.host, field=param_field,
                                                                       value=param_value)
    headers = create_headers_dict(client.access_token)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_dict = response.json()[0]
        obj_id = response_dict.pop('busObId')
        return ObjectSchema(busObId=obj_id, **response_dict)
    else:
        raise Exception(response)


def get_object_schema(client, object_name=None, object_id=None, include_relationships=False):
    if object_id:
        obj_id = object_id
    else:
        o = get_object_info(client, object_name=object_name)
        obj_id = o.busObId
    include_relationships = "true" if include_relationships else "false"
    url = "{0}/api/V1/getbusinessobjectschema/busobid/{1}?includerelationships={2}".format(client.host, obj_id,
                                                                                           include_relationships)
    headers = create_headers_dict(client.access_token)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        ro = response.json()

        ro.pop("hasError")
        ro.pop("errorCode")
        ro.pop("errorMessage")
        return ObjectSchema(**ro)
    else:
        raise ValueError("Unable to retrieve definitions")


def get_object_details(client, object_name, field_list=None, **kwargs):
    bool_dict = {True: "true", False: "False"}
    if field_list:
        include_all = False
        include_required = False
    else:
        include_all = kwargs.get('include_all', True)
        include_required = kwargs.get('include_required', True)
    fields = [] if not field_list else field_list
    obj = get_object_info(client, object_name)

    template = {
        "busObId": obj.busObId,
        "fieldNames":
            fields
        ,
        "fieldIds": [
            "string"
        ],
        "includeAll": bool_dict[include_all],
        "includeRequired": bool_dict[include_required]
    }
    template.update(kwargs)
    url = "{0}/api/V1/getbusinessobjecttemplate".format(client.host)
    headers = create_headers_dict(access_token=client.access_token)
    response = requests.post(url, data=json.dumps(template), headers=headers)
    obj.add_field_template(response.json())
    return obj


def search_object(client, object_id=None, object_name=None, **kwargs):
    """
    Should be used to search for objects
    :param client:
    :param object_id:
    :param object_name:
    :param kwargs:
    :return:
    """
    schema = get_object_schema(client, object_name, object_id)
    data = {
        "filters": [
            {
                "fieldId": "",
                "operator": "",
                "value": ""
            }
        ],
        "association": "",
        "busObId": schema.busObId,
        "customGridDefId": "",
        "dateTimeFormatting": "",
        "fieldId": "",
        "fields": [
            ""
        ],
        "includeAllFields": "",
        "includeSchema": kwargs.get("includeSchema", "false"),
        "pageNumber": 0,
        "pageSize": kwargs.get('pageSize', 0),
        "scope": "",
        "scopeOwner": "",
        "searchId": "",
        "searchName": "",
        "searchText": "",
        "sorting": [
            {
                "fieldId": "",
                "sortDirection": 0
            }
        ],
        "promptValues": [
            {
                "promptId": "",
                "value": {}
            }
        ]
    }
    data.update(**kwargs)
    if kwargs.get('fields'):
        includeAllFields = "false"
        field_list = schema.create_field_list(kwargs.get('fields'))
    else:
        field_list = ""
        includeAllFields = "true"
    data['fields'] = field_list
    data['includeAllFields'] = includeAllFields
    svc = ServiceRequest(client=client, service_method="getsearchresults")
    return requests.post(svc.action_url, headers=svc.headers, data=json.dumps(data))


def save_objects(client, object_records):
    svc = ServiceRequest(client, service_method="savebusinessobjectbatch")
    logger.debug(object_records)
    return requests.post(svc.action_url, headers=svc.headers, data=json.dumps(object_records))


def file_to_dataframe(file_path, file_type="excel"):
    try:
        import pands as pd
    except Exception:
        pass
    if os.path.exists(file_path):
        if file_type == "excel":
            df = pd.read_excel(file_path)
        elif file_type == "csv":
            df = pd.read_csv(file_path)
        return df
    else:
        raise FileNotFoundError("invalid file_path provided {}".format(file_path))


def extract_data(file_name, delimiter=',', encoding='utf-8-sig'):
    columns = None
    data = []
    with open(file_name, encoding=encoding) as inf:
        csv_reader = csv.reader(inf, delimiter=delimiter)
        for row in csv_reader:
            if not columns:
                columns = row
            else:
                data.append(row)
    return columns, data


def create_data_dict(columns, rows):
    return [dict(zip(columns, row)) for row in rows]


# def update_object(client, object_schema, object_data_dict):
#     cs = create_save_requests(obj, object_data_dict)

def update_object_from_file(client, file_name, object_name, delimiter=',', encoding='utf-8-sig'):
    columns, data = extract_data(file_name, delimiter=delimiter)
    obj = get_object_details(client, object_name, fields=columns)
    data_dict = [dict(zip(columns, row)) for row in data]

    cs = create_save_requests(obj, data_dict)
    response = save_objects(client, cs)
    # logger.debug(response.text)
    for row in response.json()['responses']:
        if row['hasError']:
            logger.debug(row)
    return response


class CherwellObjectRecord(object):
    def __init__(self, busobid, recid, busobpublicid=None):
        self.busobid = busobid
        self.recid = recid
        self.busobpublicid = busobpublicid if busobpublicid else ""

    def key_dict(self):
        return {"busObId": self.busobid,
                "busObPublicId": self.busobpublicid,
                "busObRecId": self.recid}


def delete_object(c, objects, stop_on_error=True):
    responses = []
    if isinstance(objects, list) and len(objects) > 1:
        delete_requests = {"deleteRequests": [o.key_dict() for o in objects], "stopOnError": stop_on_error}
        responses = c.post("api/V1/deletebusinessobjectbatch", data=delete_requests)
    else:
        for o in objects:
            responses.append(c.delete(
                "api/V1/deletebusinessobject/busobid/{objectid}/busobrecid/{recid}".format(objectid=o.busobid,
                                                                                           recid=o.recid)))

    return responses


if __name__ == '__main__':
    pass
