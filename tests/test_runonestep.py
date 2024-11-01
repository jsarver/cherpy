import pytest
from _pytest.logging import LogCaptureFixture
from loguru import logger

from cherpy import config_from_env
from cherpy.runonestep import get_onestep, run_onestep, get_object_summary

client = config_from_env("cherpy_dev")
client.login()

name = "Call Reconcile HPDM Devices"
association = "discovereddevices"
scope = "Global"


@pytest.fixture
def cfg():
    return client.__dict__


@pytest.fixture
def token():
    return client.access_token


@pytest.fixture
def caplog(caplog: LogCaptureFixture):
    handler_id = logger.add(
        caplog.handler,
        format="{message}",
        level=0,
        filter=lambda record: record["level"].no >= caplog.handler.level,
        enqueue=False,  # Set to 'True' if your test is spawning child processes.
    )
    yield caplog
    logger.remove(handler_id)


def test_get_onestep(cfg, token):
    association = "discovereddevices"
    object_summary = get_object_summary(cfg, association, token)
    bus_ob_id = object_summary.get('busObId')
    onestep = get_onestep(cfg, association=bus_ob_id, onestep_name=name, scope=scope, token=token)

    assert onestep.get('name') and onestep.get('name') == name


@pytest.mark.parametrize("association, expected", [
    ("discovereddevices", True),
    ("bad name", False),
])
def test_get_object_summary(cfg, association, token, expected):
    if expected:
        onestep = get_object_summary(cfg, association, token)
        assert onestep.get('busObId')
    else:
        with pytest.raises(SystemExit) as execinfo:
            get_object_summary(cfg, association, token)
        assert execinfo.type == SystemExit
