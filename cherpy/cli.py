import json
import click
from cherpy import config_from_env, get_object_schema, update_object_from_file
from cherpy.auth import config_from_file
from cherpy.main import get_object_info, search_object, create_delete_requests
from cherpy.utils import get_save_file_path, NameValueExtractor, get_open_file_path, dict_to_csv, create_temp_file
from cherpy.runonestep import run_onestep, get_onestep
from loguru import logger


def object_option(option_help="Cherwell object name"):
    """
    This option will allow the user to specify the Cherwell object name
    :return:
    """
    return click.option('--object-name', default=None, help=option_help)


def env_option(option_help="Environment variable that contains the path to the config file"):
    """
    This option will allow the user to specify the environment variable that contains the path to the config file
    :return:
    """
    return click.option('-e', '--env', default="cherpy_config",
                        prompt="Enter environment variable containing config file path",
                        help=option_help)


def input_option(option_help="Path to the input file"):
    """
    This option will allow the user to specify the path to the input file
    :return:
    """
    return click.option('-i', '--input-path', default=None, help=option_help)


def output_option(option_help="Path to the output file"):
    """
    This option will allow the user to specify the path to the output file
    :return:
    """
    return click.option('-o', '--output-path', default=None, help=option_help)


def browse_file_option(option_help="Browse for file path"):
    """
    This option will allow the user to browse for a file path
    :return:
    """
    return click.option('-a', '--ask-file', is_flag=True, help=option_help)


def field_argument():
    """
    This argument will allow the user to specify the fields to return
    :return:
    """
    return click.argument('fields', nargs=-1)


@click.group()
def csm():
    pass


@click.command('get-onestep')
@env_option()
@object_option()
@click.option('-on', '--onestep-name', default=None, help='Name of the onestep')
@click.option('-sc', '--scope', default="Global", help='Scope of the onestep')
def get_onestep_cli(env, object_name, onestep_name, scope):
    """
    Searches for and returns the standing key for a one step in Cherwell
    """
    logger.info(f'Current Env: {env}')
    logger.info(f'Searching for {onestep_name} in {scope} for Association: {object_name}')
    client = config_from_env(env=env)
    standin_key = get_onestep(client=client, association=object_name, onestep_name=onestep_name, scope=scope)
    click.echo(standin_key)


@click.command('run-onestep')
@env_option()
@object_option()
@click.option('-on', '--onestep-name', default=None, help='Name of the onestep')
@click.option('-sc', '--scope', default="Global", help='Scope of the onestep')
def run_onestep_cli(env, object_name, onestep_name, scope):
    """
    Call a one step in Cherwell
    """
    logger.info(f'Current Env: {env}')
    client = config_from_env(env=env)
    response = run_onestep(client, association=object_name, onestep_name=onestep_name, scope=scope)
    print(json.dumps(response, indent=2))


@click.command('get-schema')
@env_option()
@object_option()
@output_option()
@field_argument()
def get_schema_cli(object_name, output_path=None, env=None):
    """
    Returns Schema information for a Cherwell object to the console or a file
    :param object_name:
    :param output_path:
    :param env:
    :param fields:
    :param object_id:
    :param kwargs:
    :return:
    """
    logger.info(f'Current Env: {env}')
    client = config_from_env(env=env)

    if not object_name:
        object_name = click.prompt("Please type an object name")
    o = get_object_schema(client, object_name)

    # fd = o.fieldDefinitions

    if not output_path:
        # output_file = get_save_file_path()
        click.echo(o)
    else:
        with open(output_path, 'w') as out:
            out.writelines(o)

    return o


@click.command('delete')
@env_option()
@object_option()
@click.option('--chunk-size', prompt="Number of records to delete at a time",
              help='Number of records to delete in each batch')
def delete_object_cli(object_name, env, chunk_size=300):
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
            click.echo("exception {}".format(e))
    return


