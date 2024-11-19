import pytest
from _pytest.logging import LogCaptureFixture
from loguru import logger

from cherpy import config_from_env
from cherpy.runonestep import get_onestep, run_onestep, get_object_summary

name = "Call Reconcile HPDM Devices"
association = "discovereddevices"
scope = "Global"


@pytest.fixture
def client():
    return config_from_env("cherpy_dev")


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


def test_get_onestep(client):
    onestep = get_onestep(client, association=association, onestep_name=name, scope=scope)

    assert onestep.get('name') and onestep.get('name').lower() == name.lower()


@pytest.mark.parametrize("association, expected",
                         [("discovereddevices", True),
                          ("bad name", False),
                          ])
def test_get_object_summary(client, association, expected):
    if expected:
        onestep = get_object_summary(client, association)
        assert onestep.get('busObId')
    else:
        with pytest.raises(SystemExit) as execinfo:
            get_object_summary(client, association)
        assert execinfo.type == SystemExit
