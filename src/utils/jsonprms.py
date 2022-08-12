import json


class Prms:

    def __init__(self, jsonFn):
        #print(jsonFn)
        try:
                with open(jsonFn) as f:
                    self.prms = json.load(f)
        except Exception as e:
                print(f"EXCEPTION json={e}")