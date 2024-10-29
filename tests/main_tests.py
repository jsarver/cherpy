import pytest
from cherpy.auth import config_from_env
from cherpy.main import search_object

c = config_from_env("chewey_config")
c.login()

# confirm that object query works
results = search_object(c, object_name="incident", pageSize=2).json()
print(len(results['businessObjects']) > 0)

template_response = {'errorCode': None,
 'errorMessage': None,
 'fields': [{'dirty': False,
   'displayName': 'Product Name',
   'fieldId': '94249974836712921f87e743d990e80a9dc739a041',
   'name': 'ProductName',
   'value': ''},
  {'dirty': False,
   'displayName': 'Owned By Team',
   'fieldId': '9343f8800b9723457d7de946c8bf85a77532ab9e0d',
   'name': 'OwnedByTeam',
   'value': ''}],
 'hasError': False}
