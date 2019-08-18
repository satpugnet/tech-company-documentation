import os

from algoliasearch.search_client import SearchClient

ALGOLIA_APP_ID = os.getenv("ALGOLIA_APP_ID")
ALGOLIA_ADMIN_KEY = os.getenv("ALGOLIA_ADMIN_KEY")
ALGOLIA_SEARCH_KEY = os.getenv("ALGOLIA_SEARCH_KEY")

INDEX_NAME = "test_DOCUMENTATION"

CLIENT = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_ADMIN_KEY)
INDEX = CLIENT.init_index(INDEX_NAME)


def insert_doc(doc):
    INDEX.save_objects([
        doc
    ])