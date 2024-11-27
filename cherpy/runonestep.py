import pprint

import requests
import os
import sys
from loguru import logger


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
        logger.error(f"Get object summary failed: {response.text}")
        sys.exit(1)
    data = response.json()

    # check if data is a list
    if data:
        if isinstance(data, list):
            data = data[0]
        return data
    else:
        logger.error(f"{object_name} not found")
        sys.exit(1)


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
        logger.error(f"Get onestep failed: {response.json()['errorMessage']}")
        # logger.error(pprint.pformat(response.json()))
        sys.exit(1)
    data = response.json()
    onestep = _recurse_onestep(data['root'], onestep_name)
    if onestep:
        logger.info(f"Found this onestep {onestep_name}")
        logger.info(pprint.pformat(onestep))
        return onestep
    else:
        error_message = f"Unable to find Onestep: {onestep_name} in association: {association}"
        logger.error(error_message)
        sys.exit(1)


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
        logger.error(f"Attempt to run onestep {onestep_name} failed: {e}")
        sys.exit(1)
    return response.json()
