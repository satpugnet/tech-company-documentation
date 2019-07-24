from server.webhook_server import manually_update_db
import sys

manually_update_db(str(sys.argv[1]))
