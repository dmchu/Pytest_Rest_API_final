from lib.base_case import BaseCase as BC
from lib.my_requests import MyRequests as MR
from lib.assersions import Assertions as AS

class Helpers(BC, MR):
    BASE_URI: str = "/user/"

    @staticmethod
    def authorize_user(cls, user_email, user_password) -> dict:
        # Authorization

        uri_login: str = cls.BASE_URI + "login"
        login_data = {
            'email': user_email,
            'password': user_password
        }
        bc = BC()
        response = MR.post(uri_login, data=login_data)
        user_id = response.json()["user_id"]
        auth_sid = BC.get_cookie(bc,response=response, cookie_name="auth_sid")
        token = BC.get_header(bc,response=response, headers_name="x-csrf-token")

        return {
            "user_id": user_id,
            "token": token,
            "auth_sid": auth_sid
        }
    @staticmethod
    def delete_user(cls, user_email, user_password):
        authentication_data = cls.authorize_user(cls,user_email, user_password)
        user_id = authentication_data.get("user_id")
        URI_USER = cls.BASE_URI + str(user_id)

        headers = {
            'x-csrf-token': authentication_data.get("token")
        }
        cookies = {
            'auth_sid': authentication_data.get("auth_sid")
        }

        return MR.delete(URI_USER, headers=headers, cookies=cookies)

    @staticmethod
    def register_user(cls) -> dict:
        # Registration
        bc = BC()
        register_data = BC.prepare_registration_data(bc)
        response1 = MR.post(cls.BASE_URI, data=register_data)
        AS.assert_code_status(response1, 200)
        AS.assert_json_has_key(response1, "id")
        registered_user: dict = {
            "user_email": register_data.get("email"),
            "user_password": register_data.get("password"),
            "user_id": BC.get_json_value(bc,response1, "id")
        }
        return registered_user

    @staticmethod
    def get_user_data(cls, user_email, user_password):
        authentication_data = cls.authorize_user(cls,user_email, user_password)
        user_id = authentication_data.get("user_id")
        URI_USER = cls.BASE_URI + str(user_id)

        headers = {
            'x-csrf-token': authentication_data.get("token")
        }
        cookies = {
            'auth_sid': authentication_data.get("auth_sid")
        }

        return MR.get(URI_USER, headers=headers, cookies=cookies)
