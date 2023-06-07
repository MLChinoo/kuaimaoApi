import api
import pprint
pp = pprint.PrettyPrinter(indent=4)

api.setProxy({
    "http": "http://127.0.0.1:10809",
    "https": "http://127.0.0.1:10809"
})
pp.pprint(api.getUserInfo("82036755", 1, 3))
