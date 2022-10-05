import requests
import json
class Offsets:
    def __init__(self):
        print('запрос оффсетов у Hazedumper')
        request = requests.get('https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json')
        self.offsets = json.loads(request.content)
    def get_offsets(self):
        return self.offsets