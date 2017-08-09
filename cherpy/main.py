import json
import attr
import os
import requests
import logging
import pandas as pd
import csv
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('cherpy.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)

from cherpy.api import config_from_file, create_headers_dict

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
        return s['url']


@attr.s
class ObjectSchema(object):
    busObId = attr.ib()
    name = attr.ib()
    displayName = attr.ib(default=None)
    firstRecIdField = attr.ib(default=None)
    group = attr.ib(default=None)
    groupSummaries = attr.ib(default=None)
    lookup = attr.ib(default=None)
    major = attr.ib(default=None)
    recIdFields = attr.ib(default=None)
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


def SaveRequest(object):
    business_object_id = attr.ib()
    business_object_public_id = attr.ib()
    business_object_record_id = attr.ib()
    fields = attr.ib(attr.Factory(list))


def create_field_template(object_template, field_dict):
    fields = []
    for f in field_dict:
        field_template = object_template.get_field_info_by_name(f)
        field_template['value'] = field_dict[f]
        field_template['dirty'] = "true"
        fields.append(field_template)
    return fields


def create_user_request(object_template, data_dict, field_dict=None):
    userinfo = object_template
    data = {
        "accountLocked": "false",
        "busObId": "",
        "displayName": "",
        "ldapRequired": "false",
        "loginId": "",
        "nextPasswordResetDate": "null",
        "password": "P@ssw0rd",
        "passwordNeverExpires": "true",
        "securityGroupId": "",
        "userCannotChangePassword": "false",
        "userMustChangePasswordAtNextLogin": "true",
        "userInfoFields": [
        ],
        "windowsUserId": ""
    }
    data['busObId'] = userinfo.busObId
    data['displayName'] = userinfo.displayName
    data.update(data_dict)

    if field_dict:
        data["userInfoFields"] = create_field_template(userinfo, field_dict)
    return data

def create_save_request(object_schema, data_dict):
    request_list = []
    logger.info("Creating save request for {}".format(object_schema))
    logger.debug(data_dict)
    for d in data_dict:
        save_request = {}
        save_request['busObId'] = object_schema.busObId
        save_request['busObRecId'] = d.pop('RecID')
        save_request['fields'] = []
        for f in d:
            field_template = object_schema.get_field_info_by_name(f)
            field_template['value'] = d[f]
            field_template['dirty'] = "true"
            save_request['fields'].append(field_template)
        request_list.append(save_request)
    return {"saveRequests": request_list}

def create_save_requests(object_schema, data_dict):
    request_list = []
    logger.info("Creating save request for {}".format(object_schema))
    logger.debug(data_dict)
    for d in data_dict:
        save_request = {}
        save_request['busObId'] = object_schema.busObId
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


def get_object_info(client, object_name):
    url = "{0}/api/V1/getbusinessobjectsummary/busobname/{1}".format(client.host, object_name)
    headers = create_headers_dict(client.access_token)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:

        response_dict = response.json()[0]
        obj_id = response_dict.pop('busObId')
        return ObjectSchema(busObId=obj_id, **response_dict)
    else:
        return response


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

    url = "{0}/api/V1/getbusinessobjecttemplate".format(client.host)
    headers = create_headers_dict(access_token=client.access_token)
    response = requests.post(url, data=json.dumps(template), headers=headers)
    obj.add_field_template(response.json())
    return obj


def query_object(client, object_id=None, object_name=None, search_string=None):
    if object_name:
        object_id = get_object_info(client, object_name).busObId
    data = {
        "busObIds": [
            object_id
        ],
        "searchText": search_string
    }
    svc = ServiceRequest(client=client, service_method="getquicksearchresults")
    return requests.post(svc.action_url, headers=svc.headers, data=json.dumps(data))


def search_object(client, object_id=None, object_name=None, **kwargs):
    bool_dict = {True: "true", False: "false"}

    if object_name:
        object_id = get_object_info(client, object_name).busObId
    data = {
        "filters": [
            {
                "fieldId": "",
                "operator": "",
                "value": ""
            }
        ],
        "association": "",
        "busObId": object_id,
        "customGridDefId": "",
        "dateTimeFormatting": "",
        "fieldId": "",
        "fields": [
            ""
        ],
        "includeAllFields": "true",
        "includeSchema": "true",
        "pageNumber": 0,
        "pageSize": 0,
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
    svc = ServiceRequest(client=client, service_method="getsearchresults")
    return requests.post(svc.action_url, headers=svc.headers, data=json.dumps(data))


def save_objects(client, object_records):
    svc = ServiceRequest(client, service_method="savebusinessobjectbatch")
    logger.debug(object_records)
    return requests.post(svc.action_url, headers=svc.headers, data=json.dumps(object_records))

def save_object(client, object_records):
    svc = ServiceRequest(client, service_method="savebusinessobject")
    logger.debug(object_records)
    return requests.post(svc.action_url, headers=svc.headers, data=json.dumps(object_records))


def file_to_dataframe(file_path, file_type="excel"):
    if os.path.exists(file_path):
        if file_type == "excel":
            df = pd.read_excel(file_path)
        elif file_type == "csv":
            df = pd.read_csv(file_path)
        return df
    else:
        raise FileNotFoundError("invalid file_path provided {}".format(file_path))

def extract_data(file_name, delimiter=','):
    columns = None
    data = []
    with open(file_name,encoding='utf-8-sig') as inf:
        csv_reader = csv.reader(inf, delimiter=delimiter)
        for row in csv_reader:
            if not columns:
                columns = row
            else:
                data.append(row)
    return columns, data


def create_data_dict(columns, rows):
    return [dict(zip(columns, row)) for row in rows]


def update_object_from_file(client, file_name, object_name, delimiter=','):
    columns, data = extract_data(file_name, delimiter=delimiter)
    obj = get_object_details(client, object_name, fields=columns)
    data_dict = [dict(zip(columns, row)) for row in data]
    cs = create_save_requests(obj, data_dict)
    response = save_objects(client, cs)
    logger.debug(response.text)
    return response


if __name__ == '__main__':
    import csv

    c = config_from_file()
    c.login()