@click.command('update')
@env_option()
@object_option()
@input_option()
@browse_file_option()
def update_object_cli(object_name, input_path=None, env=None, ask_file=False):
    """
    Update only! if matching record not found it will not create a new record. Input file must contain a RecId field
        :param ask_file: This flag will open a file dialog to browse for the input file
        :param env: Environmental variable storing location of configuration file
        :param object_name: Name of the Cherwell object
        :param input_path: file name of data for object you want to create
        :return:
    """
    if ask_file:
        input_path = get_open_file_path()
    client = config_from_env(env=env)

    if not input_path:
        input_path = get_open_file_path()
    click.echo(input_path)

    # check for RecId field in the file
    with open(input_path, 'r') as f:
        first_line = f.readline()
        if "recid" not in first_line.lower():
            raise ValueError(
                "RecID column not found in file. It is required when using the update command")
    responses, errors = update_object_from_file(client=client, file_name=input_path, object_name=object_name,
                                                delimiter=",",
                                                encoding='utf-8-sig')
    for error in errors:
        click.echo(error)
    return f"Updated {len(responses)} records"


@click.command('create')
@env_option()
@object_option(option_help='Object name for the record you are creating')
@click.option('--config-path', default=None, help='Full path to the configuration file')
@input_option(option_help='Full path to the file containing new record data')
@browse_file_option(option_help='This flag will open a file dialog to browse for the input file')
@click.argument('object-data', nargs=-1)
def create_object_cli(object_name, ask_file, input_path=None, env=None, config_path=None, object_data=None):
    """
    Create a new Cherwell record from an input file or key value pairs

    :param object_name: Name of the Cherwell object
    :param env: Environmental variable storing location of configuration file
    :param config_path: full path to the configuration file
    :param ask_file: This flag will open a file dialog to browse for the input file
    :param input_path: path to file with data for object you want to create
    :param object_data: key value pairs for creating object if you don't want to use an input file
    :return:

    """
    if env:
        client = config_from_env(env=env)
    elif config_path:
        client = config_from_file(config_path)
    else:
        click.BadParameter("You must provide cfg path (--cfg_path) or environment variable containing it (--cfg_var)")
        click.echo("You must provide cfg path (--cfg_path) or environment variable containing it (--cfg_var)")
        return

    # if no file is provided but ask_file is passed then it prompts for file, if neither is provided
    # assumes that object data is provided, otherwise there is an error
    if not input_path:
        if ask_file:
            input_path = get_open_file_path()
        elif object_data:
            input_path = "temp_file.txt"
            create_temp_file(object_data, input_path)
        else:
            raise ValueError("no file or object data provided")

    # click.echo(input_file)
    responses, errors = update_object_from_file(client=client, file_name=input_path, object_name=object_name,
                                                delimiter=",",
                                                encoding='utf-8-sig')
    for error in errors:
        click.echo(error)
    return f"Created {len(responses)} records"


@click.command('search')
@env_option()
@object_option(option_help='Name of the Cherwell object to search')
@output_option(option_help='File path to save the search results')
@click.option('-s', '--search-text', 'searchText', default="", help='Free text search')
@click.option('-ps', '--page-size', 'pageSize', default=20000, help='Number of records per page')
@click.option('-pg', '--page-number', 'pageNumber', default=0, help='Page number to retrieve')
@field_argument()
def search_object_cli(object_name, output_path=None, env=None, fields="", **kwargs):
    """
    Search for records in Cherwell and save the results to a file

    :param object_name:
    :param output_path:
    :param env:
    :param fields:
    :param kwargs:
    :return:
    """
    if not object_name:
        object_name = click.prompt("Please type an object name")
        if not object_name:
            click.MissingParameter("No Object Name was provided")
            return
    client = config_from_env(env=env)
    client.login()
    if not output_path:
        output_path = get_save_file_path()
    response = search_object(client, object_name=object_name, fields=fields, **kwargs)
    data_dict = NameValueExtractor(response).create_dict()
    dict_to_csv(data_dict, data_dict[0].keys(), output_path, mode="w")

    return response


csm.add_command(get_schema_cli)
csm.add_command(create_object_cli)
csm.add_command(update_object_cli)
csm.add_command(delete_object_cli)
csm.add_command(search_object_cli)
csm.add_command(run_onestep_cli)
csm.add_command(get_onestep_cli)

if __name__ == '__main__':
    csm()
