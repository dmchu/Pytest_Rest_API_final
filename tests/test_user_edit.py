from lib.base_case import BaseCase
from lib.assersions import Assertions as AS
from lib.my_requests import MyRequests as MR

class TestUserEdit(BaseCase):

    BASE_URI: str = "/user/"

    def test_edit_just_created_user(self):
        # Registration
        register_data = self.prepare_registration_data()
        response1 = MR.post(self.BASE_URI, data=register_data)
        AS.assert_code_status(response1, 200)
        AS.assert_json_has_key(response1, "id")
        user_email = register_data.get("email")
        user_password = register_data.get("password")
        user_id = self.get_json_value(response1, "id")

        # Authorization
        login_data = {
            'email': user_email,
            'password': user_password
        }

        URI1 = self.BASE_URI + "login"

        response2 = MR.post(URI1, data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        URI2 = self.BASE_URI + str(user_id)
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

        response3 = MR.put(URI2, headers=headers, cookies=cookies, data=edit_data)
        AS.assert_code_status(response3, 200)

        # Get updated user data

        response4 = MR.get(URI2, headers=headers, cookies=cookies)
        AS.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of user after update")