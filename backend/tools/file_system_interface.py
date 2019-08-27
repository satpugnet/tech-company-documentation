from tools import logger


class FileSystemInterface:
    """
    An interface to access the local file system.
    """

    @staticmethod
    def load_private_key():
        """
        :return: The private key for our Github App.
        """
        logger.get_logger().info("Loading the private key from the file system.")

        with open('backend/ressources/github-private-key.pem', 'rb') as file:
            private_key = file.read()
            file.close()

            return private_key
