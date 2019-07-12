class FileInterface:

    @staticmethod
    def load_private_key():
        with open('backend/ressources/github-private-key.pem', 'rb') as file:
            private_key = file.read()
            file.close()
            return private_key