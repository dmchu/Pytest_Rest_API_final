from lib.base_case import BaseCase
from lib.assersions import Assertions as AS
from lib.my_requests import MyRequests as MR

class TestUserGet(BaseCase):

    BASE_URI: str = "/user/"

    def test_get_user_details_not_auth(self):
        user_id = "2"
        URI = self.BASE_URI + user_id
        response = MR.get(URI)
        AS.assert_json_has_key(response, "username")
        expected_fields = ["email", "firstName", "lastName"]
        AS.assert_json_has_no_keys(response, expected_fields)

    def test_get_user_details_auth_as_same_user(self):
        URI1 = self.BASE_URI + "login"
        user_email = "vinkotov@example.com"
        user_password = "1234"
        data = {
            'email': user_email,
            'password': user_password
        }
        response1 = MR.post(URI1, data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        URI2 = self.BASE_URI + str(user_id_from_auth_method)
        headers = {
            'x-csrf-token': token
        }
        cookies = {
            'auth_sid': auth_sid
        }
        response2 = MR.get(URI2, headers=headers, cookies=cookies)
        expected_fields = ["username", "email", "firstName", "lastName"]
        AS.assert_json_has_keys(response2, expected_fields)
