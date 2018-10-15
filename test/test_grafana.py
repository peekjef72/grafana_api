import unittest
from unittest.mock import patch, Mock

from grafana_api.grafana_face import GrafanaFace


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestGrafanaAPI(unittest.TestCase):
    @patch('grafana_api.grafana_api.GrafanaAPI.__getattr__')
    def test_grafana_api(self, mock_get):
        mock_get.return_value = Mock()
        mock_get.return_value.return_value = """{
  "email": "user@mygraf.com",
  "name": "admin",
  "login": "admin",
  "theme": "light",
  "orgId": 1,
  "isGrafanaAdmin": true
}"""
        cli = GrafanaFace(('admin', 'admin'), host='localhost',
                          url_path_prefix='', protocol='https')
        cli.users.find_user('test@test.com')

    def test_grafana_api_no_verify(self):
        cli = GrafanaFace(('admin', 'admin'), host='localhost',
                          url_path_prefix='', protocol='https', verify=False)
        cli.api.s.get = Mock(name='get')
        cli.api.s.get.return_value = MockResponse({
  "email": "user@mygraf.com",
  "name": "admin",
  "login": "admin",
  "theme": "light",
  "orgId": 1,
  "isGrafanaAdmin": True}, 200)

        cli.users.find_user('test@test.com')
        cli.api.s.get.assert_called_once_with('https://localhost/api/users/lookup?loginOrEmail=test@test.com', auth=('admin', 'admin'), headers=None, json=None, verify=False)


if __name__ == '__main__':
    unittest.main()
