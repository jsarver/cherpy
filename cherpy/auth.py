import json
import attr
import yaml
import os
import datetime
from functools import wraps
from loguru import logger
import sys

# Check if requests is already in sys.modules
requests = sys.modules.get('requests')

# If it's not already imported, try to import it
if requests is None:
    try:
        import requests
    except ImportError as e:
        raise ImportError("The 'requests' package is required but not installed. "
                          "Please install it using 'pip install requests'") from e
DEFAULT_CONFIG = {}


def check_expired(func):
    @wraps(func)
    def refresh_wrapper(*args, **kwargs):
        cls = args[0]
        if cls.expired:
            cls.login()
        return func(*args, **kwargs)

    return refresh_wrapper


def config_from_file(file_name):
    with open(file_name) as f:
        cfg = yaml.safe_load(f)
    return Client(**cfg)


def config_from_env(env="CHEWEY_CONFIG"):
    file_name = os.environ[env]
    client = config_from_file(file_name)
    return client


def create_config(filename="cherpy.yml", **kwargs):
    file_path = os.path.join(os.environ['USERPROFILE'], ".cherpy", filename)
    c = Client(**kwargs)
    cfg_dict = attr.asdict(c, filter=attr.filters.exclude(attr.fields(Client).access_token))
    with open(file_path, 'w') as outf:
        yaml.dump(cfg_dict, outf, default_flow_style=False)
    os.system("SETX {0} {1}".format("CHEWEY_CONFIG", file_path))


def create_headers_dict(access_token):
    headers = {"Authorization": "Bearer {}".format(access_token),
               "Content-type": "application/json",
               "Accept": "application/json"}
    return headers


def refresh(client_id, host, refresh_token):
    data = "grant_type=refresh_token&client_id={client}&refresh_token={refresh_token}" \
        .format(client=client_id, refresh_token=refresh_token)
    url = "{host}/token".format(host=host)
    response = requests.post(url, data=data).json()
    return response


@attr.s
class Client:
    """
    param host:
    param user
    param password
    param client_id
    param grant_type
    param auth_mode
    param access_token
    param expires_in
    param expires
    param issued
    param refresh_token
    """
    host = attr.ib()
    user = attr.ib()
    password = attr.ib(repr=False)
    client_id = attr.ib()
    grant_type = attr.ib(default="password")
    auth_mode = attr.ib(default="internal")
    access_token = attr.ib(default=None)
    expires_in = attr.ib(default=None)
    expires = attr.ib(default=None)
    issued = attr.ib(default=None)
    refresh_token = attr.ib(default=None)
    refresh_automatically = attr.ib(default=True)
    token_type = attr.ib(default=None)

    def __str__(self):
        return (
            f"Client(host={self.host}, user={self.user}, password=***, client_id={self.client_id}, "
            f"grant_type={self.grant_type}, auth_mode={self.auth_mode}, access_token={self.access_token}, "
            f"expires_in={self.expires_in}, expires={self.expires}, issued={self.issued}, "
            f"refresh_token={self.refresh_token}, refresh_automatically={self.refresh_automatically}, token_type={self.token_type})"
        )

    def login(self):
        if self.refresh_token and self.expired:
            logger.debug('Token expired, refreshing login')
            if self.refresh_token:
                self._access_response = refresh(self.client_id, self.host, self.refresh_token)
        else:
            self._access_response = login(self.user, self.password, self.client_id, self.host, self.grant_type,
                                          self.auth_mode)
        if not self._access_response.get('access_token'):
            raise ValueError("unable to Login")
        else:
            self.access_token = self._access_response.get('access_token')
            self.expires = datetime.datetime.strptime(self._access_response.get('.expires'), "%a, %d %b %Y %H:%M:%S %Z")
            self.expires_in = self._access_response.get('expires_in')
            self.issued = self._access_response.get('issued')
            self.token_type = self._access_response.get('token_type')
            self.refresh_token = self._access_response.get('refresh_token')

    def get_security_groups(self):
        response = requests.get("{}/api/V2/getsecuritygroups".format(self.host), headers=self.headers)
        return response

    def save_user_batch(self, data, version="v1"):
        return requests.post("{}/{}".format(self.host, "api/v1/saveuserbatch"), headers=self.headers, data=data)

    @property
    def expired(self):
        return not self.expires or self.expires < datetime.datetime.utcnow()

    @property
    def headers(self):
        if not self.access_token:
            self.login()
        return create_headers_dict(self.access_token)

    def get_user_batch(self, data):
        template = {
            "readRequests": [

            ],
            "stopOnError": "false"
        }
        user_list = [{"loginId": d, "publicId": ""} for d in data]
        template['readRequests'] = user_list
        return requests.post("{}/{}".format(self.host, "api/v1/getuserbatch"), headers=self.headers,
                             data=json.dumps(template))

    def get_teams(self):
        return self.get("api/v1/getteams", headers=self.headers)

    def add_user_to_team_by_batch(self, user_dict_list, stop_on_error="false"):
        template = {"addUserToTeamRequests": user_dict_list, "stopOnError": stop_on_error}
        return self.post("api/v1/addusertoteambybatch", template)

    def removeuserfromteam(self, team_id, user_record_id):
        return self.delete("api/V2/removeuserfromteam/teamid/{team_id}/userrecordid/{user_record_id}".
                           format(team_id=team_id, user_record_id=user_record_id))

    @check_expired
    def get(self, url, headers=None):
        headers = self.headers if not headers else headers
        return requests.get("{}/{}".format(self.host, url), headers=headers)

    @check_expired
    def post(self, url, data, headers=None):
        headers = self.headers if not headers else headers
        return requests.post("{}/{}".format(self.host, url), headers=headers, data=json.dumps(data))

    @check_expired
    def delete(self, url, headers=None):
        headers = self.headers if not headers else headers
        return requests.delete("{}/{}".format(self.host, url), headers=headers)


def login(user, password, client_id, host, grant_type="password", auth_mode="Internal"):
    """
    :param user:
    :param password:
    :param client_id:
    :param host:
    :param grant_type:
    :param auth_mode:
    :return:
    """
    data = "grant_type={grant_type}&client_id={client}&username={user}&password={password}" \
        .format(client=client_id, user=user, password=password, grant_type=grant_type)
    url = "{host}/token?auth_mode={auth_mode}".format(host=host, auth_mode=auth_mode)

    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise ValueError("Login Failed with status code: {} Reason: {}".format(response.status_code, response.reason))
    return response.json()


if __name__ == '__main__':
    pass
