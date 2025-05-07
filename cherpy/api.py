import csv
import json
import os
import pprint

import requests
import attr
from loguru import logger

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
        return self.client.headers

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
    logger.info(f"Creating save request for {object_schema.name}")
    for d in data_dict:
        save_request = {'busObId': object_schema.busObId, 'fields': []}
        # get recid value regardless of key case
        if d.get('recid'):
            save_request['busObRecId'] = d.pop('recid')

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


def get_object_info(client, object_name=None, object_id=None):
    if all([object_name is None, object_id is None]):
        raise ValueError("Must provide object_name or object_id")
    param_field = "busobname" if object_name else "busobid"
    param_value = object_name if object_name else object_id
    url = "{0}/api/V1/getbusinessobjectsummary/{field}/{value}".format(client.host, field=param_field,
                                                                       value=param_value)
    response = requests.get(url, headers=client.headers)
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
    response = requests.get(url, headers=client.headers)
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
    response = requests.post(url, data=json.dumps(template), headers=client.headers)
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


def summarize_save_request(save_request, records=3):
    summary_str = f"Sample of first {records} save requests (of {len(save_request['saveRequests'])}):\n"
    for record in save_request['saveRequests'][:records]:
        summary_str += f"BusobId: {record['busObId']}\nFields:\n"
        for field in record['fields']:
            summary_str += f"    {field['name']}: {field['value']}\n"
    return summary_str


def save_objects(client, object_records):
    svc = ServiceRequest(client, service_method="savebusinessobjectbatch")
    logger.debug(f"Saving {len(object_records['saveRequests'])} records")
    logger.debug(summarize_save_request(object_records))
    return requests.post(svc.action_url, headers=svc.headers, data=json.dumps(object_records))


def file_to_dataframe(file_path, file_type="excel"):
    try:
        import pandas as pd
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


def read_csv_data(file_name, delimiter=',', encoding='utf-8-sig'):
    with open(file_name, encoding=encoding) as inf:
        csv_reader = csv.reader(inf, delimiter=delimiter)
        columns = next(csv_reader)
        data = [row for row in csv_reader]
    return columns, data


def convert_to_dict(columns, rows) -> list:
    return [dict(zip(columns, row)) for row in rows]


def update_object_from_file(client, file_name: str, object_name: str, delimiter: str = ',', encoding: str = 'utf-8-sig',
                            batch: int = 1000):
    columns, data = read_csv_data(file_name, delimiter=delimiter, encoding=encoding)
    columns = [c.lower() for c in columns]
    object_schema = get_object_details(client, object_name, fields=columns)
    responses = []
    errors = []
    for row_num in range(0, len(data), batch):
        data_dict = convert_to_dict(columns, data[row_num:row_num + batch])
        save_requests = create_save_requests(object_schema, data_dict)
        response = save_objects(client, save_requests)
        for row in response.json()['responses']:
            if row['hasError']:
                logger.debug(row)
                errors.append(f"{batch}:{row}")
        responses.append(response)
    return responses, errors


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


class CherpyError(Exception):
    """Base exception class for Cherpy errors."""
    pass


class ObjectSummaryError(CherpyError):
    """Exception raised when there's an error getting object summary."""
    pass


class ObjectNotFoundError(CherpyError):
    """Exception raised when an object is not found."""
    pass


class OneStepError(CherpyError):
    """Exception raised when there's an error with a OneStep operation."""
    pass


class OneStepNotFoundError(CherpyError):
    """Exception raised when a OneStep is not found."""
    pass


class RunOneStepError(CherpyError):
    """Exception raised when there's an error running a OneStep."""
    pass


def get_script_directory():
    return os.path.dirname(os.path.abspath(__file__))


def _recurse_onestep(node, search, found_node=None):
    """
    Recursively search for the onestep node tree by name
    :param node:
    :param search:
    :param found_node:
    :return json object matching the search parameter:
    """
    nodes = node.get('childFolders', []) + node.get('childItems', [])
    for n in nodes:
        if found_node:
            return found_node
        if n.get('childFolders') or n.get('childItems'):
            found_node = _recurse_onestep(n, search, found_node)
        else:
            if n.get('name').lower() == search.lower() and found_node is None:
                logger.info("Found it!")
                found_node = n
    return found_node


def get_object_summary(client, object_name):
    base_url = client.host
    url = f"{base_url}/api/V1/getbusinessobjectsummary/busobname/{object_name}"

    logger.info(f"Getting object summary for {object_name}")
    response = requests.get(url, headers=client.headers)
    if response.status_code != 200:
        error_msg = f"Get object summary failed: {response.text}"
        logger.error(error_msg)
        raise ObjectSummaryError(error_msg)
    data = response.json()

    # check if data is a list
    if data:
        if isinstance(data, list):
            data = data[0]
        return data
    else:
        error_msg = f"{object_name} not found"
        logger.error(error_msg)
        raise ObjectNotFoundError(error_msg)


def get_onestep(client, association, scope, onestep_name):
    """
    Get the onestep by name and returns the json object for it
    :param client:
    :param association:
    :param scope:
    :param onestep_name:
    :return:
    """
    association = get_object_summary(client, association).get('busObId')
    base_url = client.host
    url = f"{base_url}/api/V1/getonestepactions/association/{association}/scope/{scope}/scopeowner/{association}"

    response = requests.get(url, headers=client.headers)
    if response.status_code != 200:
        error_msg = f"Get onestep failed: {response.json()['errorMessage']}"
        logger.error(error_msg)
        # logger.error(pprint.pformat(response.json()))
        raise OneStepError(error_msg)
    data = response.json()
    onestep = _recurse_onestep(data['root'], onestep_name)
    if onestep:
        logger.info(f"Found this onestep {onestep_name}")
        logger.info(pprint.pformat(onestep))
        return onestep
    else:
        error_msg = f"Unable to find Onestep: {onestep_name} in association: {association}"
        logger.error(error_msg)
        raise OneStepNotFoundError(error_msg)


def run_onestep(client, association, onestep_name, scope):
    """
    Run the onestep by name
    :param client:
    :param association:
    :param onestep_name:
    :param scope:
    :return:
    """
    onestep = get_onestep(client, association, scope, onestep_name)
    standin_key = onestep.get('standInKey', '').replace(':', '%3A').replace('#', '%23')
    url = f"{client.host}/api/V1/runonestepaction/standinkey/{standin_key}"
    logger.debug(f"Attempting to run the onestep {onestep_name} at endpoint: {url}")
    try:
        response = requests.get(url, headers=client.headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        error_msg = f"Attempt to run onestep {onestep_name} failed: {e}"
        logger.error(error_msg)
        raise RunOneStepError(error_msg)
    return response.json()
