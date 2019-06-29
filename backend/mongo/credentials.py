import json


class CredentialsManager:

    @staticmethod
    def write_credentials(user_access_token="", installation_access_token=""):
        credentials = CredentialsManager.read_credentials()

        user_access_token = credentials[
            "user_access_token"] if "user_access_token" in credentials and not user_access_token else user_access_token
        installation_access_token = credentials[
            "installation_access_token"] if "installation_access_token" in credentials and not installation_access_token else installation_access_token

        with open("backend/ressources/credentials.txt", "w") as file:
            credentials = "{\"installation_access_token\":\"" + str(
                installation_access_token) + "\",\"user_access_token\":\"" + str(user_access_token) + "\"}"
            file.write(credentials)
            file.close()

    @staticmethod
    def read_credentials():
        with open("backend/ressources/credentials.txt", "r") as file:
            file_content = file.read()
            if file_content == "":
                file_content = "{}"
            file.close()

        return json.loads(file_content)