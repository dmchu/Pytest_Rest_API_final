from decouple import config


class Environment:
    DEV = "dev"
    PROD = "prod"

    URLS = {
        DEV: config("DEV_URL"),
        PROD: config("PROD_URL")
    }

    def __init__(self):
        try:
            self.env = config("ENV")
        except KeyError:
            self.env = self.DEV

    def get_base_url(self):
        if self.env in self.URLS:
            return self.URLS.get(self.env)
        else:
            raise Exception(f"Unnown value of ENV variable {self.env}")


ENV_OBJECT = Environment()