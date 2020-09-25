import time
from unittest.mock import Mock, patch

from murakami.exporters.http import HTTPExporter

RESPONSE_SUCCESS_JSON = {
    'status': 'success'
}

RESPONSE_FAILURE_JSON = {
    'error': '<Error type>',
    'message': '<Error message>'
}

@patch('requests.post')
def test_push_response_ok(mock_post):
    mock_post.return_value = Mock(ok=True)
    mock_post.return_value.json.return_value = RESPONSE_SUCCESS_JSON

    exporter = HTTPExporter("test", config={'url': 'http://testurl'})
    assert exporter.push("ndt5", '{"TestName": "ndt5"}', time.time()) is True

@patch('requests.post')
def test_push_response_error(mock_post):
    mock_post.return_value = Mock(ok=False)
    mock_post.return_value.json.return_value = RESPONSE_FAILURE_JSON

    exporter = HTTPExporter("test", config={'url': 'http://testurl'})
    assert exporter.push("ndt5", '{"TestName": "ndt5"}', time.time()) is False
