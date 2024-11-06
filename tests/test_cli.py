# test that the CLI works using click testing
from click.testing import CliRunner

from cherpy.cli import search_object_cli


def test_search_object_cli():
    runner = CliRunner()
    result = runner.invoke(search_object_cli,
                           ['--env', 'cherpy_dev', '--object-name', 'Incident', '--page-size', '10', '--output-file',
                            'test.csv'])
    assert result.exit_code == 0
    with open('../cherpy/test.csv', 'r') as f:
        assert f.read() != ""
