class FileSystemInterface:
    """
    An interfacr to access the local file system.
    """

    @staticmethod
    def load_private_key():
        """
        :return: The private key for our Github App.
        """

        with open('backend/ressources/github-private-key.pem', 'rb') as file:
            private_key = file.read()
            file.close()

            return private_key
