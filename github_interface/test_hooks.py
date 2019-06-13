import json

import requests

from hooks import hook_manager

# hooks = hook_manager.subscribe_hooks("fc08d7d54a93e264c94b6c0f87e0f5a56e3b198f",
#                                      owner="paulvidal",
#                                      repo="1-week-1-tool",
#                                      url_postback="https://47defdd8.ngrok.io/webhook")
#
# print(hooks)
#
# hooks = hook_manager.get_hooks("fc08d7d54a93e264c94b6c0f87e0f5a56e3b198f",
#                                owner="paulvidal",
#                                repo="1-week-1-tool")
#
# print(hooks)
#
# p = requests.post(
#     "https://api.github.com/repos/paulvidal/1-week-1-tool/hooks/112655114/pings",
#     headers={'Authorization': 'token {}'.format("fc08d7d54a93e264c94b6c0f87e0f5a56e3b198f")}
# )
#
# print(p)

# p = requests.post(
#     "https://api.github.com/repos/paulvidal/1-week-1-tool/issues/1/comments",
#     data=json.dumps({
#         "body": "Well done for creating that commit",
#     }),
#     headers={'Authorization': 'token {}'.format("fc08d7d54a93e264c94b6c0f87e0f5a56e3b198f")}
# )
#
# print(p)