import json
import subprocess
import click
from cherpy import config_from_env, get_object_schema, update_object_from_file
from cherpy.auth import config_from_file
from cherpy.main import get_object_info, search_object, create_delete_requests
from cherpy.utils import get_save_file_path, NameValueExtractor, get_open_file_path, dict_to_csv, create_temp_file
from cherpy.runonestep import run_onestep
from loguru import logger


@click.group()
def csm():
    pass


@csm.command('run-onestep')
@click.option('--env', default="CHEWEY_CONFIG", prompt="Please provide Environment to get config file")
@click.option('--association', default=None)
@click.option('--onestep-name', default=None)
@click.option('--scope', default="Global")
@click.option('--scope-owner', default=None)
def run_onestep_cli(env, association, onestep_name, scope, scope_owner):
    """
    Command-line interface to run a Cherwell onestep action.
    """
    logger.info(f'Current Env: {env}')
    cfg = config_from_env(env=env)
    if scope_owner is None:
        scope_owner = association
    response = run_onestep(cfg, association=association, onestep_name=onestep_name, scope=scope,
                           scope_owner=scope_owner,
                           prompts=None)
    print(json.dumps(response, indent=2))


@click.command('get-schema')
@click.option('--env', default="CHEWEY_CONFIG", prompt="Please provide Environment to get config file")
@click.option('--object_name', default=None)
@click.option('--object_id', default=None)
@click.option('--output_file', default=None)
@click.argument('fields', nargs=-1)
def get_schema_cli(object_name, output_file=None, env=None, fields=None, object_id=None, **kwargs):
    logger.info(f'Current Env: {env}')
    client = config_from_env(env=env)

    client.login()
    obj_id = None
    if object_id:
        obj_id = object_id
    elif not object_name:
        object_name = click.prompt("Please type an object name")
    o = get_object_schema(client, object_name, obj_id)

    fd = o.fieldDefinitions

    if not output_file:
        # output_file = get_save_file_path()
        click.echo(o)
    else:
        with open(output_file, 'w') as out:
            out.writelines(o)

    return o


@click.command('delete')
@click.option('--env', prompt="Env variable that contains config file path")
@click.option('--object-name', prompt="provide cherwell object")
@click.option('--chunk-size', prompt="Number of records to delete at a time")
def delete_objects_cli(object_name, env, chunk_size=300):
    client = config_from_env(env=env)
    client.login()
    del_obj_info = get_object_info(client, object_name)
    row_count = 1
    total_del = 0
    current_page = 1
    while row_count > 0:
        try:
            del_dict = search_object(client, object_id=del_obj_info.busObId, fields=["RecId"],
                                     pageSize=chunk_size, pageNumber=current_page).json()
            row_count = len(del_dict['businessObjects'])
            click.echo("{} of {} records found".format(row_count, del_dict['totalRows']))
            if row_count > 0:
                del_requests = create_delete_requests(del_obj_info, del_dict['businessObjects'])
                r = client.post("api/V1/deletebusinessobjectbatch", data=del_requests)
                logger.debug(r.content)
            total_del += row_count
            current_page += 1
            click.echo("{} objects deleted".format(total_del))
        except Exception as e:
            row_count = 0
            click.echo("expection {}".format(e))
    return


@click.command('publish')
@click.option('--connection', prompt="Cherwell connection file")
@click.option('--blueprint', prompt="blueprint Path ")
def publish_blueprint(connection, blueprint):
    subprocess.Popen('')


@click.command('update')
@click.option('--env', prompt="Please provide Environment to get config file")
@click.option('--object-name', prompt="provide cherwell object")
@click.option('--input-file-path', default=None)
def update_object_cli(object_name, input_file_path=None, env=None):
    """
        :param env: Environmental variable storing location of configuration file
        :param object_name: Name of the Cherwell object
        :param ask_file: pass this flag if you want to be prompted for filename
        :param input_file_path: file name of data for object you want to create
        :return:
    """
    client = config_from_env(env=env)
    client.login()
    if not input_file_path:
        input_file_path = get_open_file_path()
    click.echo(input_file_path)
    response = update_object_from_file(client=client, file_name=input_file_path, object_name=object_name, delimiter=",",
                                       encoding='utf-9-sig')
    count = 0
    for r in response.json()['responses']:
        count += 1
        if r['hasError']:
            click.echo("{}:{}".format(r, str(count)))
            logger.debug("{}:{}".format(r, str(count)))
    return response


# TODO add docstrings to all the commands
# TODO cleanup the readme file with some good examples
# TODO add a login decorator for all the commands that require login
@click.command('create')
@click.option('--object-name', prompt="provide cherwell object")
@click.option('--env', default=None)
@click.option('--cfg-file', default=None)
@click.option('--input-file', default=None)
@click.option('--ask-file', is_flag=True)
@click.argument('object-data', nargs=-1)
def create_object(object_name, ask_file, input_file=None, env=None, cfg_file=None, object_data=None):
    """

    :param cfg_file:
    :param object_name: name of the Cherwell object
    :param ask_file: pass this flag if you want to be prompted for filename
    :param input_file: filename of data for object you want to create
    :param env: Environmental variable storing location of configuration file
    :param object_data: key value pairs for creating object
    :return:
    """
    if env:
        client = config_from_env(env=env)
    elif cfg_file:
        client = config_from_file(cfg_file)
    else:
        click.BadParameter("stuff")
        click.echo("You must provide cfg path (--cfg_path) or environment variable containing it (--cfg_var)")
        return

    client.login()
    # if no file is provided but ask_file is passed then it prompts for file, if neither is provided
    # assumes that object data is provided, otherwise there is an error
    if not input_file:
        if ask_file:
            input_file = get_open_file_path()
        elif object_data:
            input_file = "temp_file.txt"
            create_temp_file(object_data, input_file)
        else:
            raise ValueError("no file or object data provided")

    # click.echo(input_file)
    response = update_object_from_file(client=client, file_name=input_file, object_name=object_name, delimiter=",",
                                       encoding='utf-9-sig')
    count = 0
    for r in response.json()['responses']:
        count += 1
        if r['hasError']:
            logger.debug("{}:{}".format(r, str(count)))
    return response


@click.command('search')
@click.option('--object-name', default=None)
@click.option('--env', default="CHEWEY_CONFIG", prompt="Please provide Environment to get config file")
@click.option('--output-file', default=None)
@click.option('--search-text', 'searchText', default="")
@click.option('--page-size', 'pageSize', default=20000)
@click.option('--page-number', 'pageNumber', default=0)
@click.argument('fields', nargs=-1)
def search_object_cli(object_name, output_file=None, env=None, fields="", **kwargs):
    if not object_name:
        object_name = click.prompt("Please type an object name")
        if not object_name:
            click.MissingParameter("No Object Name was provided")
            return
    client = config_from_env(env=env)
    client.login()
    if not output_file:
        output_file = get_save_file_path()
    response = search_object(client, object_name=object_name, fields=fields, **kwargs)
    data_dict = NameValueExtractor(response).create_dict()
    dict_to_csv(data_dict, data_dict[0].keys(), output_file, mode="w")

    return response


csm.add_command(get_schema_cli)
csm.add_command(create_object)
csm.add_command(delete_objects_cli)
csm.add_command(search_object_cli)
csm.add_command(get_schema_cli)
csm.add_command(run_onestep_cli)

if __name__ == '__main__':
    csm()
