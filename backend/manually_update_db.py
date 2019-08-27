import sys

from webhook.webhook_server import manually_update_db


# Used for development to manually update the database to take into account the latest commit.
manually_update_db(str(sys.argv[1]), str(sys.argv[2]))
