from lib.base_case import BaseCase
from lib.assersions import Assertions as AS
from lib.my_requests import MyRequests as MR


class TestUserEdit(BaseCase):
    BASE_URI: str = "/user/"
    URI_LOGIN: str = BASE_URI + "login"


    def setup(self):
        # Registration
        register_data = self.prepare_registration_data()
        response1 = MR.post(self.BASE_URI, data=register_data)
        AS.assert_code_status(response1, 200)
        AS.assert_json_has_key(response1, "id")
        self.registered_user: dict = {
            "user_email": register_data.get("email"),
            "user_password": register_data.get("password"),
            "user_id": self.get_json_value(response1, "id")
        }


    def test_edit_just_created_user(self):
        user_email = self.registered_user.get("user_email")
        user_password = self.registered_user.get("user_password")
        user_id = self.registered_user.get("user_id")

        # Authorization
        login_data = {
            'email': user_email,
            'password': user_password
        }

        response2 = MR.post(self.URI_LOGIN, data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        URI_USER = self.BASE_URI + str(user_id)
        new_name = "Changed Name"
        headers = {
            'x-csrf-token': token
        }
        cookies = {
            'auth_sid': auth_sid
        }
        edit_data = {
            'firstName': new_name
        }
        # Edit user data

        response3 = MR.put(URI_USER, headers=headers, cookies=cookies, data=edit_data)
        AS.assert_code_status(response3, 200)

        # Get updated user data

        response4 = MR.get(URI_USER, headers=headers, cookies=cookies)
        AS.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of user after update")

    def test_edit_existing_user_without_authorization(self):
        user_id = self.registered_user.get("user_id")
        URI_USER = self.BASE_URI + str(user_id)
        new_name = "Changed Name2"
        headers = {
            'x-csrf-token': ""
        }
        cookies = {
            'auth_sid': ""
        }
        edit_data = {
            'firstName': new_name
        }
        # Edit user data

        response = MR.put(URI_USER, headers=headers, cookies=cookies, data=edit_data)
        AS.assert_code_status(response, 400)
        AS.assert_response_text(response, "Auth token not supplied")
