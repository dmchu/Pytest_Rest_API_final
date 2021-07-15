
from lib.base_case import BaseCase as BC
from lib.assersions import Assertions as AS
from lib.my_requests import MyRequests as MR
from lib.helpers import Helpers as HP


class TestUserDelete(BC):
    BASE_URI: str = "/user/"
    URI_LOGIN: str = BASE_URI + "login"

    def test_delete_existing_user(self):

        user_email = "vinkotov@example.com"
        user_password = "1234"

        delete_user_response = HP.delete_user(HP, user_email, user_password)
        AS.assert_code_status(delete_user_response, 400)

        login_user_response = HP.authorize_user(HP, user_email, user_password)
        uri_user = self.BASE_URI + str(login_user_response.get("user_id"))

        get_user_info_response = MR.get(uri_user)
        AS.assert_code_status(get_user_info_response, 200)
        AS.assert_json_value_by_name(get_user_info_response, "username", "Vitaliy", "Unexpected response value for 'username'")


    def test_delete_user_successfully(self):
        registered_user: dict = HP.register_user(HP)
        user_email = registered_user.get("user_email")
        user_password = registered_user.get("user_password")
        user_id = registered_user.get("user_id")

        delete_user_response = HP.delete_user(HP, user_email=user_email, user_password=user_password)
        AS.assert_code_status(delete_user_response, 200)

        uri_user = self.BASE_URI + str(user_id)
        get_user_info_response = MR.get(uri_user)
        AS.assert_code_status(get_user_info_response, 404)
        assert get_user_info_response.text == f"User not found", f"Unexpected response text {get_user_info_response.text}"


