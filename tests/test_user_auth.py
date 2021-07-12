import pytest
import allure
from lib.base_case import BaseCase
from lib.assersions import Assertions as AS
from lib.my_requests import MyRequests as MR

@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):

    exclude_params = [("no_cookie"), ("no_tocken")]

    def setup(self):
        self.URI1 = "/user/login"
        self.URI2 = "/user/auth"
        self.payload_1 = {
            'email':'vinkotov@example.com',
            'password':'1234'
        }

        response1 = MR.post(url=self.URI1, data=self.payload_1)
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")
        self.auth_headers = {
            "x-csrf-token": self.token,
        }
        self.auth_cookies = {
            "auth_sid": self.auth_sid
        }

    @allure.description("Verifiying 'happy path' for user authentication by email and password")
    def test_auth_user(self):
        response2 = MR.get(self.URI2,headers=self.auth_headers, cookies=self.auth_cookies)
        error_message = "User id from auth method is not equal to user id from check method"
        AS.assert_json_value_by_name(response2, "user_id", self.user_id_from_auth_method, error_message)

    @allure.description("Verifiying authorization without sending auth cookie or token")
    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            response2 = MR.get(self.URI2, headers=self.auth_headers)
        else:
            response2 = MR.get(self.URI2, cookies=self.auth_cookies)

        error_message = f"User is authorized with condition {condition}"
        AS.assert_json_value_by_name(response2, "user_id", 0, error_message)
