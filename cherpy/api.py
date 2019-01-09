import json

import attr
import yaml
import os

DEFAULT_CONFIG = {}

try:
    import requests
except ImportError:
    pass



def config_from_env(env="CHEWEY_CONFIG"):
    file_name = os.environ[env]
    with open(file_name) as f:
        cfg = yaml.load(f)
    return Client(**cfg)


def create_config(filename="cherpy.yml", **kwargs):

    file_path = os.path.join(os.environ['USERPROFILE'],".cherpy",filename)
    c = Client(**kwargs)
    cfg_dict= attr.asdict(c,filter=attr.filters.exclude(attr.fields(Client).access_token))
    with open(file_path, 'w') as outf:
        yaml.dump(cfg_dict, outf, default_flow_style=False)
    os.system("SETX {0} {1}".format("CHEWEY_CONFIG", file_path))


def create_headers_dict(access_token):
    headers = {"Authorization": "Bearer {}".format(access_token),
               "Content-type": "application/json",
               "Accept": "application/json"}
    return headers

@attr.s
class Client(object):
    host = attr.ib()
    user = attr.ib()
    password = attr.ib()
    client_id = attr.ib()
    access_token = attr.ib(default=None)
    grant_type = attr.ib(default="password")
    auth_mode = attr.ib(default="internal")

    def login(self):
        self.access_token = login(self.user, self.password, self.client_id, self.host, self.grant_type, self.auth_mode)

    def get_security_groups(self):
        h=create_headers_dict(self.access_token)
        response = requests.get("{}/api/V2/getsecuritygroups".format(self.host), headers=h)
        return response

    def save_user_batch(self, data, version="v1"):
        headers = create_headers_dict(self.access_token)
        return requests.post("{}/{}".format(self.host, "api/v1/saveuserbatch"), headers=headers, data=data)

    @property
    def headers(self):
        return create_headers_dict(self.access_token)

    def get_user_batch(self, data ):
        template ={
            "readRequests": [

            ],
            "stopOnError": "false"
        }
        user_list = [{"loginId": d, "publicId": ""} for d in data]
        template['readRequests'] = user_list
        headers = create_headers_dict(self.access_token)
        return requests.post("{}/{}".format(self.host, "api/v1/getuserbatch"), headers=headers, data=json.dumps(template))


    def get_teams(self):
        headers = create_headers_dict(self.access_token)
        return self.get("api/v1/getteams", headers=headers)

    def add_user_to_team_by_batch(self, user_dict_list, stop_on_error="false"):
        template = {
            "addUserToTeamRequests": [],
            "stopOnError": stop_on_error
        }
        template["addUserToTeamRequests"] = user_dict_list

        return self.post("api/v1/addusertoteambybatch", template)

    def removeuserfromteam(self,team_id, user_record_id):
        return self.delete("api/V2/removeuserfromteam/teamid/{team_id}/userrecordid/{user_record_id}".
                           format(team_id=team_id, user_record_id=user_record_id))
    def get(self, url, headers=None):
        headers = self.headers if not headers else headers
        return requests.get("{}/{}".format(self.host, url), headers=headers)

    def post(self,url, data, headers=None):
        headers = self.headers if not headers else headers
        return requests.post("{}/{}".format(self.host, url), headers=headers,data=json.dumps(data))

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
    data = "grant_type={grant_type}&client_id={client}&username={user}&password={password}"\
        .format(client=client_id, user=user,password=password, grant_type=grant_type)
    url = "{host}/token?auth_mode={auth_mode}".format(host=host, auth_mode=auth_mode)
    response = requests.post(url, data=data).json()
    token = response.get('access_token')
    return token

if __name__ == '__main__':
    c=config_from_env()

