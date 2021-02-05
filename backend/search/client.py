import os

from algoliasearch.search_client import SearchClient

from tools import logger

ALGOLIA_APP_ID = os.getenv("ALGOLIA_APP_ID")
ALGOLIA_ADMIN_KEY = os.getenv("ALGOLIA_ADMIN_KEY")
ALGOLIA_SEARCH_KEY = os.getenv("ALGOLIA_SEARCH_KEY")

INDEX_NAME = "test_DOCUMENTATION"

try:
    CLIENT = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_ADMIN_KEY)
    INDEX = CLIENT.init_index(INDEX_NAME)
except Exception:
    logger.get_logger().exception("Failed to initialise algolia client")


def insert_doc(doc):
    success = True

    try:
        INDEX.save_objects([doc])
    except Exception:
        logger.get_logger().exception("Failed to index markdown document %s", doc)
        success = False

    return success
