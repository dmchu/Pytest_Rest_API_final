from lib.base_case import BaseCase
from lib.assersions import Assertions as AS
from lib.my_requests import MyRequests as MR
from lib.helpers import Helpers as HP

class TestUserEdit(BaseCase):
    BASE_URI: str = "/user/"
    URI_LOGIN: str = BASE_URI + "login"

    def test_edit_just_created_user(self):
        registered_user: dict = HP.register_user(HP)
        user_email = registered_user.get("user_email")
        user_password = registered_user.get("user_password")
        user_id = registered_user.get("user_id")

        login_user_response = HP.authorize_user(HP, user_email, user_password)

        URI_USER = self.BASE_URI + str(user_id)
        new_name = "Changed Name"
        headers = {
            'x-csrf-token': login_user_response.get("token")
        }
        cookies = {
            'auth_sid': login_user_response.get("auth_sid")
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
        registered_user: dict = HP.register_user(HP)
        user_id = registered_user.get("user_id")
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

    def test_edit_existing_user_with_authorization_by_another_user(self):
        registered_user: dict = HP.register_user(HP)
        correct_user_email = registered_user.get("user_email")
        correct_user_password = registered_user.get("user_password")
        user_id = registered_user.get("user_id")

        user_email = "vinkotov@example.com"
        user_password = "1234"


        # Authorization with another user
        login_data = {
            'email': user_email,
            'password': user_password
        }

        response = MR.post(self.URI_LOGIN, data=login_data)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")

        URI_USER = self.BASE_URI + str(user_id)
        new_name = "Changed Name3"
        headers = {
            'x-csrf-token': token
        }
        cookies = {
            'auth_sid': auth_sid
        }
        edit_data = {
            'email': new_name
        }
        # Try to edit user data

        response2 = MR.put(URI_USER, headers=headers, cookies=cookies, data=edit_data)
        AS.assert_code_status(response2, 400)

        # Authorization with correct user
        login_user_response = HP.authorize_user(HP, correct_user_email, correct_user_password)

        URI_USER = self.BASE_URI + str(user_id)
        new_name = "Changed Name"
        headers_2 = {
            'x-csrf-token': login_user_response.get("token")
        }
        cookies_2 = {
            'auth_sid': login_user_response.get("auth_sid")
        }
        # Get user data and verify that changes was not made

        response4 = MR.get(URI_USER, headers=headers_2, cookies=cookies_2)
        response_data = response4.json()
        user_first_name = response_data.get("firstName")
        assert user_first_name != new_name,\
            "First name should not be changed by user with another authenticated user, but it did"

    def test_edit_user_email_with_wrong_format(self):
        registered_user: dict = HP.register_user(HP)
        user_email = registered_user.get("user_email")
        user_password = registered_user.get("user_password")
        user_id = registered_user.get("user_id")

        login_user_response = HP.authorize_user(HP, user_email, user_password)

        URI_USER = self.BASE_URI + str(user_id)
        new_email = user_email.replace("@", ".")

        headers = {
            'x-csrf-token': login_user_response.get("token")
        }
        cookies = {
            'auth_sid': login_user_response.get("auth_sid")
        }
        edit_data = {
            'email': new_email
        }
        # Edit user data

        response3 = MR.put(URI_USER, headers=headers, cookies=cookies, data=edit_data)
        AS.assert_code_status(response3, 400)
        AS.assert_response_text(response3, "Invalid email format")

        # Get updated user data

        response4 = MR.get(URI_USER, headers=headers, cookies=cookies)
        response_data = response4.json()
        user_email = response_data.get("email")
        assert user_email != new_email,\
            "Email should not be changed by user to email with wrong format, but it did"

    def test_edit_user_first_name_with_one_character(self):
        registered_user: dict = HP.register_user(HP)
        user_email = registered_user.get("user_email")
        user_password = registered_user.get("user_password")
        user_id = registered_user.get("user_id")

        login_user_response = HP.authorize_user(HP, user_email, user_password)

        URI_USER = self.BASE_URI + str(user_id)
        new_email = user_email.replace("@", ".")

        headers = {
            'x-csrf-token': login_user_response.get("token")
        }
        cookies = {
            'auth_sid': login_user_response.get("auth_sid")
        }
        edit_data = {
            'firstName': "V"
        }
        # Edit user data

        response3 = MR.put(URI_USER, headers=headers, cookies=cookies, data=edit_data)
        AS.assert_code_status(response3, 400)
        AS.assert_json_value_by_name(response3, "error",
                                     "Too short value for field firstName", "The error message is not as expected")

        # Get updated user data

        response4 = MR.get(URI_USER, headers=headers, cookies=cookies)
        response_data = response4.json()
        user_first_name = response_data.get("firstName")
        assert user_first_name != "V", \
            "First name should not be changed by user to very short name, but it did"
