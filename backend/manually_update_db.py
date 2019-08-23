import sys

from webhook.webhook_server import manually_update_db

manually_update_db(str(sys.argv[1]), str(sys.argv[2]))
