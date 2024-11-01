import pytest
from cherpy.auth import config_from_env
from cherpy.main import search_object

c = config_from_env("cherpy_dev")
c.login()

# confirm that object query works
@pytest.fixture()
def test_search_object():
    response = search_object(c, object_name="Incident",
                             pageSize=10)
    assert response.status_code == 200
