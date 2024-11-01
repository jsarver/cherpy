import requests
import os
import sys
from loguru import logger


def get_script_directory():
    return os.path.dirname(os.path.abspath(__file__))


def recurse(node, search, found_node=None):
    nodes = node.get('childFolders', []) + node.get('childItems', [])
    for n in nodes:
        if found_node:
            return found_node
        if n.get('childFolders') or n.get('childItems'):
            found_node = recurse(n, search, found_node)
        else:
            if n.get('name') == search and found_node is None:
                logger.info("Found it!")
                found_node = n
    return found_node


def get_onestep(cfg, association, scope, onestep_name, token):
    base_url = cfg['host']
    url = f"{base_url}/api/V1/getonestepactions/association/{association}/scope/{scope}/scopeowner/{association}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"Get onestep failed: {response.text}")
        sys.exit(1)
    data = response.json()
    onestep = recurse(data['root'], onestep_name)
    if onestep and onestep.get('name') == onestep_name:
        logger.info(f"Found this onestep {onestep_name}")
        return onestep
    else:
        error_message = f"Unable to find Onestep: {onestep_name} in association: {association}"
        logger.error(error_message)
        sys.exit(1)


def get_object_summary(cfg, object_name, token):
    base_url = cfg['host']
    url = f"{base_url}/api/V1/getbusinessobjectsummary/busobname/{object_name}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    logger.info(f"Getting object summary for {object_name}")
    response = requests.get(url, headers=headers)
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


def run_onestep(cfg, association, onestep_name, scope, token):
    object_summary = get_object_summary(cfg, association, token)
    bus_ob_id = object_summary.get('busObId')
    onestep = get_onestep(cfg, bus_ob_id, scope, onestep_name, token)
    standin_key = onestep.get('StandInKey', '').replace(':', '%3A').replace('#', '%23')
    base_url = cfg['host']
    url = f"{base_url}/api/V1/runonestepaction/standinkey/{standin_key}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    logger.info(f"Attempting to run the onestep {onestep_name} at endpoint: {url}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Attempt to run onestep {onestep_name} failed: {e}")
        sys.exit(1)
    return response.json()
