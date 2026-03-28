from unittest.mock import Mock, patch

from api.aeroplanes_api import AeroplanesAPI


class TestAeroplanesAPI:
    @patch("api.aeroplanes_api.requests.get")
    def test_get_country_coordinates_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"boundingbox": ["35.0", "70.0", "-10.0", "60.0"]}]
        mock_get.return_value = mock_response

        api = AeroplanesAPI()
        coords = api.get_country_coordinates("Russia")

        assert coords == (35.0, 70.0, -10.0, 60.0)

    @patch("api.aeroplanes_api.requests.get")
    def test_get_country_coordinates_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        api = AeroplanesAPI()
        coords = api.get_country_coordinates("Russia")

        assert coords is None

    @patch("api.aeroplanes_api.requests.get")
    def test_get_aeroplanes_success(self, mock_get):
        with patch.object(AeroplanesAPI, "get_country_coordinates", return_value=(35.0, 70.0, -10.0, 60.0)):
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"states": [["abc123", "AFL123", "Russia", 0, 0, 0, 0, 10000, 0, 850]]}
            mock_get.return_value = mock_response

            api = AeroplanesAPI()
            data = api.get_aeroplanes("Russia")

            assert len(data) == 1
            assert data[0][0] == "abc123"

    @patch("api.aeroplanes_api.requests.get")
    def test_get_aeroplanes_no_coords(self, mock_get):
        with patch.object(AeroplanesAPI, "get_country_coordinates", return_value=None):
            api = AeroplanesAPI()
            data = api.get_aeroplanes("Russia")
            assert data == []
            mock_get.assert_not_called()

    @patch("api.aeroplanes_api.requests.get")
    def test_get_country_coordinates_http_error(self, mock_get):
        """Тест на статус код 500 (покрывает строки 20, 22-23)"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        api = AeroplanesAPI()
        coords = api.get_country_coordinates("Russia")

        assert coords is None

    @patch("api.aeroplanes_api.requests.get")
    def test_get_aeroplanes_http_error(self, mock_get):
        with patch.object(AeroplanesAPI, "get_country_coordinates", return_value=(35.0, 70.0, -10.0, 60.0)):
            mock_response = Mock()
            mock_response.status_code = 500
            mock_get.return_value = mock_response

            api = AeroplanesAPI()
            data = api.get_aeroplanes("Russia")

            assert data == []
